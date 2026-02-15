"""
Docstring para actividad5.2
P1 Compute Sales
Autor: Oliver Alejandro Martínez Quiroz
"""


#Imports
import sys
import time
import json

def main():
    """
    Función principal
    """

    #Leer el nombre del archivo desde la línea de comandos
    file_name_catalogue = sys.argv[1]
    file_name_sales = sys.argv[2]
    filepath_catalogue = '../tests/' + file_name_catalogue
    filepath_sales = '../tests/' + file_name_sales

    print("Reading files...")
    print("Catalogue file: ", filepath_catalogue)
    print("Sales file: ", filepath_sales)

    #leer el catálogo de productos
    with open (filepath_catalogue, 'r', encoding="utf-8") as file:
        data = json.load(file)

    #leer las ventas
    with open (filepath_sales, 'r', encoding="utf-8") as file:
        sales = json.load(file)
    

    #Recorrer las ventas y calcular el total de ventas
    total_sales = 0

    for sale in sales:
        product_sale = sale['Product']
        quantity = sale['Quantity']
        for product in data:
            if product['title'] == product_sale:
                total_sales += product['price'] * quantity

    print(f"Total Sales: {total_sales}")


if __name__ == "__main__":
    main()