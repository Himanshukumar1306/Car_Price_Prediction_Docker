from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

MODEL_PATH = 'model.pkl'

# Load the model globally at startup
model = None
if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
else:
    print(f"WARNING: Model file '{MODEL_PATH}' not found. Please train the model first.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    global model
    if model is None:
        # Try loading model again if not initialized
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, 'rb') as f:
                    model = pickle.load(f)
            except Exception as e:
                return jsonify({'error': f'Model failed to load: {str(e)}'}), 500
        else:
            return jsonify({'error': 'Model file not found. App is not trained.'}), 500

    try:
        # Support both JSON and standard Form data submissions
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        # Required fields list
        required_fields = ['present_price', 'kms_driven', 'fuel_type', 'seller_type', 'transmission', 'owner', 'age']
        
        # Verify fields existence and non-emptiness
        missing = [field for field in required_fields if field not in data or str(data[field]).strip() == '']
        if missing:
            return jsonify({'error': f'Missing required fields: {", ".join(missing)}'}), 400

        # Parse numerical types
        try:
            present_price = float(data['present_price'])
            kms_driven = float(data['kms_driven'])
            fuel_type = int(data['fuel_type'])
            seller_type = int(data['seller_type'])
            transmission = int(data['transmission'])
            owner = int(data['owner'])
            age = int(data['age'])
        except ValueError:
            return jsonify({'error': 'Invalid input formats. All fields must be numeric.'}), 400

        # Validate values range
        if present_price <= 0:
            return jsonify({'error': 'Present Price must be greater than 0 Lakhs.'}), 400
        if kms_driven < 0:
            return jsonify({'error': 'Kilometers Driven cannot be negative.'}), 400
        if fuel_type not in [0, 1, 2]:
            return jsonify({'error': 'Fuel Type must be 0 (Petrol), 1 (Diesel), or 2 (CNG).'}), 400
        if seller_type not in [0, 1]:
            return jsonify({'error': 'Seller Type must be 0 (Dealer) or 1 (Individual).'}), 400
        if transmission not in [0, 1]:
            return jsonify({'error': 'Transmission must be 0 (Manual) or 1 (Automatic).'}), 400
        if owner < 0:
            return jsonify({'error': 'Owners count cannot be negative.'}), 400
        if age < 0:
            return jsonify({'error': 'Age of Car cannot be negative.'}), 400

        # Match columns used during model training:
        # ['Present_Price', 'Kms_Driven', 'Fuel_Type_Num', 'Seller_Type_Num', 'Transmission_Num', 'Owner', 'Age']
        features = np.array([[present_price, kms_driven, fuel_type, seller_type, transmission, owner, age]])
        
        # Predict price
        pred = model.predict(features)[0]
        
        # Clip negative predictions to 0.0
        prediction_val = max(0.0, float(pred))
        
        return jsonify({
            'success': True,
            'prediction': round(prediction_val, 2),
            'formatted_prediction': f"{prediction_val:.2f}"
        })

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/health')
def health():
    if model is not None:
        return jsonify({'status': 'healthy'}), 200
    return jsonify({'status': 'unhealthy', 'reason': 'model not loaded'}), 500

if __name__ == '__main__':
    # Listen on all interfaces on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
