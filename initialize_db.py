import sys
import os

# Add the vehicle_rental_system directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'vehicle_rental_system')))

from models.database import Base, engine

try:
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
except Exception as e:
    print(f"An error occurred during database initialization: {e}")
