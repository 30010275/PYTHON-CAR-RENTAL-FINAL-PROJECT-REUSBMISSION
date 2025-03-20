def validate_vehicle_data(vehicle_type, vehicle_brand):
    # This function checks if the vehicle data is valid. 
    # Just a simple check for now, but hey, it works!
    if not vehicle_type or not vehicle_brand:
        print("❌ Missing vehicle type or brand!")
        return False
    return True

def handle_error(err):
    # Oops! Something went wrong. Let's handle it.
    print(f"❌ An error occurred: {err}. Please try again later.")
    # Maybe log it somewhere? Just a thought.
