import os
import json
# ...
from flask import Flask, request, jsonify, render_template # ADD render_template
from flask_cors import CORS 
from house_price_prediction.pipeline.prediction_pipeline import CustomData, PredictPipeline

# Initialize the Flask application
app = Flask(__name__)
CORS(app) # Enable CORS for frontend connection

# --- Configuration ---
MODEL_PATH = os.path.join(os.getcwd(), 'artifacts', 'model.pkl')
PREPROCESSOR_PATH = os.path.join(os.getcwd(), 'artifacts', 'preprocessor.pkl')

# --- API Endpoints ---

@app.route('/', methods=['GET'])
def home():
    """Serves the frontend application template."""
    # Flask looks in the 'templates' folder for this file
    return render_template('index.html') 

@app.route('/predict', methods=['POST'])
# ... (rest of the predict route remains unchanged)
def predict_house_price():
    """Endpoint to receive house features (JSON) and return the price prediction."""
    try:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(PREPROCESSOR_PATH):
            return jsonify({
                "error": "Model or Preprocessor artifacts not found. Please run the training pipeline first."
            }), 500

        data = request.json
        
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
        
        pred_df = custom_data.get_data_as_dataframe()
        
        predict_pipeline = PredictPipeline(model_path=MODEL_PATH, preprocessor_path=PREPROCESSOR_PATH)
        
        predicted_price_lakhs = predict_pipeline.predict(pred_df)
        
        return jsonify({
        # CRITICAL FIX: Cast the NumPy float32 result to a standard Python float
        "predicted_price_lakhs": round(float(predicted_price_lakhs), 2),
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