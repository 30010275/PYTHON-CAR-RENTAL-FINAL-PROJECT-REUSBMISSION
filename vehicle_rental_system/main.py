from models.database import Base, engine, SessionLocal  # Import SessionLocal
from models.vehicle import Vehicle
from models.rental import Rental
from services.vehicle_service import addVehicle  # Import the addVehicle function
from colorama import Fore, Style, init
from sqlalchemy.orm import joinedload  # Import joinedload
from services.rental_service import rentThisVehicle  # Import the rentThisVehicle function

init(autoreset=True)

# database tables
Base.metadata.create_all(bind=engine)

def listRentedVehicles():
    rented_vehicles = Rental.list_all_rentals()  # Let's grab all the rented vehicles, shall we?
    if rented_vehicles:
        print("\n🚗 Rented Vehicles 📋 Let's see what's out!")
        for rental in rented_vehicles:
            vehicle = Vehicle.find_by_id(rental.vehicle_id)  # Load vehicle explicitly
            if not vehicle:
                print("❌ Rental record not found.")
                return
            print(f"{rental.id}: {vehicle.brand} ({vehicle.vehicle_type}) - Rented by {rental.renter_name} on {rental.rental_date}. Cool, right?")


    else:
        print("✅ No vehicles are currently rented. Bummer!")

def listAvailableVehicles():
    available_vehicles = Vehicle.list_all()  # Let's check out the available rides!
    if available_vehicles:
        print("\n🚗 Available Vehicles 📋 Here are the rides you can take!")
        for vehicle in available_vehicles:
            print(f"{vehicle.id}: {vehicle.brand} ({vehicle.vehicle_type}) - Available: {vehicle.available}")
    else:
        print("✅ No vehicles are currently available. Guess we’re all booked!")

def handleRentVehicle():
    vehicle_id = input("Enter the vehicle ID to rent: Let's get you a ride! ")
    try:
        vehicle_id = int(vehicle_id)  # Convert to integer
    except ValueError:
        print("❌ Oops! Invalid vehicle ID. Please enter a valid number, okay?")
        return
    renter_name = input("Enter your name: ")
    is_vip = input("Are you a VIP customer? (yes/no): Just curious! ").strip().lower() == 'yes'
    
    rental = rentThisVehicle(vehicle_id, renter_name, is_vip)  #
    if rental is None:
        print("❌ Rental failed. Double-check the vehicle ID and availability, please!")
        return
    rental.vehicle = Vehicle.find_by_id(rental.vehicle_id)  # Load vehicle explicitly
    if rental:
        print(f"✅ Awesome! Successfully rented {rental.vehicle.brand} ({rental.vehicle.vehicle_type}) to {renter_name}. Enjoy your ride!")
    else:
        print("❌ Rental failed. Please check the vehicle ID and availability.")

def returnVehicle():
    rental_id = input("Enter the rental ID to return: Let's get that vehicle back! ")
    try:
        rental_id = int(rental_id)  # Convert to integer
    except ValueError:
        print("❌ Yikes! Invalid rental ID. Please enter a valid number.")
        return
    rental_hours = input("Enter the number of hours the vehicle was rented: How long did you have it? ")
    try:
        rental_hours = int(rental_hours)  # Convert to integer
    except ValueError:
        print("❌ Invalid number of hours. Please enter a valid number, please!")
        return
    
    db = SessionLocal()  # Create a new session
    rental = db.query(Rental).options(joinedload(Rental.vehicle)).filter_by(id=rental_id).first()  # Eager load vehicle
    if rental:
        total_cost = rental.return_vehicle(rental_hours)  # Call return_vehicle on rental
        vehicle = Vehicle.find_by_id(rental.vehicle_id)  # Load vehicle explicitly
        print(f"✅ Successfully returned {vehicle.brand} ({vehicle.vehicle_type}). Total cost: ${total_cost}. Thanks for bringing it back!")
    else:
        print("❌ Rental record not found. Did you enter the right ID?")
    db.close()

def main():
    while True:
        print(Fore.BLUE + "Welcome to inno_lyrico Vehicle Rental System! Buckle up!" + Style.RESET_ALL)
        
        print("1. Add Vehicle - ")
        print("2. List Vehicles - Check out what's available!")
        print("3. Rent Vehicle - Ready to hit the road?")
        print("4. Return Vehicle - Time to bring it back!")
        print("5. List Rented Vehicles - See what's out there!")  
        print("00. Exit - Until next time!")

        choice = input("Select an option: ")
        if choice == "1":
            vehicle_type = input("Enter the vehicle type. e.g. 'Car', 'Motorcycle', 'Truck': ")
            vehicle_brand = input("Enter the vehicle brand: ")
            vehicle_year_of_manufacturer = input("Enter the vehicle year of manufacturer: ")
            vehicle_color = input("Enter the vehicle color: ")
            if addVehicle(vehicle_type, vehicle_brand, vehicle_year_of_manufacturer, vehicle_color):
                print("✅ Vehicle added successfully! Nice choice!")
        elif choice == "2":
            listAvailableVehicles()  # Call the new function
        elif choice == "3":
            handleRentVehicle()  # Call the handleRentVehicle function
        elif choice == "4":
            returnVehicle()  # Call the returnVehicle function
        elif choice == "5":
            listRentedVehicles()  # Call function
        elif choice == "00":
            print("👋 Goodbye Welcome Back Again!")
            break
        else:
            print("❌ Invalid choice. Try again!")

if __name__ == "__main__":
    main()
