"""
Docstring para actividad5.2
P1 Compute Sales
Autor: Oliver Alejandro Martínez Quiroz
"""


# Imports
import sys
import time
import json


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

    # Leer el nombre del archivo desde la línea de comandos
    file_name_catalogue = sys.argv[1]
    file_name_sales = sys.argv[2]
    lines = []

    print("Catalogue file: ", file_name_catalogue)
    print("Sales file: ", file_name_sales)
    print("Reading files...\n")
    start_time = time.perf_counter()

    catalogue = load_json_file(f"../tests/{file_name_catalogue}")
    sales = load_json_file(f"../tests/{file_name_sales}")

    # Creamos un diccionario con la información del catálogo
    # para facilitar la búsqueda de precios
    catalogue_dict = {product['title']: product['price']
                      for product in catalogue}

    # Recorrer las ventas y calcular el total de ventas
    total_sales = 0

    for sale in sales:
        product_sale = sale['Product']
        quantity = sale['Quantity']

        if product_sale in catalogue_dict:
            total_sales += catalogue_dict[product_sale] * quantity
            lines.append(
                f"{product_sale}\n"
                f"Unit Price: ${catalogue_dict[product_sale]}\n"
                f"Quantity: {quantity}\n"
                f"Total: ${catalogue_dict[product_sale] * quantity}\n"
            )
        else:
            lines.append(
                f"{product_sale}\n"
                f"PRODUCT NOT FOUND IN CATALOGUE\n"
                f"Quantity: {quantity}\n"
                )

    end_time = time.perf_counter()

    lines.append("-----------------------")
    lines.append(f"Total Sales: ${total_sales:,.2f}")
    lines.append("-----------------------\n")
    lines.append(f"Execution Time: {end_time - start_time:.6f} seconds")

    # Definir el nombre del archivo de resultados
    archivo_salida = '../results/SalesResults_' + (
        file_name_sales.replace('.json', '.txt'))

    # Escribir las líneas en un archivo de resultados
    with open(archivo_salida, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")
    file.close()

    print(
        f"Detailed information file: {archivo_salida}\n"
        f"-----------------------\n"
        f"Total Sales: ${total_sales:,.2f}\n"
        f"-----------------------\n"
        f"Execution Time: {end_time - start_time:.6f} seconds\n"
    )


if __name__ == "__main__":
    main()
