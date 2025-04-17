from flask import Flask, request, jsonify
import pickle
import pandas as pd
import xgboost as xgb

app = Flask(__name__)

# Cargar el modelo y los encoders
def load_model_and_encoders():
    try:
        with open('assets/model.pkl', 'rb') as f:
            model = pickle.load(f)

        with open('assets/encoder_make_model.pkl', 'rb') as f:
            encoder_make_model = pickle.load(f)

        with open('assets/encoder_fuel_shift.pkl', 'rb') as f:
            encoder_fuel_shift = pickle.load(f)
        
        return model, encoder_make_model, encoder_fuel_shift

    except Exception as e:
        print(f"Error al cargar los archivos: {e}")
        return None, None, None

model, encoder_make_model, encoder_fuel_shift = load_model_and_encoders()

# Características categóricas y numéricas
categorical_features = ['make', 'model', 'fuel', 'shift']
numeric_features = ['year', 'kms', 'power', 'doors']

# Ruta de prueba para verificar que la API está funcionando
@app.route('/', methods=['GET'])
def home():
    return "API está funcionando correctamente."

@app.route('/predict', methods=['POST'])
def predict():
    # Verificar que los modelos y encoders se cargaron correctamente
    if model is None or encoder_make_model is None or encoder_fuel_shift is None:
        return jsonify({"error": "Modelo o encoder no cargados correctamente"}), 500
    
    try:
        # Obtener los datos de la solicitud
        input_data = request.json
        
        # Verificar que los datos contienen las claves necesarias
        required_keys = ['make', 'model', 'fuel', 'year', 'kms', 'power', 'doors', 'shift']
        if not all(key in input_data for key in required_keys):
            return jsonify({"error": "Datos incompletos, faltan claves necesarias"}), 400
        
        # Crear un DataFrame a partir de la entrada
        df_input = pd.DataFrame([input_data])

        # Codificar las columnas categóricas (make, model)
        X_encoded_make_model = encoder_make_model.transform(df_input[['make', 'model']])
        encoded_columns_make_model = encoder_make_model.get_feature_names_out(['make', 'model'])
        X_encoded_df_make_model = pd.DataFrame(X_encoded_make_model, columns=encoded_columns_make_model)

        # Codificar las columnas fuel y shift
        X_encoded_fuel_shift = encoder_fuel_shift.transform(df_input[['fuel', 'shift']])
        encoded_columns_fuel_shift = encoder_fuel_shift.get_feature_names_out(['fuel', 'shift'])
        X_encoded_df_fuel_shift = pd.DataFrame(X_encoded_fuel_shift, columns=encoded_columns_fuel_shift)

        # Concatenar las columnas codificadas con las numéricas
        final_input = pd.concat([ 
            df_input[numeric_features].reset_index(drop=True),
            X_encoded_df_make_model.reset_index(drop=True),
            X_encoded_df_fuel_shift.reset_index(drop=True)
        ], axis=1)

        # Verificar que el modelo es de tipo XGBoost
        if not isinstance(model, (xgb.Booster, xgb.XGBModel)):
            return jsonify({"error": "Modelo cargado no es compatible con XGBoost"}), 500

        # Convertir a DMatrix para XGBoost
        dtest = xgb.DMatrix(final_input)

        # Realizar la predicción
        prediction = model.predict(dtest)

        # Devolver el resultado
        predicted_price = float(prediction[0])  # Convertir la predicción a un float estándar
        return jsonify({"predicted_price": round(predicted_price, 2)})

    except Exception as e:
        # Capturar cualquier error que ocurra durante el procesamiento de la solicitud
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Ejecutar la app Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
