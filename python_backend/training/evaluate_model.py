# evaluate_model.py
import pandas as pd
import pickle
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

# Cargar datos
df = pd.read_csv("assets/coches_data_cleaned.csv")

# Cargar encoder y modelo
with open("assets/model.pkl", "rb") as f:
    model = pickle.load(f)
with open("assets/encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

# Features y target
X = df[['make', 'model', 'fuel', 'year', 'kms', 'power', 'doors', 'shift']]
y = df['price']

# Codificar categóricas
X_encoded = encoder.transform(X[['make', 'model', 'fuel', 'shift']])
X_encoded_df = pd.DataFrame(X_encoded, columns=encoder.get_feature_names_out())

# Concatenar numéricas
X_final = pd.concat([
    X_encoded_df.reset_index(drop=True),
    X[['year', 'kms', 'power', 'doors']].reset_index(drop=True)
], axis=1)

# Split igual que en el entrenamiento
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)
df_test = df.iloc[y_test.index]  # Para saber qué marca corresponde

# Predecir
y_pred = model.predict(X_test)

# Calcular MAE general
mae_global = mean_absolute_error(y_test, y_pred)
print(f"📊 MAE Global: {mae_global:.2f} €")

# MAE por marca
df_resultado = df_test.copy()
df_resultado["predicted"] = y_pred
df_resultado["error_abs"] = abs(df_resultado["predicted"] - df_resultado["price"])

mae_por_marca = df_resultado.groupby("make")["error_abs"].mean().sort_values(ascending=False)
print("\n🚗 MAE por marca:")
print(mae_por_marca)
