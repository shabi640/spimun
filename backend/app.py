from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
from flask_socketio import SocketIO, emit, join_room
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from flask_cors import CORS
import pypandoc
import json
from models import db, bcrypt, Amendment, Chair, Delegate, Group, Message, File, Clause, UnreadCount  # Import all models
from werkzeug.utils import secure_filename

from bs4 import BeautifulSoup
from sqlalchemy.orm import joinedload
import base64
import requests
import re


#configure flask app

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for development
BASE_UPLOAD_FOLDER = 'uploads'
app.config['JWT_SECRET_KEY'] = 'LAIWHFoHEFAWHBOIGBFOBWEFOWBAOFGBAIWOEFBNC'
app.config['UPLOAD_FOLDER'] = BASE_UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///amendments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CHAT_FILES'] = os.path.join(os.getcwd(), 'chatfiles')

db.init_app(app)
jwt = JWTManager(app)
bcrypt = bcrypt.init_app(app)
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:5173", "http://172.30.27.44:5173"])

# Ensure the base upload folder exists
if not os.path.exists(BASE_UPLOAD_FOLDER):
    os.makedirs(BASE_UPLOAD_FOLDER)
    
# Ensure the upload folder exists
if not os.path.exists(app.config['CHAT_FILES']):
    os.makedirs(app.config['CHAT_FILES'])

GROUPS = ['junior', 'senior', 'security council']


    
# Create the database and table
with app.app_context():
    from initialize_db import initialize_database
    initialize_database()

# Endpoint to get all users
@app.route('/delegates', methods=['GET'])
def get_delegates():
    delegates = Delegate.query.all()
    return jsonify([delegate.serialize() for delegate in delegates])


