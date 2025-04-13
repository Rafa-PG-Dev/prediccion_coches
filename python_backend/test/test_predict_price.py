import sys
import os

# Añadir el directorio donde se encuentra el archivo predict_price.py al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'prediction')))

# Ahora puedes importar la función predict_price desde predict_price.py
from prediction.predict_price import predict_price

# Test de la función
if __name__ == "__main__":
    input_data = {
        'make': 'CITROEN',
        'model': 'C1',
        'fuel': 'Gasolina',
        'year': 2017,
        'kms': 50071,
        'power': 82,
        'doors': 5,
        'shift': 'Automático'
    }

    predicted_price = predict_price(input_data)
    print(f"Predicted price: {predicted_price}")
