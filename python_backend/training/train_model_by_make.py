# train_models_by_make.py
import pandas as pd
import os
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pickle

# Cargar los datos
df = pd.read_csv("assets/coches_data_cleaned.csv")
os.makedirs("assets/models_por_marca", exist_ok=True)

# Obtener las marcas
marcas = df["make"].value_counts().index.tolist()

# Iterar sobre cada marca
for marca in marcas:
    df_marca = df[df["make"] == marca]

    # Ignorar marcas con menos de 500 registros
    if len(df_marca) < 500:
        print(f"⚠️  Marca {marca} ignorada (solo {len(df_marca)} registros).")
        continue

    # Seleccionar las características (X) y la variable objetivo (y)
    X = df_marca[['model', 'fuel', 'year', 'kms', 'power', 'doors', 'shift']]
    y = df_marca['price']

    # Aplicar OneHotEncoding para las variables categóricas
    encoder = OneHotEncoder(handle_unknown='ignore', drop='first', sparse_output=False)
    X_encoded = encoder.fit_transform(X[['model', 'fuel', 'shift']])
    X_encoded_df = pd.DataFrame(X_encoded, columns=encoder.get_feature_names_out())

    # Concatenar las características codificadas con las numéricas
    X_final = pd.concat([X_encoded_df.reset_index(drop=True),
                         X[['year', 'kms', 'power', 'doors']].reset_index(drop=True)], axis=1)

    # Dividir en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

    # Configuración de los parámetros de XGBoost
    params = {
        'objective': 'reg:squarederror',  # Tarea de regresión
        'eval_metric': 'rmse',  # Métrica de evaluación
        'max_depth': 6,  # Profundidad máxima del árbol
        'eta': 0.1,  # Tasa de aprendizaje
        'silent': 1,  # Silenciar mensajes
        'nthread': 4  # Número de hilos para paralelizar
    }

    # Convertir los datos a DMatrix (formato eficiente de XGBoost)
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    # Entrenar el modelo XGBoost
    num_round = 100  # Número de iteraciones (árboles)
    model = xgb.train(params, dtrain, num_round)

    # Guardar el modelo entrenado
    with open(f"assets/models_por_marca/model_{marca.lower()}.pkl", "wb") as f:
        pickle.dump(model, f)

    # Guardar el codificador (encoder) para las variables categóricas
    with open(f"assets/models_por_marca/encoder_{marca.lower()}.pkl", "wb") as f:
        pickle.dump(encoder, f)

    print(f"✅ Modelo para marca {marca} entrenado y guardado.")
