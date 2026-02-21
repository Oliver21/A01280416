import sys
from abc import ABC, abstractmethod


#Creamos los diccionarios para almacenar la informacion de los clientes y las reservas
customers_dict = {}
reservations_dict = {}
hotels_dict = {}


#Clase abstracta para definir la estructura de las clases de clientes, hoteles y reservas
class Entity(ABC):
    @abstractmethod
    def create(self, *args):
        pass

    @abstractmethod
    def display_info(self):
        pass


#Clase para crear clientes
class Customers(Entity):

    def create(self, email, name, birthdate, phone):
        self.email = email

        customers_dict[self.email] = {
            "name": name,
            "birthdate": birthdate,
            "phone": phone
        }
        print(f"Customer '{name}' created successfully.")

    def display_info(self):
        customer = customers_dict.get(self.email)
        if customer:
            print(f"Customer Name: {customer['name']}")
            print(f"Email: {self.email}")
            print(f"Birthdate: {customer['birthdate']}")
            print(f"Phone: {customer['phone']}")
        else:
            print("Customer not found.")

    def modify_customer(self, new_name=None, new_birthdate=None, new_phone=None):
        customer = customers_dict.get(self.email)
        if customer:
            if new_name:
                customer['name'] = new_name
            if new_birthdate:
                customer['birthdate'] = new_birthdate
            if new_phone:
                customer['phone'] = new_phone
            print(f"Customer '{self.email}' modified successfully.")
        else:
            print("Customer not found.")
    
    def delete(self):
        if self.email in customers_dict:
            del customers_dict[self.email]
            print(f"Customer '{self.email}' deleted successfully.")
        else:
            print("Customer not found.")


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



    


def main():
    """
    Función principal
    """


if __name__ == "__main__":
    main()