# search the groups that relate to this delegate id
@app.route('/searchgroup/<int:id>', methods=['GET'])
def get_groups_for_delegate(id):
    try:
        delegate = Delegate.query.get(id)
        if not delegate:
            return jsonify({"error": "Delegate not found"}), 404

        groups = delegate.groups
        group_list = []
        for group in groups:
            # Get the last message for the group
            last_message = None
            if group.messages:
                # For group ID 1, always use message with ID 1
                if group.id == 1:
                    special_message = Message.query.get(1)
                    last_message = special_message.serialize() if special_message else None
                else:
                    last_message = group.messages[-1].serialize()

            group_data = group.serialize()
            group_data["lastMessage"] = last_message
            
            # Get unread count from the UnreadCount table
            unread_count = UnreadCount.query.filter_by(user_id=id, group_id=group.id).first()
            if unread_count:
                group_data["unreadCount"] = unread_count.count
            else:
                # Create a new entry if one doesn't exist
                new_unread = UnreadCount(user_id=id, group_id=group.id, count=0)
                db.session.add(new_unread)
                db.session.commit()
                group_data["unreadCount"] = 0
                
            group_list.append(group_data)

        return jsonify(group_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get unread count for a specific user and group
@app.route('/unread/<int:user_id>/<int:group_id>', methods=['GET'])
def get_unread_count(user_id, group_id):
    try:
        unread_count = UnreadCount.query.filter_by(user_id=user_id, group_id=group_id).first()
        
        if not unread_count:
            # Create a new entry if one doesn't exist
            unread_count = UnreadCount(user_id=user_id, group_id=group_id, count=0)
            db.session.add(unread_count)
            db.session.commit()
            
        return jsonify({"count": unread_count.count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to update unread count for a specific user and group
@app.route('/unread/<int:user_id>/<int:group_id>', methods=['POST'])
def update_unread_count(user_id, group_id):
    try:
        count = request.json.get('count', 0)
        
        unread_count = UnreadCount.query.filter_by(user_id=user_id, group_id=group_id).first()
        
        if not unread_count:
            # Create a new entry if one doesn't exist
            unread_count = UnreadCount(user_id=user_id, group_id=group_id, count=count)
            db.session.add(unread_count)
        else:
            # Update the existing entry
            unread_count.count = count
            
        db.session.commit()
        
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#Endpoint to send a message
@app.route('/messages', methods=['POST'])
def create_message():
    try:
        # Extract data from the request form
        # We assume the frontend is sending data as multipart/form-data
        content = request.form.get('content', '')  # Message content (text)
        room_id = request.form.get('roomId')
        sender_id = request.form.get('senderId')
        timestamp = request.form.get('timestamp')
        date = request.form.get('date')

        # Validate the required fields
        if not all([room_id, sender_id, timestamp, date]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create a new message entry
        new_message = Message(
            text=content if content else None,  # Allow empty text if only files are being sent
            sender_id=sender_id,
            group_id=room_id,
            timestamp=timestamp,
            date=date
        )
        db.session.add(new_message)
        
        # Check if there are any files being sent
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and file.filename:
                    # Secure the filename
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['CHAT_FILES'], filename)
                    
                    # Save the file
                    file.save(file_path)

                    # Create a new File entry associated with the message
                    new_file = File(
                        message=new_message,
                        name=filename,
                        size=file.content_length,
                        type=file.mimetype,
                        path=os.path.join('/chatfiles',filename)
                    )
                    db.session.add(new_file)

        # Commit all changes to the database
        db.session.commit()

        # Don't emit for group 1 except message ID 1
        if int(room_id) == 1 and new_message.id != 1:
            return jsonify(new_message.serialize()), 201

        # Increment unread count for all users in the group except the sender
        group = Group.query.get(room_id)
        if group:
            for delegate in group.delegates:
                if str(delegate.id) != str(sender_id):  # Skip the sender
                    unread_count = UnreadCount.query.filter_by(user_id=delegate.id, group_id=room_id).first()
                    if unread_count:
                        unread_count.count += 1
                    else:
                        new_unread = UnreadCount(user_id=delegate.id, group_id=room_id, count=1)
                        db.session.add(new_unread)
            db.session.commit()

        # Emit the new message to all connected clients
        socketio.emit('new_message', new_message.serialize(), room=f"group_{room_id}", namespace='/chatsocket')

        return jsonify(new_message.serialize()), 201
    except Exception as e:
        db.session.rollback()  # Roll back the transaction on error
        return jsonify({'error': str(e)}), 500

# Endpoint to serve the uploaded files
@app.route('/chatfiles/<path:filename>', methods=['GET'])
def download_file(filename):
    try:
        # Log the filename and the full path we are trying to access
        full_path = os.path.join(app.config['CHAT_FILES'], filename)
        
        # Check if the file exists before trying to serve it
        if not os.path.exists(full_path):
            return jsonify({'error': 'File not found'}), 404

        return send_from_directory(app.config['CHAT_FILES'], filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#join user's room
@socketio.on('join_user_room', namespace='/chatsocket')
def join_user_room(data):
    user_id = data.get('user_id')
    if user_id:
        join_room(f"user_{user_id}")
        print(f"User {user_id} joined their own room")

#join chat room
@socketio.on('join_room',namespace='/chatsocket')
def handle_join_room(data):
    room_id = data.get('roomId')
    join_room(f"group_{room_id}")  # Add the user to the room

    
# Example of using a namespace
@socketio.on('connect', namespace='/chatsocket')
def handle_connect():
    print('Client connected to /chatsocket')

# Endpoint to get messages for a group with pagination
@app.route('/groups/<int:group_id>/messages', methods=['GET'])
def get_group_messages(group_id):
    try:
        group = Group.query.get_or_404(group_id)
        messages = Message.query.filter_by(group_id=group_id).all()
        
        messages_data = [{
            'id': msg.id,
            'text': msg.text,
            'timestamp': msg.timestamp,
            'sender_id': msg.sender_id,
            'sender_name': msg.sender.name if msg.sender else 'Unknown',
            'date': msg.date,
            'files': [{
                'name': file.name,
                'size': file.size,
                'type': file.type,
                'url': f"http://localhost:8000/{file.path}",
                'preview': f"data:{file.type};base64,{base64.b64encode(open(file.path, 'rb').read()).decode('utf-8')}" if file.type.startswith('image/') and os.path.exists(file.path) else None
            } for file in msg.files]
        } for msg in messages]
        
        return jsonify(messages_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


from datetime import datetime

# Endpoint to create a new group
@app.route('/groups', methods=['POST'])
def create_group():
    data = request.json
    
    # Create a new group with the specified name
    new_group = Group(name=data['name'])
    
    # Add the group to the database
    db.session.add(new_group)
    
    if 'delegate_ids' in data:
        delegate_ids = data['delegate_ids']
        
        # Fetch the delegates from the database based on their IDs
        delegates = Delegate.query.filter(Delegate.id.in_(delegate_ids)).all()
        
        if len(delegates) != len(delegate_ids):
            return jsonify({"error": "Some delegate IDs are invalid"}), 400
        
        # Add the delegates to the group
        new_group.delegates.extend(delegates)
    
    # Commit the new group and delegate assignments to the database
    db.session.commit()
    
    # Serialize the new group data
    new_group_data = new_group.serialize()

    # Create a system message indicating that a user has invited others to the group
    inviting_user_id = data['inviting_user_id']  # Assuming this ID is passed with the request
    inviting_user = Delegate.query.get(inviting_user_id)
    
    if not inviting_user:
        return jsonify({"error": "Invalid inviting user ID"}), 400
    
    invited_users = ', '.join([delegate.name for delegate in delegates if delegate.id != inviting_user_id])
    system_message_text = f"{inviting_user.name} has invited {invited_users} to join the group."

    # Create a new message entry
    system_message = Message(
        text=system_message_text,
        sender_id=inviting_user_id,  # Use the inviting user's ID as the sender
        group_id=new_group.id,
        timestamp=datetime.now().strftime("%H:%M"),  # Current time as 'HH:MM'
        date=datetime.now().strftime("%Y-%m-%d")     # Current date as 'YYYY-MM-DD'
    )
    db.session.add(system_message)
    db.session.commit()
    
    # Include this system message in the group data to notify users immediately
    new_group_data['messages'] = [system_message.serialize()]
    
    # Get all delegate room names
    delegate_rooms = [f"user_{delegate.id}" for delegate in delegates]
    
    # Emit the 'added_to_group' event to all relevant users at once, including the system message
    emit('added_to_group', new_group_data, to=delegate_rooms, namespace='/chatsocket')

    return jsonify(new_group_data), 201



@app.route('/amendments', methods=['GET'])
def get_amendments():
    committee = request.args.get('committee')
    
    if not committee:
        return jsonify({'error': 'Committee is required!'}), 400

    amendments = Amendment.query.filter_by(committee=committee)\
        .options(joinedload(Amendment.clause))\
        .order_by(Amendment.timestamp.desc()).all()

    amendments_list = []
    for amendment in amendments:
        amendment_data = {
            'id': amendment.id,
            'amendment_text': amendment.amendment_text, 
            'country': amendment.country,
            'committee': amendment.committee,
            'clause_id': amendment.clause_id,
            'timestamp': amendment.timestamp.isoformat(),
            'is_published': amendment.is_published,
            'is_rejected': amendment.is_rejected,
            'is_passed': amendment.is_passed,
            'amended_clause': amendment.amended_clause,
            'under_debate': amendment.under_debate,
            'debate_clause_id': amendment.debate_clause_id,
            'clause_status': amendment.clause.is_published if amendment.clause else None
        }
        amendments_list.append(amendment_data)
    
    return jsonify(amendments_list), 200


# Dictionary to store content based on group
content_store = {
    'junior': '',
    'senior': '',
    'security-council': ''
}

# Storage for resolutions by committee
resolutions = {
    'junior': [],
    'senior': [],
    'security-council': [],
}

def normalize_committee_name(committee):
    """Convert between URL-friendly and database-friendly committee names"""
    if committee:
        # For URLs: spaces to hyphens
        if ' ' in committee:
            return committee.replace(' ', '-')
        # For database: hyphens to spaces
        if '-' in committee:
            return committee.replace('-', ' ')
    return committee

@app.route('/api/login', methods=['POST'])
def loginDelegate():
    data = request.json
    name = data.get('name')
    country = data.get('country')

    # Query the database for the delegate
    delegate = Delegate.query.filter_by(name=name, country=country).first()

    if delegate:
        return jsonify({
            'success': True,
            'committee': delegate.committee,
            'id': delegate.id  # Return delegate's ID
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid name or country'
        }), 401


# Endpoint to add a resolution
@app.route('/api/resolutions/<committee>', methods=['POST'])
def add_resolution(committee):
    committee = committee.lower()
    committee = normalize_committee_name(committee)
    if committee not in resolutions:
        return jsonify({"error": "Invalid committee"}), 400

    data = request.json.get('data')
    clause_id = request.json.get('clauseId')
    
    # Update clause status in database
    if clause_id:
        clause = Clause.query.get(clause_id)
        if clause:
            clause.is_published = False
            clause.is_passed = True  # Set is_passed to True
            db.session.commit()
    
    resolutions[committee].append(data)
    
    # Emit a WebSocket event to update the committee's data
    socketio.emit(f'update-{committee}', data)
    socketio.emit('clause_status_changed', {
        'clauseId': clause_id,
        'committee': committee,
        'is_published': False,
        'is_passed': True
    })
    
    return jsonify({"message": "Resolution added successfully"}), 200

# Endpoint to get resolutions
@app.route('/api/resolutions/<committee>', methods=['GET'])
def get_resolutions(committee):
    committee=committee.lower()
    if committee not in resolutions:
        return jsonify({"error": "Invalid committee"}), 400
    print(resolutions[committee])
    return jsonify(resolutions[committee]), 200

@app.route('/current', methods=['GET', 'POST'])
def current_content():
    if request.method == 'POST':
        # Get content and group from the request
        data = request.json
        group = data.get('group').lower()
        content = data.get('content')

        
        # Store the content for the specific group
        if group in content_store:
            content_store[group] = content
            # Broadcast the new content to all connected clients in the relevant group
            socketio.emit('update_content', {'group': group, 'content': content}, room=group)
            return jsonify({"message": "Content stored and broadcasted successfully"}), 200
        else:
            return jsonify({"error": "Invalid group"}), 400

    elif request.method == 'GET':
        group = request.args.get('group')
        # Return the content for the requested group
        if group in content_store:
            return jsonify({"content": content_store[group]}), 200
        else:
            return jsonify({"error": "Invalid group"}), 400

@socketio.on('join', namespace='/content')
def on_join(data):
    group = data['group']
    join_room(group)
    emit('update_content', {'group': group, 'content': content_store[group]}, room=group)

    
@app.route('/amendments/add', methods=['POST'])
def add_amendment():
    data = request.get_json()
    new_amendment = Amendment(
        amendment_text=data['amendment'],
        country=data['country'],
        committee=data['committee'],
        clause_id=data.get('clause_id'),  # Link amendment to clause
        is_published=False,
        is_rejected=False,
        is_passed=False
    )
    db.session.add(new_amendment)
    db.session.commit()

    amendment_data = {
        'id': new_amendment.id,
        'amendment_text': new_amendment.amendment_text,
        'country': new_amendment.country,
        'committee': new_amendment.committee,
        'clause_id': new_amendment.clause_id,
        'timestamp': new_amendment.timestamp.isoformat(),
        'is_published': new_amendment.is_published,
        'is_rejected': new_amendment.is_rejected,
        'is_passed': new_amendment.is_passed
    }

    # Emit the new amendment to all connected clients
    socketio.emit('new_amendment', amendment_data)

    return jsonify({'message': 'Amendment added successfully.'}), 200



@app.route('/amendments/delete', methods=['POST'])
def delete_all_amendments():
    amendments = Amendment.query.all()
    if amendments:
        archive_file = 'archived_amendments.json'

        if os.path.exists(archive_file):
            with open(archive_file, 'r') as file:
                archived_data = json.load(file)
        else:
            archived_data = []

        archived_data.extend([
            {
                'id': amendment.id,
                'amendment_text': amendment.amendment_text,
                'country': amendment.country,
                'committee': amendment.committee,
                'timestamp': amendment.timestamp.isoformat()
            }
            for amendment in amendments
        ])

        with open(archive_file, 'w') as file:
            json.dump(archived_data, file, indent=4)

        db.session.query(Amendment).delete()
        db.session.commit()

        # Emit an event to notify clients to clear the amendments list
        socketio.emit('amendments_cleared')

    return jsonify({'message': 'All amendments have been deleted and archived.'}), 200


@app.route('/amendments/delete/<int:amendment_id>', methods=['DELETE'])
def delete_single_amendment(amendment_id):
    amendment = Amendment.query.get(amendment_id)
    if amendment:
        archive_file = 'archived_amendments.json'

        if os.path.exists(archive_file):
            with open(archive_file, 'r') as file:
                archived_data = json.load(file)
        else:
            archived_data = []

        archived_data.append({
            'id': amendment.id,
            'amendment_text': amendment.amendment_text,
            'country': amendment.country,
            'committee': amendment.committee,
            'timestamp': amendment.timestamp.isoformat()
        })

        with open(archive_file, 'w') as file:
            json.dump(archived_data, file, indent=4)

        db.session.delete(amendment)
        db.session.commit()

        # Emit an event to notify clients about the deletion
        socketio.emit('amendment_deleted', {'id': amendment_id})

        return jsonify({'message': f'Amendment {amendment_id} has been deleted and archived.'}), 200

    return jsonify({'error': 'Amendment not found'}), 404



@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = Chair.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity={'username': user.username})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid username or password"}), 401


@app.route('/chair', methods=['GET'])
@jwt_required()
def chair():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


def get_group_folder(group):
    if group not in GROUPS:
        raise ValueError("Invalid group")
    return os.path.join(BASE_UPLOAD_FOLDER, group)

def docx_to_html(docx_path):
    html_content = pypandoc.convert_file(docx_path, 'html5')
    return html_content

@app.route('/files/<committee>', methods=['GET'])
def list_files(committee):
    normalized_committee = committee
    clauses = Clause.query.filter_by(committee=normalized_committee).order_by(Clause.timestamp.desc()).all()
    return jsonify([{
        'id': clause.id,
        'filename': clause.filename,
        'country': clause.country,
        'timestamp': clause.timestamp.isoformat(),
        'is_published': clause.is_published,
        'is_rejected': clause.is_rejected,
        'is_passed': clause.is_passed
    } for clause in clauses])

@app.route('/clause/<int:clause_id>', methods=['GET'])
def get_clause(clause_id):
    clause = Clause.query.get_or_404(clause_id)
    return jsonify({
        'id': clause.id,
        'committee': clause.committee,
        'country': clause.country,
        'filename': clause.filename,
        'html_content': clause.html_content,
        'timestamp': clause.timestamp.isoformat()
    })

@app.route('/upload/<committee>', methods=['POST'])
def upload_file(committee):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.docx'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], committee, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        try:
            # Convert DOCX to HTML using pypandoc
            html_content = pypandoc.convert_file(
                file_path,
                'html',
                format='docx',
                extra_args=['--wrap=none', '--extract-media=media']
            )
            # Get country from session or request
            country = request.headers.get('X-Country', 'Unknown')
            # Save to database
            clause = Clause(
                committee=committee,
                country=country,
                filename=filename,
                html_content=html_content
            )
            db.session.add(clause)
            db.session.commit()
            # Emit websocket event
            socketio.emit('new_clause', {
                'id': clause.id,
                'committee': committee,
                'country': country,
                'filename': filename,
                'timestamp': clause.timestamp.isoformat()
            })
            
            return jsonify({'message': 'File uploaded successfully'}), 200
            
        except Exception as e:
            return jsonify({'error': f'Conversion failed: {str(e)}'}), 500
        
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/clause/<int:clause_id>/publish', methods=['POST'])
def publish_clause(clause_id):
    try:
        data = request.get_json()
        committee = data.get('committee')
        content = data.get('content')

        # Clear any existing amendments' debate status
        Amendment.query.filter_by(debate_clause_id=clause_id).update({
            'under_debate': False,
            'debate_clause_id': None
        })

        # First check if there's already a published clause for this committee
        existing_published = Clause.query.filter_by(
            committee=committee,
            is_published=True
        ).first()

        if existing_published and existing_published.id != clause_id:
            return jsonify({
                'success': False,
                'message': 'Another clause is already published for this committee'
            }), 409

        # Get the clause to publish
        clause = Clause.query.get_or_404(clause_id)
        
        # Update the content if provided
        if content:
            clause.html_content = content
            
        clause.is_published = True
        db.session.commit()

        # Emit socket event for real-time updates
        socketio.emit('clause_published', {
            'id': clause.id,
            'committee': clause.committee,
            'country': clause.country,
            'content': clause.html_content,
            'timestamp': clause.timestamp.isoformat()
        })

        return jsonify({
            'success': True,
            'message': 'Clause published successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clause/<int:clause_id>/status', methods=['GET'])
def get_clause_status(clause_id):
    try:
        clause = Clause.query.get_or_404(clause_id)
        return jsonify({
            'is_published': clause.is_published,
            'committee': clause.committee,
            'country': clause.country
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/committee/<committee>/published-clause', methods=['GET'])
def get_published_clause(committee):
    try:
        clause = Clause.query.filter_by(
            committee=committee,
            is_published=True
        ).order_by(Clause.timestamp.desc()).first()
        
        if clause:
            return jsonify({
                'id': clause.id,
                'content': clause.html_content,
                'country': clause.country,
                'filename': clause.filename,
                'timestamp': clause.timestamp.isoformat()
            }), 200
        else:
            return jsonify({'message': 'No published clause found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clause/<int:clause_id>/reject', methods=['POST'])
def reject_clause(clause_id):
    try:
        clause = Clause.query.get_or_404(clause_id)
        clause.is_published = False
        clause.is_rejected = True
        db.session.commit()
        
        # Emit websocket event for real-time updates
        socketio.emit('clause_rejected', {
            'clauseId': clause.id,
            'committee': clause.committee
        })
        
        return jsonify({'success': True, 'message': 'Clause rejected successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/clause/<int:clause_id>/unpublish', methods=['POST'])
def unpublish_clause(clause_id):
    try:
        clause = Clause.query.get_or_404(clause_id)
        clause.is_published = False
        db.session.commit()
        
        # Emit websocket event for real-time updates
        socketio.emit('clause_unpublished', {
            'clauseId': clause.id,
            'committee': clause.committee
        })
        
        return jsonify({'success': True, 'message': 'Clause unpublished successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/committee/<committee>/current-clause', methods=['GET'])
def get_current_clause(committee):
    try:
        clause = Clause.query.filter_by(
            committee=committee.lower(),
            is_published=True
        ).first()
        
        if not clause:
            return jsonify({'message': 'No published clause'}), 404
            
        # Find active amendment if exists
        active_amendment = Amendment.query.filter_by(
            debate_clause_id=clause.id,
            under_debate=True
        ).first()
        
        response_data = clause.serialize()
        if active_amendment:
            response_data['active_amendment_id'] = active_amendment.id
            
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add new endpoints for managing amendment status
@app.route('/amendments/<int:amendment_id>/publish', methods=['POST'])
def publish_amendment(amendment_id):
    try:
        amendment = Amendment.query.get_or_404(amendment_id)
        amendment.is_published = True
        amendment.is_rejected = False
        amendment.under_debate = True
        db.session.commit()
        
        socketio.emit('amendment_published', {
            'id': amendment.id,
            'committee': amendment.committee
        })
        
        return jsonify({'message': 'Amendment published successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/amendments/<int:amendment_id>/reject', methods=['POST'])
def reject_amendment(amendment_id):
    try:
        amendment = Amendment.query.get_or_404(amendment_id)
        amendment.is_rejected = True
        amendment.is_published = False
        
        # Clear debate relationships
        amendment.under_debate = False
        debate_clause_id = amendment.debate_clause_id
        amendment.debate_clause_id = None

        db.session.commit()
        
        # Emit cleanup events
        socketio.emit('amendment_rejected', {
            'amendment_id': amendment_id,
            'committee': amendment.committee,
            'debate_clause_id': debate_clause_id  # Include clause ID for cleanup
        })
        
        return jsonify({'success': True, 'message': 'Amendment rejected and removed'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/amendments/<int:amendment_id>/approve', methods=['POST'])
def approve_amendment(amendment_id):
    try:
        amendment = Amendment.query.get_or_404(amendment_id)
        clause = Clause.query.get(amendment.debate_clause_id)
        
        # Clear debate status
        amendment.under_debate = False
        amendment.debate_clause_id = None
        
        # Update amendment status
        amendment.is_passed = True
        amendment.is_published = False
        amendment.is_rejected = False
        
        if clause:
            # Update clause content
            clause.html_content = amendment.amended_clause
            clause.is_amended = False  # Clear amended status
            
            # Commit changes before emitting events
            db.session.commit()
            
            # Emit content update
            socketio.emit('debate_content_update', {
                'committee': amendment.committee,
                'content': clause.html_content,
                'country': clause.country,
                'type': 'amendment_approved',
                'amendment_id': amendment.id,
                'clause_id': clause.id
            })
        else:
            db.session.commit()

        # Emit status change
        socketio.emit('amendment_status_changed', {
            'id': amendment.id,
            'committee': amendment.committee,
            'is_published': False,
            'is_passed': True,
            'country': amendment.country
        })

        return jsonify({'message': 'Amendment approved successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/committee/<committee>/current-clause', methods=['PUT'])
def update_current_clause(committee):
    try:
        data = request.get_json()
        clause = Clause.query.filter_by(
            committee=committee.lower(),
            is_published=True
        ).first_or_404()

        # Keep original content intact
        original_content = clause.html_content  # No longer modified
        
        # Update amendment status and content
        if 'amendment_id' in data:
            amendment = Amendment.query.get(data['amendment_id'])
            if amendment:
                amendment.is_published = True
                amendment.under_debate = True
                amendment.debate_clause_id = clause.id
                amendment.amended_clause = data['content']  # Store amendment content here
                db.session.add(amendment)
        
        db.session.commit()

        socketio.emit('amendment_under_debate', {
            'clause_id': clause.id,
            'amendment_id': data.get('amendment_id'),
            'original_content': original_content,  # Original remains unchanged
            'amended_content': data['content'],     # Get amended content from request
            'committee': committee,
            'country': clause.country
        })
        return jsonify({'message': 'Amendment published successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/amendments/<int:amendment_id>/unpublish', methods=['POST'])
def unpublish_amendment(amendment_id):
    try:
        amendment = Amendment.query.get_or_404(amendment_id)
        clause = Clause.query.get(amendment.debate_clause_id)
        
        # Store IDs for socket emission before clearing
        committee = amendment.committee
        debate_clause_id = amendment.debate_clause_id
        
        # Revert clause status
        if clause:
            clause.is_amended = False
            # Revert to original clause content
            original_clause = Clause.query.get(amendment.clause_id)
            if original_clause:
                clause.html_content = original_clause.html_content
                db.session.add(clause)
        
        # Clear amendment debate status
        amendment.under_debate = False
        amendment.debate_clause_id = None
        amendment.is_published = False
        db.session.commit()

        # Emit socket events
        socketio.emit('amendment_unpublished', {
            'committee': committee,
            'amendment_id': amendment_id,
            'clause_id': debate_clause_id,
            'original_content': original_clause.html_content if original_clause else ''
        })
        
        return jsonify({'message': 'Amendment unpublished and changes reverted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/amendments/<int:amendment_id>/update-amended-clause', methods=['POST'])
def update_amended_clause(amendment_id):
    try:
        data = request.get_json()
        amended_clause = data.get('amended_clause')
        
        if not amended_clause:
            return jsonify({'error': 'Amended clause content is required'}), 400
            
        amendment = Amendment.query.get_or_404(amendment_id)
        amendment.amended_clause = amended_clause
        db.session.commit()
        
        return jsonify({'message': 'Amendment updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/amendments/<int:amendment_id>', methods=['GET'])
def get_amendment(amendment_id):
    try:
        amendment = Amendment.query.get_or_404(amendment_id)
        
        amendment_data = {
            'id': amendment.id,
            'amendment_text': amendment.amendment_text,
            'amended_clause': amendment.amended_clause,
            'country': amendment.country,
            'committee': amendment.committee,
            'clause_id': amendment.clause_id,
            'timestamp': amendment.timestamp.isoformat(),
            'is_published': amendment.is_published,
            'is_rejected': amendment.is_rejected,
            'is_passed': amendment.is_passed,
            'under_debate': amendment.under_debate,
            'debate_clause_id': amendment.debate_clause_id
        }
        
        return jsonify(amendment_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/amendments/<int:amendment_id>/finalize', methods=['POST'])
def finalize_amendment(amendment_id):
    try:
        amendment = Amendment.query.get_or_404(amendment_id)
        data = request.get_json()
        clause = Clause.query.get(amendment.debate_clause_id)
        
        if data.get('approved'):
            # Permanently update the original clause
            clause.html_content = amendment.amended_clause
            amendment.is_passed = True
            # Remove debate relationship
            amendment.debate_clause_id = None
        else:
            amendment.is_rejected = True

        # Cleanup statuses
        clause.is_amended = False
        amendment.under_debate = False
        amendment.is_published = False
        db.session.commit()
        
        socketio.emit('amendment_resolved', {
            'amendment_id': amendment_id,
            'approved': data.get('approved'),
            'new_content': clause.html_content,
            'committee': amendment.committee
        })
        
        return jsonify({'message': 'Amendment finalized successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    try:
        message = Message.query.get_or_404(message_id)
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# DeepSeek formatting endpoint
@app.route('/clause/<int:clause_id>/format-with-deepseek', methods=['POST'])
def format_with_deepseek(clause_id):
    try:
        clause = Clause.query.get_or_404(clause_id)
        
        # This endpoint just validates that the clause exists
        # The actual API call is handled by the stream_format endpoint
        # This is done to properly handle streaming responses
        
        return jsonify({
            'success': True,
            'message': 'Formatting initiated',
            'clause_id': clause_id
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Stream response from DeepSeek API
@app.route('/clause/<int:clause_id>/stream-format', methods=['GET'])
def stream_format(clause_id):
    def generate():
        try:
            clause = Clause.query.get_or_404(clause_id)
            
            # Get the HTML content to format
            html_content = clause.html_content
            
            # Format the instruction for DeepSeek
            instruction = """
            Please reformat the following HTML content to use proper clause styling:
            - First level: number (1, 2, 3, ...)
            - Second level: small letters (a, b, c, ...)
            - Third level: small roman numerals (i, ii, iii, ...)
            - Fourth level: capital letters (A, B, C, ...)
            
            Maintain all original content and meaning, but structure it properly with the specified formatting.
            Return just the formatted HTML that I can directly use, with no explanations or markdown.
            """
            
            # DeepSeek API endpoint
            deepseek_api_url = "https://api.deepseek.com/v1/chat/completions"
            
            # DeepSeek API key - in production, use environment variables
            api_key = os.environ.get("DEEPSEEK_API_KEY", "sk-519079ea9b144723a1c62c2bcb98202c")
            
            # Prepare the request payload
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are an assistant that formats document clauses with proper styling."},
                    {"role": "user", "content": f"{instruction}\n\n{html_content}"}
                ],
                "stream": True
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            # Make the actual API call to DeepSeek with streaming
            response = requests.post(deepseek_api_url, json=payload, headers=headers, stream=True)
            
            if response.status_code != 200:
                yield f"data: {json.dumps({'error': f'DeepSeek API error: {response.status_code} - {response.text}'})}\n\n"
                return
            
            formatted_content = ""
            for line in response.iter_lines():
                if line:
                    # Process the streaming response from DeepSeek
                    line_text = line.decode('utf-8')
                    if line_text.startswith('data: '):
                        try:
                            json_str = line_text[6:]  # Remove 'data: ' prefix
                            if json_str.strip() == '[DONE]':
                                # End of stream
                                yield f"data: {json.dumps({'done': True})}\n\n"
                                break
                                
                            data = json.loads(json_str)
                            
                            # Extract the content chunk from the response
                            if 'choices' in data and len(data['choices']) > 0:
                                choice = data['choices'][0]
                                if 'delta' in choice and 'content' in choice['delta']:
                                    chunk = choice['delta']['content']
                                    
                                    # Filter out markdown code block delimiters and standalone "html" text
                                    if chunk.strip().startswith('```html') or chunk.strip().startswith('```'):
                                        # Skip this chunk as it's just a markdown delimiter
                                        continue
                                    if chunk.strip() == '```':
                                        # Skip closing markdown delimiter
                                        continue
                                    if chunk.strip().lower() == 'html' and formatted_content == '':
                                        # Skip standalone "html" text at the beginning
                                        continue
                                    
                                    formatted_content += chunk
                                    yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                        except json.JSONDecodeError as e:
                            yield f"data: {json.dumps({'error': f'JSON parse error: {str(e)}'})}\n\n"
                
            # Clean any remaining markdown delimiters from the final content
            if formatted_content:
                # Remove opening markdown delimiter
                formatted_content = formatted_content.replace('```html', '')
                formatted_content = formatted_content.replace('```', '')
                # Remove standalone "html" at the beginning if present
                formatted_content = re.sub(r'^\s*html\s*', '', formatted_content, flags=re.IGNORECASE)
                # Trim any whitespace
                formatted_content = formatted_content.strip()
                
                yield f"data: {json.dumps({'final_content': formatted_content})}\n\n"
                
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

# Endpoint to update clause content with formatted text
@app.route('/clause/<int:clause_id>/update-content', methods=['POST'])
def update_clause_content(clause_id):
    try:
        data = request.get_json()
        formatted_content = data.get('formatted_content')
        
        if not formatted_content:
            return jsonify({'error': 'Formatted content is required'}), 400
            
        clause = Clause.query.get_or_404(clause_id)
        clause.html_content = formatted_content
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Clause content updated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=8000,debug=True)
