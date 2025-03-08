from models import db  # Importing the db object from your app
from models import Delegate, Group, Chair, delegate_group, Message, File, Amendment  # Import the models
from datetime import datetime  # Import datetime to get current time for the message

def initialize_database():
    # Ensure all tables are created
    db.create_all()

    # Clear existing data if any (optional, for testing purposes)
    db.session.query(delegate_group).delete()
    db.session.query(Delegate).delete()
    db.session.query(Group).delete()
    db.session.query(Chair).delete()  # Also clear Chair data if it exists
    db.session.query(Message).delete()
    db.session.query(File).delete()
    db.session.query(Amendment).delete()
    # Commit the deletions
    db.session.commit()

    # Step 1: Create the "gossip" group first
    gossip_group = Group(name='gossip')

    # Step 2: Create other groups
    junior_group = Group(name='junior')
    senior_group = Group(name='senior')
    security_council_group = Group(name='security council')

    # Step 3: Add the groups to the session
    db.session.add_all([gossip_group, junior_group, senior_group, security_council_group])
    db.session.commit()

    # Step 4: Create a single Chair instance for all committees
    chair = Chair(username='admin_chair', password='password123')

    # Add Chair instance to the session
    db.session.add(chair)
    db.session.commit()

    # Step 5: Create Chair delegates for each committee
    committees = ['junior', 'senior', 'security council']  # Removed 'gossip'
    chair_delegates = []
    
    for committee in committees:
        chair_delegate = Delegate(name=f'{committee.title()} Chair', country='Chair', committee=committee)
        chair_delegates.append(chair_delegate)

    # Add Chair delegates to the session
    db.session.add_all(chair_delegates)
    db.session.commit()

    # Step 6: Create regular delegates for each committee
    junior_delegates = [
        Delegate(name='Alice Junior', country='USA', committee='junior'),
        Delegate(name='Bob Junior', country='UK', committee='junior'),
        Delegate(name='Charlie Junior', country='Canada', committee='junior')
    ]

    senior_delegates = [
        Delegate(name='David Senior', country='Germany', committee='senior'),
        Delegate(name='Eve Senior', country='France', committee='senior'),
        Delegate(name='Frank Senior', country='Japan', committee='senior')
    ]

    security_council_delegates = [
        Delegate(name='Grace SC', country='Russia', committee='security council'),
        Delegate(name='Hank SC', country='China', committee='security council'),
        Delegate(name='Ivy SC', country='India', committee='security council')
    ]

    # Step 7: Add all regular delegates to the session
    all_delegates = junior_delegates + senior_delegates + security_council_delegates
    db.session.add_all(all_delegates)
    db.session.commit()

    # Step 8: Add regular delegates and Chair delegate to their respective groups
    junior_group.delegates.extend(junior_delegates + [chair_delegates[0]])
    senior_group.delegates.extend(senior_delegates + [chair_delegates[1]])
    security_council_group.delegates.extend(security_council_delegates + [chair_delegates[2]])

    # Step 9: Add all regular delegates to the "gossip" group (no chair)
    gossip_group.delegates.extend(all_delegates)  # Removed chair delegate

    # Commit changes to the database
    db.session.commit()

    # Step 10: Add a message to the "gossip" group saying it cannot be deleted
    try:
        gossip_message = Message(
            text='You can send your gossip to this group, and it cannot be deleted.',
            sender_id=chair_delegates[0].id,  # Use the Junior Chair as the sender instead of gossip chair
            group_id=gossip_group.id,
            timestamp=datetime.now().strftime("%H:%M"),  # Current time as 'HH:MM'
            date=datetime.now().strftime("%Y-%m-%d"),  # Current date as 'YYYY-MM-DD'
        )
        db.session.add(gossip_message)
        db.session.commit()
        print("Gossip group message added.")
    except Exception as e:
        print(f"Failed to add gossip message: {e}")

    # Add welcome messages to each committee group
    try:
        # Current timestamp and date for all messages
        current_time = datetime.now().strftime("%H:%M")
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Junior committee welcome message
        junior_message = Message(
            text='Welcome to the Junior Committee group chat. Here you can communicate with all delegates in your committee.',
            sender_id=chair_delegates[0].id,  # Junior Chair
            group_id=junior_group.id,
            timestamp=current_time,
            date=current_date,
        )
        db.session.add(junior_message)
        
        # Senior committee welcome message
        senior_message = Message(
            text='Welcome to the Senior Committee group chat. Here you can communicate with all delegates in your committee.',
            sender_id=chair_delegates[1].id,  # Senior Chair
            group_id=senior_group.id,
            timestamp=current_time,
            date=current_date,
        )
        db.session.add(senior_message)
        
        # Security Council welcome message
        security_council_message = Message(
            text='Welcome to the Security Council group chat. Here you can communicate with all delegates in your committee.',
            sender_id=chair_delegates[2].id,  # Security Council Chair
            group_id=security_council_group.id,
            timestamp=current_time,
            date=current_date,
        )
        db.session.add(security_council_message)
        
        db.session.commit()
        print("Committee welcome messages added.")
    except Exception as e:
        print(f"Failed to add committee welcome messages: {e}")

    print("Database initialized with groups, delegates, chair, and messages.")

    # Ensure this runs successfully
    gossip_group = Group(name='gossip')  # This should get ID=1

if __name__ == '__main__':
    from app import app
    with app.app_context():
        initialize_database()
