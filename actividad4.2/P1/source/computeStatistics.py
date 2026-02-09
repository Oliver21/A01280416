"""
Docstring para actividad4.2
P1 Compute Statistics
Autor: Oliver Alejandro Martínez Quiroz
"""

#Imports
import sys
import time

def main():
    """
    Función principal
    """
    
    #Leemos el nombre del archivo desde la línea de comandos
    file_name = sys.argv[1]
    filepath = '../tests/' + file_name
    numbers = []

    #Leemos los números del archivo, asegurándonos de convertirlos a float y omitiendo
    # líneas vacías o no numéricas
    try:
        with open(filepath, 'r', encoding="utf-8") as file:
            start_time = time.perf_counter()
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    numbers.append(float(line))
                except ValueError:
                    continue
        #with open(filepath, 'r') as file:
        #    numbers = [float(line.strip()) for line in file if line.strip().isdigit()]
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)

    #Ordenamos los números de menor a mayor
    numbers.sort()

    #Calculamos la mediana
    cantidad = len(numbers)
    print(f"Cantidad de números: {cantidad}")
    if cantidad % 2 == 1:
        median = numbers[cantidad // 2]
    else:
        median = (numbers[cantidad // 2 - 1] + numbers[cantidad // 2]) / 2


    #Obtenemos el número de elementos, la suma, el promedio, el valor máximo y el valor mínimo
    total_sum = sum(numbers)
    mean = total_sum / cantidad if cantidad > 0 else 0

    #Calculamos la moda
    moda = max(set(numbers), key=numbers.count)

    varianza = sum((x - mean) ** 2 for x in numbers) / (len(numbers) - 1)
    desviacion_estandar = varianza ** 0.5

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    lines = [
        "Statistics:",
        f"Count: {cantidad}",
        f"Mean: {mean}",
        f"Median: {median}",
        f"Mode: {moda}",
        f"Standard Deviation: {desviacion_estandar}",
        f"Variance: {varianza}",
        f"Execution time: {elapsed_time:.6f} seconds"
    ]


    #Guardamos los resultados en un archivo de salida
    archivo_salida = '../results/StatisticsResults_' + file_name

    with open(archivo_salida, "w", encoding="utf-8") as f:
        for line in lines:
            print(line)
            f.write(line + "\n")
    f.close()

if __name__ == "__main__":
    main()
