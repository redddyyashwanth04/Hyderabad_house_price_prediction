import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from dataclasses import dataclass
import os

from house_price_prediction.utils import save_object 

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation:
    
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            # Finalized feature lists for the model
            numerical_features = [
                'Area_SqFt', 'Bedrooms', 'Bathrooms', 'Floors', 'Age_of_Property_Years' 
            ] 
            categorical_features = [
                'Location_Name', 'Property_Type', 'Furnishing_Status', 
                'Facing_Direction', 'Gated_Community', 'Balcony'
            ]
            
            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')), 
                ('scaler', StandardScaler())
            ])
            
            cat_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
            ])
            
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_features),
                    ("cat_pipeline", cat_pipeline, categorical_features)
                ],
                remainder='drop' 
            )
            
            return preprocessor
        
        except Exception as e:
            print(f"Error creating transformer object: {e}")
            raise e

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            target_column_name = 'Price_Lakhs' 
            current_year = 2025 # Must match year in prediction pipeline
            
            if 'Year_Built' not in train_df.columns:
                 raise KeyError("Required column 'Year_Built' not found in data for feature engineering.")
            
            train_df['Age_of_Property_Years'] = current_year - train_df['Year_Built']
            test_df['Age_of_Property_Years'] = current_year - test_df['Year_Built']
            
            drop_columns = [target_column_name, 'Property_ID', 'Transaction_Date', 'Transaction_Year', 
                            'Transaction_Month', 'Market_Condition', 'Location_Maturity', 'Resale', 
                            'New_Construction', 'Builder_Reputation', 'Possession_Status', 'Maintenance_Staff', 
                            'Gymnasium', 'Swimming_Pool', 'Landscaped_Gardens', 'Jogging_Track', 'Club_House', 
                            '24x7_Security', 'Power_Backup', 'Car_Parking', 'Lift_Available', 'School_Proximity_Km', 
                            'Hospital_Proximity_Km', 'IT_Hub_Proximity_Km', 'Metro_Proximity_Km', 'Amenities_Score', 
                            'Transaction_Type', 'Price_per_SqFt', 'Period', 'Year_Built'] 
            
            if target_column_name not in train_df.columns:
                raise KeyError(f"Target variable '{target_column_name}' not found in data.")

            target_feature_train_df = train_df[target_column_name]
            target_feature_test_df = test_df[target_column_name]
            
            input_feature_train_df = train_df.drop(columns=drop_columns, axis=1, errors='ignore')
            input_feature_test_df = test_df.drop(columns=drop_columns, axis=1, errors='ignore')
            
            preprocessor = self.get_data_transformer_object()
            
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor
            )

            return (train_arr, test_arr, self.data_transformation_config.preprocessor_obj_file_path)

        except KeyError as e:
            print(f"ERROR: A critical column name mismatch was detected. Column {e} is missing or misspelled.")
            raise
        except Exception as e:
            print(f"Error during data transformation: {e}")
            raise e