import pandas as pd
import numpy as np
from house_price_prediction.utils import load_object

class PredictPipeline:
    
    def __init__(self, model_path, preprocessor_path):
        self.model = load_object(file_path=model_path)
        self.preprocessor = load_object(file_path=preprocessor_path)

    def predict(self, features: pd.DataFrame):
        try:
            current_year = 2025 # Must match year used in data_transformation.py
            features['Age_of_Property_Years'] = current_year - features['Year_Built']
            
            data_transformed = self.preprocessor.transform(features)
            
            prediction = self.model.predict(data_transformed)
            
            return prediction[0]
        
        except Exception as e:
            print(f"Error during prediction: {e}")
            raise e

class CustomData:
    
    def __init__(self, Location_Name: str, Area_SqFt: float, Bedrooms: int, Bathrooms: int, 
                 Property_Type: str, Furnishing_Status: str, Year_Built: int, 
                 Gated_Community: str, Balcony: str, Floors: int, Facing_Direction: str):
                 
        self.Location_Name = Location_Name
        self.Area_SqFt = Area_SqFt
        self.Bedrooms = Bedrooms
        self.Bathrooms = Bathrooms
        self.Property_Type = Property_Type
        self.Furnishing_Status = Furnishing_Status
        self.Year_Built = Year_Built
        self.Gated_Community = Gated_Community
        self.Balcony = Balcony
        self.Floors = Floors
        self.Facing_Direction = Facing_Direction

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'Location_Name': [self.Location_Name], 'Area_SqFt': [self.Area_SqFt],
                'Bedrooms': [self.Bedrooms], 'Bathrooms': [self.Bathrooms],
                'Property_Type': [self.Property_Type], 'Furnishing_Status': [self.Furnishing_Status],
                'Year_Built': [self.Year_Built], 'Gated_Community': [self.Gated_Community],
                'Balcony': [self.Balcony], 'Floors': [self.Floors],
                'Facing_Direction': [self.Facing_Direction]
            }
            
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            print(f"Error in CustomData creation: {e}")
            raise e