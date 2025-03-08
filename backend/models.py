# models.py

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import base64
from flask_bcrypt import Bcrypt
# Initialize database and Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

# Define the Amendment model
class Amendment(db.Model):
    __tablename__ = 'amendments'
    id = db.Column(db.Integer, primary_key=True)
    amendment_text = db.Column(db.Text, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    committee = db.Column(db.String(100), nullable=False)
    clause_id = db.Column(db.Integer, db.ForeignKey('clause.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    is_rejected = db.Column(db.Boolean, default=False)
    is_passed = db.Column(db.Boolean, default=False)
    amended_clause = db.Column(db.Text, default='')  # New field for amended clause content
    under_debate = db.Column(db.Boolean, default=False)
    debate_clause_id = db.Column(db.Integer, db.ForeignKey('clause.id'), nullable=True)

    def __repr__(self):
        return f'<Amendment {self.id} by {self.country}>'

# Define the Chair model
class Chair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column('password', db.String(120), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is not readable!")

    @password.setter
    def password(self, password):
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self._password, password)


# Define the DelegateGroup association table
delegate_group = db.Table('delegate_group',
    db.Column('delegate_id', db.Integer, db.ForeignKey('delegate.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

# Define the Delegate model
class Delegate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    committee = db.Column(db.String(80), nullable=False)
    
    # Many-to-many relationship with Group
    groups = db.relationship('Group', secondary=delegate_group, backref=db.backref('delegates', lazy=True))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'committee': self.committee,
            'groups': [group.name for group in self.groups]  # To see which groups the delegate is part of
        }

# Define the Group model
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    messages = db.relationship('Message', backref='group', lazy=True)
    index = db.Column(db.String(80), nullable=True)
    unreadCount = db.Column(db.Integer, default=0)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'delegates': [{"id": delegate.id, "name": delegate.name} for delegate in self.delegates],  # To see which delegates are in the group
            'index': self.index,
            'unreadCount': self.unreadCount,
            'lastMessage': self.messages[-1].serialize() if self.messages else None,
        }


# Define the Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=True)  # Nullable to allow messages with only files
    sender_id = db.Column(db.Integer, db.ForeignKey('delegate.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    
    # These fields will now accept data from the frontend
    timestamp = db.Column(db.String(5), nullable=False)  # Expected format 'HH:MM'
    date = db.Column(db.String(10), nullable=False)      # Expected format 'YYYY-MM-DD'

    # Define the relationship for the sender
    sender = db.relationship('Delegate', backref='messages', lazy=True)

    # Establish a one-to-many relationship with the File model
    files = db.relationship('File', backref='message', lazy=True, cascade="all, delete-orphan")

    def serialize(self):
        return {
            'id': self.id,
            '_id': str(self.id),  # Add _id for frontend compatibility
            'text': self.text,
            'content': self.text,  # Add content for frontend compatibility
            'sender_id': self.sender_id,
            'senderId': str(self.sender_id),  # Add senderId for frontend compatibility
            'group_id': self.group_id,
            'username': self.sender.name,
            'timestamp': self.timestamp,  # Already formatted
            'date': self.date,          # Already formatted
            'files': [file.serialize() for file in self.files]  # Serialize associated files
        }

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)  # Foreign key to Message
    name = db.Column(db.String(255), nullable=False)  # Original file name
    size = db.Column(db.Integer, nullable=False)      # File size in bytes
    type = db.Column(db.String(50), nullable=False)   # File MIME type (e.g., 'image/png')
    path = db.Column(db.String(255), nullable=False)  # Path to the stored file

    def serialize(self):
        # Check if the file type is an image
        if self.type.startswith('image/'):
            # Read the file and convert it to Base64
            try:
                with open(self.path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    # Include the Base64 data in the preview
                    preview_data = f"data:{self.type};base64,{encoded_string}"
            except FileNotFoundError:
                preview_data = None
        else:
            # If not an image, set preview to None
            preview_data = None
        
        return {
            'name': self.name,
            'size': self.size,
            'type': self.type,
            'url': f"http://localhost:8000/{self.path}",   # Construct URL for file download
            'preview': preview_data,  # Include Base64 data if it's an image, else None
        }

# Define the Clause model
class Clause(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    committee = db.Column(db.String(50))
    country = db.Column(db.String(100))
    filename = db.Column(db.String(255))
    html_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    is_rejected = db.Column(db.Boolean, default=False)
    is_passed = db.Column(db.Boolean, default=False)
    amendments = db.relationship(
        'Amendment', 
        backref='clause', 
        lazy=True,
        foreign_keys='Amendment.clause_id'  # Specify which foreign key to use
    )
    is_amended = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            'id': self.id,
            'committee': self.committee,
            'country': self.country,
            'filename': self.filename,
            'content': self.html_content,
            'is_published': self.is_published,
            'is_amended': self.is_amended,
            'timestamp': self.timestamp.isoformat(),
        }

# Define the UnreadCount model to track unread messages per user and group
class UnreadCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('delegate.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    count = db.Column(db.Integer, default=0)
    last_read_message_id = db.Column(db.Integer, nullable=True)
    
    # Define relationships
    user = db.relationship('Delegate', backref='unread_counts')
    group = db.relationship('Group', backref='unread_counts')
    
    # Add unique constraint to ensure one record per user-group pair
    __table_args__ = (db.UniqueConstraint('user_id', 'group_id'),)
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'group_id': self.group_id,
            'count': self.count,
            'last_read_message_id': self.last_read_message_id
        }