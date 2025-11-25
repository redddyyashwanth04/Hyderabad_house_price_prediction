import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS # CRITICAL: Import the CORS extension
from house_price_prediction.pipeline.prediction_pipeline import CustomData, PredictPipeline

# Initialize the Flask application
app = Flask(__name__)
CORS(app) # CRITICAL: Initialize CORS to allow cross-origin requests from the local HTML file

# --- Configuration ---
# Define the paths to the artifacts relative to the app.py file
MODEL_PATH = os.path.join(os.getcwd(), 'artifacts', 'model.pkl')
PREPROCESSOR_PATH = os.path.join(os.getcwd(), 'artifacts', 'preprocessor.pkl')

# --- API Endpoints ---

@app.route('/', methods=['GET'])
def home():
    """Simple check to ensure the server is running."""
    return "<h1>Home Price Prediction API is Running!</h1>"

@app.route('/predict', methods=['POST'])
def predict_house_price():
    """Endpoint to receive house features (JSON) and return the price prediction."""
    try:
        # Check if model artifacts exist before attempting prediction
        if not os.path.exists(MODEL_PATH) or not os.path.exists(PREPROCESSOR_PATH):
            return jsonify({
                "error": "Model or Preprocessor artifacts not found. Please run the training pipeline first."
            }), 500

        # 1. Get data from POST request (JSON body)
        data = request.json
        
        # 2. Create the CustomData object from the input, ensuring correct type casting
        custom_data = CustomData(
            Location_Name=data['Location_Name'],
            Area_SqFt=float(data['Area_SqFt']),
            Bedrooms=int(data['Bedrooms']),
            Bathrooms=int(data['Bathrooms']),
            Property_Type=data['Property_Type'],
            Furnishing_Status=data['Furnishing_Status'],
            Year_Built=int(data['Year_Built']),
            Gated_Community=data['Gated_Community'],
            Balcony=data['Balcony'],
            Floors=int(data['Floors']),
            Facing_Direction=data['Facing_Direction']
        )
        
        # 3. Get the feature dataframe
        pred_df = custom_data.get_data_as_dataframe()
        
        # 4. Run the prediction pipeline
        predict_pipeline = PredictPipeline(
            model_path=MODEL_PATH, 
            preprocessor_path=PREPROCESSOR_PATH
        )
        
        predicted_price_lakhs = predict_pipeline.predict(pred_df)
        
        # 5. Return result
        return jsonify({
            "predicted_price_lakhs": round(predicted_price_lakhs, 2),
            "currency_unit": "Lakhs",
            "message": "Prediction successful"
        })

    except KeyError as ke:
        return jsonify({
            "error": "Missing required field in JSON input. Check feature names.",
            "details": str(ke)
        }), 400
    except Exception as e:
        print(f"An unexpected error occurred during prediction: {e}")
        return jsonify({
            "error": "Prediction failed due to internal error",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Flask server on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)