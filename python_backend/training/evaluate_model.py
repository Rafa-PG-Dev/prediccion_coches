import pandas as pd
import pickle
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# ===============================
# 1. Cargar el modelo y encoders
# ===============================
with open('assets/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('assets/encoder_make_model.pkl', 'rb') as f:
    encoder_make_model = pickle.load(f)

with open('assets/encoder_fuel_shift.pkl', 'rb') as f:
    encoder_fuel_shift = pickle.load(f)

# ===============================
# 2. Cargar los datos originales
# ===============================
df = pd.read_csv('assets/coches_data_cleaned.csv')

X = df[['make', 'model', 'fuel', 'year', 'kms', 'power', 'doors', 'shift']]
y = df['price']

# ===============================
# 3. Aplicar los mismos encoders
# ===============================
X_encoded_make_model = encoder_make_model.transform(X[['make', 'model']])
X_encoded_fuel_shift = encoder_fuel_shift.transform(X[['fuel', 'shift']])

# Convertir a DataFrames
X_encoded_df_make_model = pd.DataFrame(X_encoded_make_model, columns=encoder_make_model.get_feature_names_out(['make', 'model']))
X_encoded_df_fuel_shift = pd.DataFrame(X_encoded_fuel_shift, columns=encoder_fuel_shift.get_feature_names_out(['fuel', 'shift']))

# Concatenar con columnas numéricas
X_final = pd.concat([
    X[['year', 'kms', 'power', 'doors']].reset_index(drop=True),
    X_encoded_df_make_model.reset_index(drop=True),
    X_encoded_df_fuel_shift.reset_index(drop=True)
], axis=1)

# ===============================
# 4. Evaluar el modelo
# ===============================
# Puedes dividir aquí si quieres evaluar con train/test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"📉 MSE: {mse:.2f}")
print(f"📈 R² Score: {r2:.4f}")
