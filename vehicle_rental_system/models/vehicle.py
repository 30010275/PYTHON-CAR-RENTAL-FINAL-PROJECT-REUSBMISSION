from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .database import Base, SessionLocal

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    available = Column(Boolean, default=True)

    rentals = relationship("Rental", back_populates="vehicle")  # Use string reference to avoid circular import

    @classmethod
    def create(cls, type, brand):
        db = SessionLocal()
        vehicle = cls(type=type, brand=brand)
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        db.close()
        return vehicle

    @classmethod
    def list_all(cls):
        db = SessionLocal()
        vehicles = db.query(cls).filter_by(available=True).all()
        db.close()
        return vehicles

    @classmethod
    def find_by_id(cls, vehicle_id):
        db = SessionLocal()
        vehicle = db.query(cls).filter_by(id=vehicle_id).first()
        db.close()
        return vehicle

    def rent(self, renter_name, is_vip=False):
        rental_cost = self.calculate_rental_cost(is_vip)  # Calculate rental cost
        db = SessionLocal()  # Define db session here
        if not self.available:
            print("❌ Vehicle is already rented.")
            db.close()  # Ensure to close the session
            return None

        self.available = False
        if not self.available:
            print("❌ Vehicle is already rented.")
            return None
        rental = Rental.create(renter_name, self, rental_cost)  # Pass rental cost to Rental
        db.commit()
        db.close()
        return rental

    def calculate_rental_cost(self, is_vip=False):
        base_cost = 100  # Base cost for rental
        if is_vip:
            return base_cost * 0.9  # 10% discount for VIP customers
        return base_cost

    def return_vehicle(self, rental_id, rental_hours): 
        self.available = True  # Mark vehicle as available
        db = SessionLocal()
        rental = db.query(Rental).filter_by(id=rental_id, return_date=None).first()
        if not rental:
            print("❌ Rental record not found.")
            db.close()
            return None
        
        total_cost = rental.return_vehicle(rental_hours)
        db.commit()
        db.close()
        return total_cost
