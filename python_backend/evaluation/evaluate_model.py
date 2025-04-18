import pandas as pd
import pickle
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import os

# ===============================
# 1. Cargar el modelo y los encoders
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
# 5. Visualizar los resultados
# ===============================

# Gráfico de la distribución de los errores
plt.figure(figsize=(10, 6))
errors = y_pred - y_test
sns.histplot(errors, kde=True, color='blue', bins=30)
plt.title('Distribución de los Errores de Predicción')
plt.xlabel('Error de Predicción')
plt.ylabel('Frecuencia')
plt.grid(True)
plt.show()

# Gráfico de los precios reales vs los predichos
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.6, color='purple')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', lw=2)  # Línea de igualdad
plt.title('Precio Real vs Precio Predicho')
plt.xlabel('Precio Real')
plt.ylabel('Precio Predicho')
plt.grid(True)
plt.show()

# Gráfico de error absoluto por marca
X_test['make'] = X.loc[X_test.index, 'make']
X_test['error_abs'] = abs(y_pred - y_test.values)

mae_by_make = X_test.groupby('make')['error_abs'].mean().sort_values()

plt.figure(figsize=(12, 8))
mae_by_make.plot(kind='barh', color='salmon')
plt.title('Error Absoluto Medio (MAE) por Marca')
plt.xlabel('MAE')
plt.ylabel('Marca')
plt.grid(True)
plt.show()

# ===============================
# 6. Guardar los resultados gráficos
# ===============================
os.makedirs('assets/evaluation_results', exist_ok=True)

# Guardar los gráficos generados
plt.figure(figsize=(10, 6))
sns.histplot(errors, kde=True, color='blue', bins=30)
plt.title('Distribución de los Errores de Predicción')
plt.xlabel('Error de Predicción')
plt.ylabel('Frecuencia')
plt.grid(True)
plt.savefig('assets/evaluation_results/error_distribution.png')

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.6, color='purple')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', lw=2)
plt.title('Precio Real vs Precio Predicho')
plt.xlabel('Precio Real')
plt.ylabel('Precio Predicho')
plt.grid(True)
plt.savefig('assets/evaluation_results/real_vs_predicted.png')

mae_by_make.plot(kind='barh', color='salmon', figsize=(12, 8))
plt.title('Error Absoluto Medio (MAE) por Marca')
plt.xlabel('MAE')
plt.ylabel('Marca')
plt.grid(True)
plt.savefig('assets/evaluation_results/mae_by_make.png')

# Guardar resultados generales de la evaluación
with open('assets/evaluation_results/general_evaluation.txt', 'w') as f:
    f.write(f"📉 MAE: {mae:.2f}\n")
    f.write(f"📉 MSE: {mse:.2f}\n")
    f.write(f"📈 R² Score: {r2:.4f}\n")

print("✅ Resultados gráficos y de evaluación guardados correctamente.")
