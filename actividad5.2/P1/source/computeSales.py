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
    lines = []

    print("Catalogue file: ", file_name_catalogue)
    print("Sales file: ", file_name_sales)
    print("Reading files...")

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



    lines.append("-----------------------")
    lines.append(f"Total Sales: ${total_sales:,.2f}")
    lines.append("-----------------------\n")

    #Definir el nombre del archivo de resultados
    archivo_salida = '../results/SalesResults_' + file_name_sales.replace('.json', '.txt')

    # Escribir las líneas en un archivo de resultados
    with open(archivo_salida, "w", encoding="utf-8") as file:
        for line in lines:
            print(line)
            file.write(line + "\n")
    file.close()



if __name__ == "__main__":
    main()