from market import app, db  # Import your app instance
from market.models import Item  # Import the Item model

# List of items to add with barcode
items_to_add = [
    {"name": "Laptop", "price": 800, "description": "A high-performance laptop", "barcode": "123456789012"},
    {"name": "Phone", "price": 500, "description": "A smartphone with a great camera", "barcode": "234567890123"},
    {"name": "Tablet", "price": 300, "description": "A tablet for daily tasks", "barcode": "345678901234"},
    {"name": "Headphones", "price": 150, "description": "Wireless noise-canceling headphones", "barcode": "456789012345"},
    {"name": "Smartwatch", "price": 200, "description": "A smartwatch with fitness tracking", "barcode": "567890123456"},
    {"name": "Gaming Console", "price": 400, "description": "A next-gen gaming console", "barcode": "678901234567"},
    {"name": "Bluetooth Speaker", "price": 120, "description": "Portable Bluetooth speaker", "barcode": "789012345678"},
    {"name": "Monitor", "price": 250, "description": "4K UHD monitor", "barcode": "890123456789"},
    {"name": "Keyboard", "price": 60, "description": "Mechanical RGB keyboard", "barcode": "901234567890"},
    {"name": "Mouse", "price": 40, "description": "Wireless ergonomic mouse", "barcode": "012345678901"},
    {"name": "External Hard Drive", "price": 100, "description": "1TB external storage", "barcode": "123456789013"},
    {"name": "Camera", "price": 600, "description": "DSLR camera for high-quality photography", "barcode": "234567890124"},
    {"name": "E-reader", "price": 120, "description": "E-reader with backlight and large storage", "barcode": "345678901235"},
    {"name": "Projector", "price": 350, "description": "HD projector for home theater", "barcode": "456789012356"},
    {"name": "Smart Home Hub", "price": 180, "description": "Control smart home devices", "barcode": "567890123467"}
]

# Seed function
def seed_items():
    with app.app_context():  # Set up the application context
        for item in items_to_add:
            new_item = Item(
                name=item["name"],
                price=item["price"],
                description=item["description"],
                barcode=item["barcode"]  # Include barcode
            )
            db.session.add(new_item)
        db.session.commit()
        print("Data added successfully!")

# Run the function
seed_items()
