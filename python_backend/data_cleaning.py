import pandas as pd

def clean_data(file_path, output_path):
    """
    Función para limpiar los datos del archivo CSV de coches.

    Parámetros:
    - file_path: ruta del archivo CSV de entrada.
    - output_path: ruta para guardar el archivo CSV limpio.
    """
    # Cargar CSV
    df = pd.read_csv(file_path)

    # Eliminar columnas innecesarias
    columns_to_drop = [
        'url', 'company', 'version', 'price_financed', 'dealer', 
        'publish_date', 'insert_date', 'photos', 'is_professional', 'country', 
        'color', 'province'
    ]
    df = df.drop(columns=columns_to_drop, errors='ignore')

    # Eliminar filas con valores nulos en las columnas clave
    df = df.dropna(subset=['price', 'year', 'kms', 'power', 'doors', 'make'])

    # Convertir columnas a tipo numérico (esto puede generar valores NaN si no es posible convertir)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['kms'] = pd.to_numeric(df['kms'], errors='coerce')
    df['power'] = pd.to_numeric(df['power'], errors='coerce')
    df['doors'] = pd.to_numeric(df['doors'], errors='coerce')

    # Filtrar filas con valores fuera de rango
    df = df[df['price'] > 0]  # Eliminar precios negativos o cero
    df = df[df['year'] > 1990]  # Eliminar coches más antiguos que 1990
    df = df[df['kms'] < 1_000_000]  # Limitar los kilómetros a menos de 1 millón
    df = df[df['power'] > 0]  # Eliminar coches sin potencia (0 o menos)
    df = df[df['doors'] > 0]  # Eliminar coches con número de puertas inválido

    # Guardar el DataFrame limpio en el archivo de salida
    df.to_csv(output_path, index=False)
    print(f"✅ CSV limpio guardado en: {output_path}")

# Limpiar los datos y crear el archivo coches_data_cleaned.csv
clean_data('assets/coches_data.csv', 'assets/coches_data_cleaned.csv')
