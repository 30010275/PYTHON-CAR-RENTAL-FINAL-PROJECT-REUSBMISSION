from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.vehicle import Vehicle
from models.rental import Rental

def listAvailableVehicles():  
    # Let's see what rides we have available!
    db = SessionLocal()
    vehicles = db.query(Vehicle).all()
    db.close()
    
    vehicle_list = []
    for vehicle in vehicles:
        # Is this vehicle ready to roll?
        rental_status = "Available" if vehicle.available else "Not Available (Rented)"
        vehicle_list.append(f"{vehicle.id}: {vehicle.brand} ({vehicle.vehicle_type}) - Status: {rental_status}")
    
    return vehicle_list

def addVehicle(vehicle_type, vehicle_brand, vehicle_year, vehicle_color):
    db = SessionLocal()
    vehicle = Vehicle.create(vehicle_type=vehicle_type, brand=vehicle_brand)  # Updated to use vehicle_type
    db.close()
    return vehicle  # Vehicle added successfully, right?
