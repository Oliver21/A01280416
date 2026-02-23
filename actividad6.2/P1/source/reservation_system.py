import sys
from abc import ABC, abstractmethod
import json
import os
import unittest


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
    def load_data():
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

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def load_data():
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
        customers = cls.load_data()
        for c in customers:
            if c["id"] == customer_id:
                return c

        raise CustomerError(
            f"Customer with id {customer_id} not found"
        )

    @classmethod
    def delete_customer(cls, customer_id):
        customers = cls.load_data()

        if not any(c["id"] == customer_id for c in customers):
            raise CustomerError(
                f"Customer with id {customer_id} not found"
            )

        customers = [c for c in customers if c["id"] != customer_id]
        cls._save_customers(customers)

    @classmethod
    def modify_customer(cls, customer_id, **kwargs):
        customers = cls.load_data()
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

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def load_data():
        return load_json_file(HOTELS_FILE)

    @staticmethod
    def _save_hotels(hotels):
        with open(HOTELS_FILE, "w") as file:
            json.dump(hotels, file, indent=4)

    @classmethod
    def create(cls, hotel):
        hotels = cls.load_data()
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
        reservations = Reservation.load_data()
        reservations.append(reservation)
        Reservation._save_reservations(reservations)

    
    def cancel_reservation(self, reservation_id):
        reservations = Reservation.load_data()
        found = False

        for r in reservations:
            if r["id"] == reservation_id:
                r["status"] = "cancelled"
                found = True

        if not found:
            raise ReservationError(
                f"Reservation with id {reservation_id} not found"
            )

        Reservation._save_reservations(reservations)
        self.available_rooms += 1




#Clase para crear reservas
class Reservation(Entity):

    def __init__(self, reservation_id, hotel_id, customer_id, room_number):
        self.id = reservation_id
        self.hotel_id = hotel_id
        self.customer_id = customer_id
        self.room_number = room_number
        self.status = "active"

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def load_data():
        return load_json_file(RESERVATIONS_FILE)

    @staticmethod
    def _save_reservations(reservations):
        with open(RESERVATIONS_FILE, "w") as file:
            json.dump(reservations, file, indent=4)

    @classmethod
    def create(cls, reservation):

        # Validar hotel
        hotel = Hotel.get_hotel(reservation.hotel_id)

        # Validar customer
        Customer.get_customer(reservation.customer_id)

        # Validar disponibilidad
        if hotel["available_rooms"] <= 0:
            raise ReservationError("No rooms available")

        reservations = cls.load_data()
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


class TestHotelSystem(unittest.TestCase):

    def setUp(self):
        # Limpiar archivos antes de cada prueba
        for file in [HOTELS_FILE, CUSTOMERS_FILE, RESERVATIONS_FILE]:
            with open(file, "w") as f:
                json.dump([], f)

        # Crear varios hoteles, clientes y reservas para las pruebas
        self.hotel = Hotel (1, "Hotel California", "Los Angeles", 10)
        Hotel.create(self.hotel)


        self.customer = Customer(1, "Oliver", "oliver@mail.com", "1990-01-01", "1234567890")
        Customer.create(self.customer)

        self.reservation = Reservation(1, 1, 1, 101)
        Reservation.create(self.reservation)

    # ------------------------
    # HOTEL TESTS
    # ------------------------

    #def test_delete_hotel(self):
        #Hotel.delete_hotel(1)
        #self.assertIsNone(Hotel.get_hotel(1))

    def test_delete_non_existing_hotel(self):
        Hotel.delete_hotel(999)
        self.assertIsNone(Hotel.get_hotel(999))

    # ------------------------
    # CUSTOMER TESTS
    # ------------------------

    def test_delete_customer(self):
        Customer.delete_customer(1)
        self.assertIsNone(Customer.get_customer(1))

    def test_delete_non_existing_customer(self):
        Customer.delete_customer(999)
        self.assertIsNone(Customer.get_customer(999))

    # ------------------------
    # RESERVATION TESTS
    # ------------------------

    def test_cancel_reservation(self):
        Reservation.cancel_reservation(1)

        with open(RESERVATIONS_FILE, "r") as f:
            reservations = json.load(f)

        self.assertEqual(reservations[0]["status"], "cancelled")

    def test_cancel_non_existing_reservation(self):
        Reservation.cancel_reservation(999)

        with open(RESERVATIONS_FILE, "r") as f:
            reservations = json.load(f)

        # La reserva original debe seguir activa
        self.assertEqual(reservations[0]["status"], "active")

    # ------------------------
    # NEGATIVE TESTS
    # ------------------------

    def test_get_non_existing_hotel(self):
        self.assertIsNone(Hotel.get_hotel(999))

    def test_get_non_existing_customer(self):
        self.assertIsNone(Customer.get_customer(999))

    def test_reservation_without_hotel(self):
        bad_reservation = Reservation(2, 999, 1, 102)
        Reservation.create(bad_reservation)

        with open(RESERVATIONS_FILE, "r") as f:
            reservations = json.load(f)

        # Se creó la reserva aunque el hotel no exista (falla lógica)
        self.assertEqual(len(reservations), 2)

    def tearDown(self):
        # Limpiar después de cada prueba
        for file in [HOTELS_FILE, CUSTOMERS_FILE, RESERVATIONS_FILE]:
            with open(file, "w") as f:
                json.dump([], f)






if __name__ == "__main__":
    unittest.main()