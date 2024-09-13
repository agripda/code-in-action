# database_setup.py
# This script sets up the database and populates it with some sample data.

from app import db
from models import Hotel

# Drop all tables and create them
db.drop_all()
db.create_all()

# Add some sample data
hotels = [
    Hotel(name='Hotel One', city='City A', street='Street 1'),
    Hotel(name='Hotel Two', city='City B', street='Street 2'),
    Hotel(name='Hotel Three', city='City A', street='Street 3')
]

for hotel in hotels:
    db.session.add(hotel)
db.session.commit()