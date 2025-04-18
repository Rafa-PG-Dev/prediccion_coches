import csv
import json
import os
from collections import defaultdict

# Ruta de entrada y salida
csv_path = "assets/coches_data_cleaned.csv"  # Ruta del CSV con los datos de los coches
output_path = os.path.join("assets", "coches_por_marca.json")  # Ruta donde guardaremos el JSON resultante

# Diccionario para agrupar los modelos por marca
coches_por_marca = defaultdict(set)

# Leer el archivo CSV
with open(csv_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)  # Leer el CSV como diccionario
    for row in reader:
        marca = row["make"].strip().upper()  # Obtener la marca del coche, convertirla a mayúsculas
        modelo = row["model"].strip()  # Obtener el modelo del coche
        coches_por_marca[marca].add(modelo)  # Agrupar por marca y modelo en un set

# Convertir los sets en listas y ordenarlas alfabéticamente
coches_por_marca = {marca: sorted(list(modelos)) for marca, modelos in coches_por_marca.items()}

# Crear la carpeta 'assets' si no existe
os.makedirs("assets", exist_ok=True)

# Guardar el diccionario como un archivo JSON
with open(output_path, mode="w", encoding="utf-8") as json_file:
    json.dump(coches_por_marca, json_file, indent=4, ensure_ascii=False)  # Guardamos con indentación de 4 y caracteres no ASCII permitidos

print(f"Archivo JSON creado correctamente en: {output_path}")
