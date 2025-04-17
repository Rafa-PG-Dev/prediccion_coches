import csv
import json
import os
from collections import defaultdict

# Ruta de entrada y salida
csv_path = "assets/coches_data_cleaned.csv"  
output_path = os.path.join("assets", "coches_por_marca.json")

# Diccionario para agrupar modelos por marca
coches_por_marca = defaultdict(set)

# Leer CSV y agrupar modelos
with open(csv_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        marca = row["make"].strip().upper()
        modelo = row["model"].strip()
        coches_por_marca[marca].add(modelo)

# Convertir sets en listas y ordenar
coches_por_marca = {marca: sorted(list(modelos)) for marca, modelos in coches_por_marca.items()}

# Crear carpeta si no existe
os.makedirs("assets", exist_ok=True)

# Guardar como JSON
with open(output_path, mode="w", encoding="utf-8") as json_file:
    json.dump(coches_por_marca, json_file, indent=4, ensure_ascii=False)

print(f"Archivo JSON creado correctamente en: {output_path}")
