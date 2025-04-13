# train_models_by_make.py
import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pickle

df = pd.read_csv("assets/coches_data_cleaned.csv")
os.makedirs("assets/models_por_marca", exist_ok=True)

marcas = df["make"].value_counts().index.tolist()

for marca in marcas:
    df_marca = df[df["make"] == marca]

    if len(df_marca) < 500:
        print(f"⚠️  Marca {marca} ignorada (solo {len(df_marca)} registros).")
        continue

    X = df_marca[['model', 'fuel', 'year', 'kms', 'power', 'doors', 'shift']]
    y = df_marca['price']

    encoder = OneHotEncoder(handle_unknown='ignore', drop='first', sparse_output=False)
    X_encoded = encoder.fit_transform(X[['model', 'fuel', 'shift']])
    X_encoded_df = pd.DataFrame(X_encoded, columns=encoder.get_feature_names_out())

    X_final = pd.concat([
        X_encoded_df.reset_index(drop=True),
        X[['year', 'kms', 'power', 'doors']].reset_index(drop=True)
    ], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    with open(f"assets/models_por_marca/model_{marca.lower()}.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(f"assets/models_por_marca/encoder_{marca.lower()}.pkl", "wb") as f:
        pickle.dump(encoder, f)

    print(f"✅ Modelo para marca {marca} entrenado y guardado.")
