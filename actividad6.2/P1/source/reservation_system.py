import sys


#Creamos los diccionarios para almacenar la informacion de los clientes y las reservas
customers_dict = {}
reservations_dict = {}
hotels_dict = {}


#Clase para crear clientes
class Customers:
    def create(email, name, birthdate, phone):
        customers_dict[email] = {
            "name": name,
            "birthdate": birthdate,
            "phone": phone
        }
        print(f"Customer '{name}' created successfully.")

    def display_info(email):
        customer = customers_dict.get(email)
        if customer:
            print(f"Customer Name: {customer['name']}")
            print(f"Email: {email}")
            print(f"Birthdate: {customer['birthdate']}")
            print(f"Phone: {customer['phone']}")
        else:
            print("Customer not found.")

#Clase para crear hoteles
class Hotels:
    def create(name, location, price_per_night):
        hotels_dict[name] = {
            "location": location,
            "price_per_night": price_per_night
        }
        print(f"Hotel '{name}' created successfully.")

    def display_info(name):
        hotel = hotels_dict.get(name)
        if hotel:
            print(f"Hotel Name: {name}")
            print(f"Location: {hotel['location']}")
            print(f"Price per Night: ${hotel['price_per_night']}")
        else:
            print("Hotel not found.")

#Clase para crear reservas
class Reservations:
    def create(customer_email, hotel_name, check_in_date, check_out_date):
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
            "check_in_date": check_in_date,
            "check_out_date": check_out_date
        }
        print(f"Reservation '{reservation_id}' created successfully.")

    def display_info(reservation_id):
        reservation = reservations_dict.get(reservation_id)
        if reservation:
            print(f"Reservation ID: {reservation_id}")
            print(f"Customer Email: {reservation['customer_email']}")
            print(f"Hotel Name: {reservation['hotel_name']}")
            print(f"Check-in Date: {reservation['check_in_date']}")
            print(f"Check-out Date: {reservation['check_out_date']}")
        else:
            print("Reservation not found.")

    


def main():
    """
    Función principal
    """


if __name__ == "__main__":
    main()