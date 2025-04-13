import pandas as pd
import pickle

# Cargar el modelo entrenado y los encoders
with open('assets/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('assets/encoder_make_model.pkl', 'rb') as f:
    encoder_make_model = pickle.load(f)

with open('assets/encoder_fuel_shift.pkl', 'rb') as f:
    encoder_fuel_shift = pickle.load(f)

def predict_price(input_data):
    # Crear DataFrame a partir del input
    input_df = pd.DataFrame([input_data])

    # Separar las columnas categóricas y numéricas
    categorical_cols = ['fuel', 'shift', 'make', 'model']
    numerical_cols = [col for col in input_df.columns if col not in categorical_cols]

    # Codificar las columnas categóricas
    X_encoded_fuel_shift = encoder_fuel_shift.transform(input_df[['fuel', 'shift']])
    encoded_cols_fuel_shift = encoder_fuel_shift.get_feature_names_out(['fuel', 'shift'])
    X_encoded_df_fuel_shift = pd.DataFrame(X_encoded_fuel_shift, columns=encoded_cols_fuel_shift)

    X_encoded_make_model = encoder_make_model.transform(input_df[['make', 'model']])
    encoded_cols_make_model = encoder_make_model.get_feature_names_out(['make', 'model'])
    X_encoded_df_make_model = pd.DataFrame(X_encoded_make_model, columns=encoded_cols_make_model)

    # Concatenar todo
    X_final = pd.concat([
        input_df[numerical_cols].reset_index(drop=True),
        X_encoded_df_make_model.reset_index(drop=True),
        X_encoded_df_fuel_shift.reset_index(drop=True)
    ], axis=1)

    # Predecir
    predicted_price = model.predict(X_final)[0]
    return predicted_price
