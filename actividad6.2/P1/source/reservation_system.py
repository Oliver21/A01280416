import sys
from abc import ABC, abstractmethod
import json
import os


# Archivos json para almacenar la información de los clientes, hoteles y reservas
CUSTOMERS_FILE = "customers.json"
HOTELS_FILE = "hotels.json"
RESERVATIONS_FILE = "reservations.json"



#Clase abstracta para definir la estructura de las clases de clientes, hoteles y reservas
class Entity(ABC):
    @abstractmethod
    def create(self, *args):
        pass

    @abstractmethod
    def load_data(self):
        pass

class CustomerError(Exception):
    pass

class ReservationError(Exception):
    pass

class HotelError(Exception):
    pass





#Clase para crear clientes
class Customer(Entity):

    def __init__(self, customer_id, name, email, birthday, phone):
        self.id = customer_id
        self.name = name
        self.email = email
        self.birthday = birthday
        self.phone = phone

    def load_data(self):
        return load_json_file(CUSTOMERS_FILE)
        
    def _save_customers(customers):
        with open(CUSTOMERS_FILE, "w") as file:
            json.dump(customers, file, indent=4)

    @classmethod
    def create(cls, customer):
        customers = cls.load_data()

        # Validar que no exista ID duplicado
        if any(c["id"] == customer.id for c in customers):
            raise CustomerError(
                f"Customer with id {customer.id} already exists"
            )

        customers.append(customer.to_dict())
        cls._save_customers(customers)


    @classmethod
    def get_customer(cls, customer_id):
        customers = cls._load_customers()
        for c in customers:
            if c["id"] == customer_id:
                return c

        raise CustomerError(
            f"Customer with id {customer_id} not found"
        )

    @classmethod
    def delete_customer(cls, customer_id):
        customers = cls._load_customers()

        if not any(c["id"] == customer_id for c in customers):
            raise CustomerError(
                f"Customer with id {customer_id} not found"
            )

        customers = [c for c in customers if c["id"] != customer_id]
        cls._save_customers(customers)

    @classmethod
    def modify_customer(cls, customer_id, **kwargs):
        customers = cls._load_customers()
        found = False

        for c in customers:
            if c["id"] == customer_id:
                c.update(kwargs)
                found = True

        if not found:
            raise CustomerError(
                f"Customer with id {customer_id} not found"
            )

        cls._save_customers(customers)









#Clase para crear hoteles
class Hotel(Entity):

    def __init__(self, hotel_id, name, location, total_rooms):
        self.id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.available_rooms = total_rooms

    @staticmethod
    def load_data():
        return load_json_file(HOTELS_FILE)

    @staticmethod
    def _save_hotels(hotels):
        with open(HOTELS_FILE, "w") as file:
            json.dump(hotels, file, indent=4)


    def create(cls, hotel):
        hotels = cls._load_hotels()
        hotels.append(hotel.to_dict())
        cls._save_hotels(hotels)
        
    

    @classmethod
    def get_hotel(cls, hotel_id):
        hotels = cls.load_data()
        for h in hotels:
            if h["id"] == hotel_id:
                return h
        raise HotelError(f"Hotel with id {hotel_id} not found")

    @classmethod
    def delete_hotel(cls, hotel_id):
        hotels = cls.load_data()
        if not any(h["id"] == hotel_id for h in hotels):
            raise HotelError(f"Hotel with id {hotel_id} not found")

        hotels = [h for h in hotels if h["id"] != hotel_id]
        cls._save_hotels(hotels)

    @classmethod
    def modify_hotel(cls, hotel_id, **kwargs):
        hotels = cls.load_data()
        found = False

        for h in hotels:
            if h["id"] == hotel_id:
                h.update(kwargs)
                found = True

        if not found:
            raise HotelError(f"Hotel with id {hotel_id} not found")

        cls._save_hotels(hotels)


    def reserve_room(self, customer_id, check_in_date, check_out_date):
        if self.available_rooms <= 0:
            print("No rooms available.")
            return

        reservation_id = f"{self.id}_{customer_id}_{check_in_date}_{check_out_date}"
        reservation = {
            "id": reservation_id,
            "customer_email": Customer.get_customer(customer_id)["email"],
            "hotel_name": self.name,
            "room": self.total_rooms - self.available_rooms + 1,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "status": "active"
        }
        reservations = Reservations._load_reservations()
        reservations.append(reservation)
        Reservations._save_reservations(reservations)

    
    def cancel_reservation(self, reservation_id):
        reservations = Reservations._load_reservations()
        found = False

        for r in reservations:
            if r["id"] == reservation_id:
                r["status"] = "cancelled"
                found = True

        if not found:
            raise ReservationError(
                f"Reservation with id {reservation_id} not found"
            )

        Reservations._save_reservations(reservations)
        self.available_rooms += 1




#Clase para crear reservas
class Reservations(Entity):

    def __init__(self, reservation_id, hotel_id, customer_id, room_number):
        self.id = reservation_id
        self.hotel_id = hotel_id
        self.customer_id = customer_id
        self.room_number = room_number
        self.status = "active"

    @staticmethod
    def load_data():
        return load_json_file(RESERVATIONS_FILE)

    @staticmethod
    def _save_reservations(reservations):
        with open(RESERVATIONS_FILE, "w") as file:
            json.dump(reservations, file, indent=4)


    def create(cls, reservation):

        # Validar hotel
        hotel = Hotel.get_hotel(reservation.hotel_id)

        # Validar customer
        Customer.get_customer(reservation.customer_id)

        # Validar disponibilidad
        if hotel["available_rooms"] <= 0:
            raise ReservationError("No rooms available")

        reservations = cls._load_reservations()
        reservations.append(reservation.to_dict())
        cls._save_reservations(reservations)

        Hotel.modify_hotel(
            reservation.hotel_id,
            available_rooms=hotel["available_rooms"] - 1
        )
    
    @classmethod
    def cancel_reservation(cls, reservation_id):
        reservations = cls.load_data()
        found = False

        for r in reservations:
            if r["id"] == reservation_id:
                r["status"] = "cancelled"
                found = True

        if not found:
            raise ReservationError(
                f"Reservation with id {reservation_id} not found"
            )

        cls._save_reservations(reservations)







# Funcion para leer un archivo json
def load_json_file(filepath):
    """
    Función para cargar un archivo JSON
    """
    if not os.path.exists(filepath):
            return []
    with open(filepath, "r") as file:
        return json.load(file)


def main():
    """
    Función principal
    """





if __name__ == "__main__":
    main()