import pandas as pd
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder

# Configuración
DATA_PATH = "assets/coches_data_cleaned.csv"
MODELS_PATH = "assets/brand_models/"
MAE_THRESHOLD = 8000  # puedes ajustar este umbral

# Crear carpeta si no existe
os.makedirs(MODELS_PATH, exist_ok=True)

# Cargar dataset
df = pd.read_csv(DATA_PATH)

# Definir columnas
features = ['make', 'model', 'fuel', 'year', 'kms', 'power', 'doors', 'shift']
target = 'price'
categorical_features = ['make', 'model', 'fuel', 'shift']

# 1. Entrenar modelo general para calcular MAE por marca
from sklearn.metrics import mean_absolute_error

X = df[features]
y = df[target]

encoder = OneHotEncoder(handle_unknown='ignore', drop='first', sparse_output=False)
X_encoded = encoder.fit_transform(X[categorical_features])
encoded_columns = encoder.get_feature_names_out(categorical_features)
X_encoded_df = pd.DataFrame(X_encoded, columns=encoded_columns)

X_final = pd.concat([
    X_encoded_df.reset_index(drop=True),
    X[['year', 'kms', 'power', 'doors']].reset_index(drop=True)
], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

X_test['make'] = X.loc[X_test.index, 'make']
X_test['error_abs'] = abs(y_pred - y_test.values)
mae_by_make = X_test.groupby('make')['error_abs'].mean()

# 2. Marcas con error alto
high_error_brands = mae_by_make[mae_by_make > MAE_THRESHOLD].index.tolist()

print(f"🧠 Entrenando modelos por marca para: {high_error_brands}")

# 3. Entrenar modelo por cada marca
for brand in high_error_brands:
    df_brand = df[df['make'] == brand]
    
    if len(df_brand) < 100:
        print(f"⚠️  Marca {brand} tiene pocos datos, saltando...")
        continue

    Xb = df_brand[features]
    yb = df_brand[target]

    encoder_b = OneHotEncoder(handle_unknown='ignore', drop='first', sparse_output=False)
    Xb_encoded = encoder_b.fit_transform(Xb[categorical_features])
    encoded_columns_b = encoder_b.get_feature_names_out(categorical_features)
    Xb_encoded_df = pd.DataFrame(Xb_encoded, columns=encoded_columns_b)

    Xb_final = pd.concat([
        Xb_encoded_df.reset_index(drop=True),
        Xb[['year', 'kms', 'power', 'doors']].reset_index(drop=True)
    ], axis=1)

    Xb_train, Xb_test, yb_train, yb_test = train_test_split(Xb_final, yb, test_size=0.2, random_state=42)

    model_b = RandomForestRegressor(n_estimators=100, random_state=42)
    model_b.fit(Xb_train, yb_train)

    # Guardar modelo y encoder
    model_file = os.path.join(MODELS_PATH, f"model_{brand}.pkl")
    encoder_file = os.path.join(MODELS_PATH, f"encoder_{brand}.pkl")

    with open(model_file, 'wb') as f:
        pickle.dump(model_b, f)
    with open(encoder_file, 'wb') as f:
        pickle.dump(encoder_b, f)

    print(f"✅ Modelo guardado para {brand}")
