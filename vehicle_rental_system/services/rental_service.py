from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.vehicle import Vehicle
from models.rental import Rental

def rentThisVehicle(vehicle_id, renter_name, is_vip):
    db = SessionLocal()
    vehicle = Vehicle.find_by_id(vehicle_id)
    
    if not vehicle or not vehicle.available:
        db.close()
        print("Rental failed. Please check the vehicle ID and availability.")
        return None  # Vehicle is not available for rent

    rental_cost = vehicle.calculate_rental_cost(is_vip)  # Calculate rental cost
    vehicle.available = False  # Mark vehicle as rented
    rental = Rental.create(renter_name, vehicle, rental_cost)  # Create rental record
    db.commit()
    db.close()
    print(f"Successfully rented {vehicle.brand} ({vehicle.vehicle_type}) to {renter_name}.")  # Updated line

    return rental
