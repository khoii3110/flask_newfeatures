from market import app, db
from market.models import User, Item

with app.app_context():
    # Create a user
    user = User(username='test_user', email_address='test@example.com', password_hash='hashed_password')
    db.session.add(user)
    db.session.commit()

    # Create an item
    item = Item(name='Test Item', price=100, barcode='123456789012', description='This is a test item', owner=user)
    db.session.add(item)
    db.session.commit()

    print("Test user and item added!")





