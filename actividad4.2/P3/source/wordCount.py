"""
Docstring para actividad4.2
P3 Word Count
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
    words  = []
    lines = []

    #Leemos los números del archivo, asegurándonos de convertirlos a float y
    # omitiendo líneas vacías o no numéricas
    try:
        with open(filepath, 'r', encoding="utf-8") as file:
            start_time = time.perf_counter()
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    words.append(line)
                except ValueError:
                    continue


    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)

    #Obtenemos el total de palabras
    total_words = len(words)


    #Creamos un diccionario para contar la frecuencia de cada palabra
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1


    #Ordenamo el diccionario por mayor frecuencia a menor frecuencia
    word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))

    #Hacemos un append al array de salida con el resultado de cada palabra y su frecuencia
    for word, count in word_count.items():
        lines.append(f"{word}: {count}")



    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    #Agregamos el total de palabras y el tiempo de ejecución al array de salida
    lines.append(f"Total de palabras: {total_words}")
    lines.append(f"Tiempo de ejecución: {elapsed_time:.6f} segundos")


    #Guardamos los resultados en un archivo de salida
    archivo_salida = '../results/WordCountResults_' + file_name

    with open(archivo_salida, "w", encoding="utf-8") as f:
        for line in lines:
            print(line)
            f.write(line + "\n")
    f.close()

if __name__ == "__main__":
    main()
