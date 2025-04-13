import pickle
import pandas as pd
import numpy as np

# Cargar modelo y encoder
with open('assets/model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('assets/encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

# Ejemplo JSON recibido desde Postman
input_data = {
    "make": "citroen",
    "model": "c4",
    "fuel": "diesel",
    "year": 2018,
    "kms": 50000,
    "power": 150,
    "doors": 4,
    "shift": "automatico",
    "color": "negro",
    "is_professional": True,
    "province": "madrid"
}

# Convertir a DataFrame
df_input = pd.DataFrame([input_data])

# Codificar columnas categóricas
categorical_features = ['make', 'model', 'fuel', 'shift', 'color', 'province']
encoded_input = encoder.transform(df_input[categorical_features])
encoded_columns = encoder.get_feature_names_out(categorical_features)
encoded_df = pd.DataFrame(encoded_input, columns=encoded_columns)

# Concatenar columnas numéricas
numeric_features = ['year', 'kms', 'power', 'doors', 'is_professional']
final_input = pd.concat([
    encoded_df.reset_index(drop=True),
    df_input[numeric_features].reset_index(drop=True)
], axis=1)

# Predecir
prediction = model.predict(final_input)
print(f"✅ Precio estimado: {prediction[0]:,.2f} €")
