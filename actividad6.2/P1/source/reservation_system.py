import sys
from abc import ABC, abstractmethod
import json
import os

#Creamos los diccionarios para almacenar la informacion de los clientes y las reservas
customers_dict = {}
reservations_dict = {}
hotels_dict = {}


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
    def display_info(self):
        pass

class CustomerError(Exception):
    pass

#Clase para crear clientes
class Customers(Entity):

    def __init__(self, customer_id, name, email, birthday, phone):
        self.id = customer_id
        self.name = name
        self.email = email
        self.birthday = birthday
        self.phone = phone

    def _load_customers():
        if not os.path.exists(CUSTOMERS_FILE):
            return []
        with open(CUSTOMERS_FILE, "r") as file:
            return json.load(file)
        
    def _save_customers(customers):
        with open(CUSTOMERS_FILE, "w") as file:
            json.dump(customers, file, indent=4)

    @classmethod
    def create(cls, customer):
        customers = cls._load_customers()

        # Validar que no exista ID duplicado
        if any(c["id"] == customer.id for c in customers):
            raise CustomerError(
                f"Customer with id {customer.id} already exists"
            )

        customers.append(customer.to_dict())
        cls._save_customers(customers)

    def display_info(self):
        customer = customers_dict.get(self.email)
        if customer:
            print(f"Customer Name: {customer['name']}")
            print(f"Email: {self.email}")
            print(f"Birthdate: {customer['birthdate']}")
            print(f"Phone: {customer['phone']}")
        else:
            print("Customer not found.")

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
class Hotels(Entity):

    def create(self, name, location, price_per_night):
        self.name = name

        hotels_dict[name] = {
            "location": location,
            "price_per_night": price_per_night
        }
        print(f"Hotel '{name}' created successfully.")

    def display_info(self):
        hotel = hotels_dict.get(self.name)
        if hotel:
            print(f"Hotel Name: {self.name}")
            print(f"Location: {hotel['location']}")
            print(f"Price per Night: ${hotel['price_per_night']}")
        else:
            print("Hotel not found.")

    def delete(self):
        if self.name in hotels_dict:
            del hotels_dict[self.name]
            print(f"Hotel '{self.name}' deleted successfully.")
        else:
            print("Hotel not found.")
    
    def modify_hotel(self, new_location=None, new_price_per_night=None):
        hotel = hotels_dict.get(self.name)
        if hotel:
            if new_location:
                hotel['location'] = new_location
            if new_price_per_night:
                hotel['price_per_night'] = new_price_per_night
            print(f"Hotel '{self.name}' modified successfully.")
        else:
            print("Hotel not found.")

    def reserve_room(self, customer_email, room, check_in_date, check_out_date):
        if customer_email not in customers_dict:
            print("Customer not found. Please create the customer first.")
            return

        reservation_id = len(reservations_dict) + 1
        reservations_dict[reservation_id] = {
            "customer_email": customer_email,
            "hotel_name": self.name,
            "room": room,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date
        }
        print(f"Room reserved successfully for customer '{customer_email}' at hotel '{self.name}' from {check_in_date} to {check_out_date}.")

    def cancel_reservation(self, reservation_id):
        if reservation_id in reservations_dict:
            del reservations_dict[reservation_id]
            print(f"Reservation '{reservation_id}' cancelled successfully.")
        else:
            print("Reservation not found.")

#Clase para crear reservas
class Reservations(Entity):
    def create(self, customer_email, hotel_name, room, check_in_date, check_out_date):
        if customer_email not in customers_dict:
            print("Customer not found. Please create the customer first.")
            return
        if hotel_name not in hotels_dict:
            print("Hotel not found. Please create the hotel first.")
            return

        reservation_id = len(reservations_dict) + 1
        reservations_dict[reservation_id] = {
            "customer_email": customer_email,
            "hotel_name": hotel_name,
            "room": room,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date
        }
        print(f"Reservation '{reservation_id}' created successfully.")

        self.reservation_id = reservation_id

    def display_info(self):
        reservation = reservations_dict.get(self.reservation_id)
        if reservation:
            print(f"Reservation ID: {self.reservation_id}")
            print(f"Customer Email: {reservation['customer_email']}")
            print(f"Hotel Name: {reservation['hotel_name']}")
            print(f"Room: {reservation['room']}")
            print(f"Check-in Date: {reservation['check_in_date']}")
            print(f"Check-out Date: {reservation['check_out_date']}")
        else:
            print("Reservation not found.")
    
    def cancel_reservation(self):
        if self.reservation_id in reservations_dict:
            del reservations_dict[self.reservation_id]
            print(f"Reservation '{self.reservation_id}' cancelled successfully.")
        else:
            print("Reservation not found.")




# Funcion para leer un archivo json
def load_json_file(filepath):
    """
    Función para cargar un archivo JSON
    """
    try:
        with open(filepath, 'r', encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file '{filepath}'.")
        return None


def main():
    """
    Función principal
    """





if __name__ == "__main__":
    main()