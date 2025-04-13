import pandas as pd
import pickle
from sklearn.preprocessing import OneHotEncoder

# Cargar el modelo entrenado y el encoder
with open('assets/model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('assets/encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

# Definir las categorías posibles de 'fuel' y 'shift' según el entrenamiento
fuel_categories = ['Petrol', 'Diesel', 'Electric', 'Hybrid']  # Ajusta según las categorías utilizadas en el entrenamiento
shift_categories = ['Manual', 'Automatic']  # Ajusta según las categorías utilizadas en el entrenamiento

# Función para predecir el precio de un coche
def predict_price(input_data):
    # Convertir input_data a un DataFrame
    input_df = pd.DataFrame([input_data], columns=['make', 'model', 'fuel', 'year', 'kms', 'power', 'doors', 'shift'])

    # Asegurarse de que las columnas 'make' y 'model' están en el encoder si es necesario
    categorical_columns = ['make', 'model', 'fuel', 'shift']
    
    # Codificar las columnas categóricas (incluyendo make y model si es necesario)
    X_encoded = encoder.transform(input_df[categorical_columns])

    # Crear DataFrame con columnas codificadas
    encoded_columns = encoder.get_feature_names_out(categorical_columns)
    X_encoded_df = pd.DataFrame(X_encoded, columns=encoded_columns)

    # Concatenar con columnas numéricas (sin 'is_professional')
    X_final = pd.concat([input_df[['year', 'kms', 'power', 'doors']].reset_index(drop=True),
                         X_encoded_df.reset_index(drop=True)], axis=1)

    # Asegurarse de que las columnas estén en el mismo orden que las columnas del modelo
    final_column_order = encoder.get_feature_names_out(categorical_columns).tolist() + ['year', 'kms', 'power', 'doors']
    X_final = X_final[final_column_order]

    # Predecir el precio
    predicted_price = model.predict(X_final)[0]

    return predicted_price

# Ejemplo de uso
input_data = {
    'make': 'BMW',
    'model': 'X5',
    'fuel': 'Diesel',
    'year': 2020,
    'kms': 50000,
    'power': 250,
    'doors': 5,
    'shift': 'Automatic'
}

# Obtener el precio estimado
predicted_price = predict_price(input_data)
print(f"💰 Precio estimado: {predicted_price:.2f} €")
