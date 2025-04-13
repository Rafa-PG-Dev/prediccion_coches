import pandas as pd

def clean_data(file_path, output_path):
    # Cargar CSV
    df = pd.read_csv(file_path)

    # Eliminar columnas innecesarias
    columns_to_drop = ['url', 'company', 'version', 'price_financed', 'dealer', 'publish_date', 'insert_date']
    df = df.drop(columns=columns_to_drop, errors='ignore')

    # Eliminar filas con valores nulos en columnas clave
    df = df.dropna(subset=['price', 'year', 'kms', 'power', 'doors', 'make', 'color'])

    # Convertir columnas a tipo numérico
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['kms'] = pd.to_numeric(df['kms'], errors='coerce')
    df['power'] = pd.to_numeric(df['power'], errors='coerce')
    df['doors'] = pd.to_numeric(df['doors'], errors='coerce')

    # Filtrar valores fuera de rango
    df = df[df['price'] > 0]
    df = df[df['year'] > 1990]
    df = df[df['kms'] < 1_000_000]
    df = df[df['power'] > 0]
    df = df[df['doors'] > 0]

    # Guardar CSV limpio
    df.to_csv(output_path, index=False)
    print(f"✅ CSV limpio guardado en: {output_path}")

# Ejecutar
clean_data('assets/coches_data.csv', 'assets/data_cleaned.csv')
