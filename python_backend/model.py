import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# Cargar datos limpios
df = pd.read_csv('assets/data_cleaned.csv')

# Definir X e y
X = df[['make', 'model', 'fuel', 'year', 'kms', 'power', 'doors', 'shift', 'color', 'is_professional', 'province']]
y = df['price']

# Codificar variables categóricas
categorical_features = ['make', 'model', 'fuel', 'shift', 'color', 'province']
encoder = OneHotEncoder(handle_unknown='ignore', drop='first', sparse_output=False)
X_encoded = encoder.fit_transform(X[categorical_features])

# Crear DataFrame con columnas codificadas
encoded_columns = encoder.get_feature_names_out(categorical_features)
X_encoded_df = pd.DataFrame(X_encoded, columns=encoded_columns)

# Concatenar con columnas numéricas
X_final = pd.concat([
    X_encoded_df.reset_index(drop=True),
    X[['year', 'kms', 'power', 'doors', 'is_professional']].reset_index(drop=True)
], axis=1)

# Dividir en train/test
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

# Entrenar modelo
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Guardar modelo y encoder
with open('assets/model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('assets/encoder.pkl', 'wb') as f:
    pickle.dump(encoder, f)

print("✅ Modelo y encoder entrenados y guardados correctamente.")
