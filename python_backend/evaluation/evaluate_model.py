import pandas as pd
import pickle
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os
import xgboost as xgb
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
from sklearn.model_selection import train_test_split

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

# Convertir X_test a DMatrix
dtest = xgb.DMatrix(X_test)

# Realizar predicciones con el modelo cargado
y_pred = model.predict(dtest)

# Evaluación general
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"📉 MAE: {mae:.2f}")
print(f"📉 MSE: {mse:.2f}")
print(f"📈 R² Score: {r2:.4f}")

# ===============================
# 5. Evaluación por marca
# ===============================
# Añadir la columna 'make' a X_test para evaluar el error por marca
X_test['make'] = X.loc[X_test.index, 'make']
X_test['error_abs'] = abs(y_pred - y_test.values)

# Calcular el MAE por marca
mae_by_make = X_test.groupby('make')['error_abs'].mean()

# Mostrar el MAE por marca
print("📊 MAE por marca:")
print(mae_by_make)

# Definir umbral de MAE alto para marcas que requieren evaluación adicional
MAE_THRESHOLD = 8000
high_error_brands = mae_by_make[mae_by_make > MAE_THRESHOLD].index.tolist()

print(f"\n🧠 Marcas con error alto ({MAE_THRESHOLD}): {high_error_brands}")

# ===============================
# 6. Guardar resultados de evaluación
# ===============================
os.makedirs('assets/evaluation_results', exist_ok=True)

# Guardar los resultados generales de la evaluación
with open('assets/evaluation_results/general_evaluation.txt', 'w') as f:
    f.write(f"📉 MAE: {mae:.2f}\n")
    f.write(f"📉 MSE: {mse:.2f}\n")
    f.write(f"📈 R² Score: {r2:.4f}\n")

# Guardar los MAE por marca
mae_by_make.to_csv('assets/evaluation_results/mae_by_make.csv')

# Guardar las marcas con error alto
with open('assets/evaluation_results/high_error_brands.txt', 'w') as f:
    f.write("\n".join(high_error_brands))

print("✅ Resultados de evaluación guardados correctamente.")
