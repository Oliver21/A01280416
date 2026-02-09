"""
Docstring para actividad4.2
P2 Convert Numbers
Autor: Oliver Alejandro Martínez Quiroz
"""

#Imports
import sys
import time

def main():
    """
    Función principal
    """
    file_name = sys.argv[1]
    filepath = '../tests/' + file_name
    bits = 10
    bitshex = 40

    #Creamos la lista de líneas para el archivo de salida, incluyendo el encabezado
    lines = [ f"{'ITEM':<6}{'Number':<12}{'BIN':<12}{'HEX':<8}" ]


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
                    number = int(line)
                    binary = format(number & (2**bits - 1), "b")
                    hexadecimal = format(number & (2**bitshex - 1), "10X")
                    lines.append(f"{len(lines):<6}{number:<12}{binary:<12}{hexadecimal:<8}")
                except ValueError:
                    number = line
                    lines.append(f"{len(lines):<6}{number:<12}{"#VALUE!":<12}{"#VALUE!":<8}")
                    continue
        #with open(filepath, 'r') as file:
        #    numbers = [float(line.strip()) for line in file if line.strip().isdigit()]
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    lines.append(f"Execution time: {elapsed_time:.6f} seconds")


    #Guardamos los resultados en un archivo de salida
    archivo_salida = '../results/ConvertionResults_' + file_name

    with open(archivo_salida, "w", encoding="utf-8") as f:
        for line in lines:
            print(line)
            f.write(line + "\n")
    f.close()

if __name__ == "__main__":
    main()
