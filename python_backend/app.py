from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Cargar el modelo y los encoders
try:
    with open('assets/model.pkl', 'rb') as f:
        model = pickle.load(f)

    with open('assets/encoder_make_model.pkl', 'rb') as f:
        encoder_make_model = pickle.load(f)

    with open('assets/encoder_fuel_shift.pkl', 'rb') as f:
        encoder_fuel_shift = pickle.load(f)
    
except Exception as e:
    print(f"Error al cargar los archivos: {e}")
    model, encoder_make_model, encoder_fuel_shift = None, None, None

# Características categóricas y numéricas
categorical_features = ['make', 'model', 'fuel', 'shift']
numeric_features = ['year', 'kms', 'power', 'doors']

# Ruta de prueba para verificar que la API está funcionando
@app.route('/', methods=['GET'])
def home():
    return "API está funcionando correctamente."

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or encoder_make_model is None or encoder_fuel_shift is None:
        return jsonify({"error": "Modelo o encoder no cargados correctamente"}), 500
    
    try:
        # Obtener los datos de la solicitud
        input_data = request.json
        
        # Verificar si se recibe la información correctamente
        print(f"Received data: {input_data}")

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

        # Realizar la predicción
        prediction = model.predict(final_input)

        # Devolver el resultado
        return jsonify({"predicted_price": round(prediction[0], 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



