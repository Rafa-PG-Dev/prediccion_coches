import pandas as pd
import os
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pickle

# ===============================
# 1. Cargar los datos
# ===============================
df = pd.read_csv('assets/coches_data_cleaned.csv')

# ===============================
# 2. Filtrar marcas con pocos registros (menos de 50 registros)
# ===============================
marca_counts = df['make'].value_counts()
umbral = 50
marcas_validas = marca_counts[marca_counts >= umbral].index
df = df[df['make'].isin(marcas_validas)]

# ===============================
# 3. Definir variables X (features) e y (target)
# ===============================
X = df[['make', 'model', 'fuel', 'year', 'kms', 'power', 'doors', 'shift']]  # is_professional eliminado si no se usó
y = df['price']

# ===============================
# 4. Crear el encoder SIN definir manualmente las categorías
# ===============================
encoder = OneHotEncoder(
    handle_unknown='ignore',
    sparse_output=False
)

X_encoded_fuel_shift = encoder.fit_transform(X[['fuel', 'shift']])
encoded_columns_fuel_shift = encoder.get_feature_names_out(['fuel', 'shift'])
X_encoded_df_fuel_shift = pd.DataFrame(X_encoded_fuel_shift, columns=encoded_columns_fuel_shift)

# ===============================
# 5. Codificar las columnas 'make' y 'model' (otras variables categóricas)
# ===============================
encoder_make_model = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
X_encoded_make_model = encoder_make_model.fit_transform(X[['make', 'model']])
encoded_columns_make_model = encoder_make_model.get_feature_names_out(['make', 'model'])
X_encoded_df_make_model = pd.DataFrame(X_encoded_make_model, columns=encoded_columns_make_model)

# ===============================
# 6. Concatenar todas las columnas
# ===============================
X_final = pd.concat([ 
    X[['year', 'kms', 'power', 'doors']].reset_index(drop=True),
    X_encoded_df_make_model.reset_index(drop=True),
    X_encoded_df_fuel_shift.reset_index(drop=True)
], axis=1)

# ===============================
# 7. Dividir en train y test
# ===============================
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

# ===============================
# 8. Entrenar el modelo (XGBoost en vez de RandomForest)
# ===============================
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test)

# Parámetros de XGBoost
params = {
    'objective': 'reg:squarederror',  # Problema de regresión
    'eval_metric': 'mae',  # Métrica para evaluación
    'max_depth': 6,  # Profundidad del árbol
    'learning_rate': 0.1,  # Tasa de aprendizaje
    'n_estimators': 100  # Número de árboles
}

# Entrenamos el modelo
model = xgb.train(params, dtrain, num_boost_round=100)

# ===============================
# 9. Guardar el modelo y el encoder
# ===============================
os.makedirs('assets', exist_ok=True)

with open('assets/model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('assets/encoder_make_model.pkl', 'wb') as f:
    pickle.dump(encoder_make_model, f)

with open('assets/encoder_fuel_shift.pkl', 'wb') as f:
    pickle.dump(encoder, f)

print("✅ Modelo y encoders entrenados y guardados correctamente.")
