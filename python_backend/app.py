from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Cargar modelo y encoder
try:
    with open('assets/model.pkl', 'rb') as f:
        model = pickle.load(f)

    with open('assets/encoder.pkl', 'rb') as f:
        encoder = pickle.load(f)
except Exception as e:
    print(f"Error al cargar los archivos: {e}")
    model, encoder = None, None

categorical_features = ['make', 'model', 'fuel', 'shift', 'color', 'province']
numeric_features = ['year', 'kms', 'power', 'doors', 'is_professional']

# Ruta de prueba para verificar que la API está funcionando
@app.route('/', methods=['GET'])
def home():
    return "API está funcionando correctamente."

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or encoder is None:
        return jsonify({"error": "Modelo o encoder no cargados correctamente"}), 500
    
    try:
        # Obtener los datos de la solicitud
        input_data = request.json
        
        # Verificar si se recibe la información correctamente
        print(f"Received data: {input_data}")

        # Crear un DataFrame a partir de la entrada
        df_input = pd.DataFrame([input_data])

        # Codificar las columnas categóricas
        encoded_input = encoder.transform(df_input[categorical_features])
        encoded_columns = encoder.get_feature_names_out(categorical_features)
        encoded_df = pd.DataFrame(encoded_input, columns=encoded_columns)

        # Concatenar las columnas numéricas con las categóricas codificadas
        final_input = pd.concat([encoded_df.reset_index(drop=True), df_input[numeric_features].reset_index(drop=True)], axis=1)

        # Realizar la predicción
        prediction = model.predict(final_input)

        # Devolver el resultado
        return jsonify({"predicted_price": round(prediction[0], 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
