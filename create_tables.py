from market import app, db  # Ensure this imports the correct app and db instances

# Create the tables in the database
with app.app_context():
    db.create_all()
    print("Tables created successfully!")
