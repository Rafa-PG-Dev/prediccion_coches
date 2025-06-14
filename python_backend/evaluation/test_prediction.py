import pickle
import pandas as pd
import xgboost as xgb

# Cargar el modelo y los encoders
try:
    with open('assets/model.pkl', 'rb') as f:
        model = pickle.load(f)

    with open('assets/encoder_make_model.pkl', 'rb') as f:
        encoder_make_model = pickle.load(f)

    with open('assets/encoder_fuel_shift.pkl', 'rb') as f:
        encoder_fuel_shift = pickle.load(f)

except Exception as e:
    print(f"Error al cargar los archivos: {e}")
    model, encoder_make_model, encoder_fuel_shift = None, None, None

# Características categóricas y numéricas
categorical_features = ['make', 'model', 'fuel', 'shift']
numeric_features = ['year', 'kms', 'power', 'doors']

# Datos de prueba (un coche con ciertos datos)
test_data = {
    "make": "bmw",
    "model": "x5",
    "fuel": "gasoline",
    "year": 2015,
    "kms": 80000,
    "power": 120,
    "doors": 4,
    "shift": "manual"
}

# Procedimiento similar al que haces en la API
df_input = pd.DataFrame([test_data])

# Codificar las características categóricas
X_encoded_make_model = encoder_make_model.transform(df_input[['make', 'model']])
encoded_columns_make_model = encoder_make_model.get_feature_names_out(['make', 'model'])
X_encoded_df_make_model = pd.DataFrame(X_encoded_make_model, columns=encoded_columns_make_model)

X_encoded_fuel_shift = encoder_fuel_shift.transform(df_input[['fuel', 'shift']])
encoded_columns_fuel_shift = encoder_fuel_shift.get_feature_names_out(['fuel', 'shift'])
X_encoded_df_fuel_shift = pd.DataFrame(X_encoded_fuel_shift, columns=encoded_columns_fuel_shift)

# Depuración: Imprime las características codificadas para ver cómo están transformándose
print("Características codificadas para make y model:")
print(X_encoded_df_make_model)

print("Características codificadas para fuel y shift:")
print(X_encoded_df_fuel_shift)

# Concatenar las columnas codificadas con las numéricas
final_input = pd.concat([ 
    df_input[numeric_features].reset_index(drop=True),
    X_encoded_df_make_model.reset_index(drop=True),
    X_encoded_df_fuel_shift.reset_index(drop=True)
], axis=1)

# Imprimir los datos finales que serán ingresados al modelo
print("Datos finales para la predicción:")
print(final_input)

# Convertir a DMatrix para XGBoost
dtest = xgb.DMatrix(final_input)

# Realizar la predicción
prediction = model.predict(dtest)

# Convertir la predicción a un valor flotante y redondear
predicted_price = round(float(prediction[0]), 2)

# Imprimir el resultado redondeado
print(f"Predicción para el coche de prueba: {predicted_price}")
