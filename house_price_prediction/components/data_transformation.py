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
    """Stores configuration paths for data transformation artifacts."""
    preprocessor_obj_file_path: str = os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation:
    """Performs data cleaning, feature engineering, and transformation."""
    
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        Creates the data preprocessing pipeline with the finalized feature set.
        """
        
        try:
            # --- 1. Define the finalized feature lists ---
            # These lists must match the column names exactly after feature engineering (if applicable).
            
            # Features that will be scaled
            numerical_features = [
                'Area_SqFt', 
                'Bedrooms', 
                'Bathrooms', 
                'Floors', 
                'Age_of_Property_Years' # Engineered feature
            ] 
            
            # Features that will be One-Hot Encoded
            categorical_features = [
                'Location_Name', 
                'Property_Type', 
                'Furnishing_Status', 
                'Facing_Direction', 
                'Gated_Community',
                'Balcony'
            ]
            
            # --- Numerical Pipeline ---
            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')), 
                ('scaler', StandardScaler())
            ])
            
            # --- Categorical Pipeline ---
            cat_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
            ])
            
            print("Numerical and Categorical pipelines configured with selected features.")

            # 2. Combine pipelines using ColumnTransformer
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_features),
                    ("cat_pipeline", cat_pipeline, categorical_features)
                ],
                remainder='drop' # Explicitly drops any columns not specified above
            )
            
            return preprocessor
        
        except Exception as e:
            print(f"Error creating transformer object: {e}")
            raise e

    def initiate_data_transformation(self, train_path, test_path):
        """Loads data, applies feature engineering, transformation, and saves the preprocessor."""
        
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            print("Train and test data loaded for transformation.")
            
            # Define target and the columns we need to drop
            target_column_name = 'Price_Lakhs' 
            
            # --- 1. Feature Engineering: Create Age_of_Property_Years ---
            current_year = 2025 # Must match year in prediction pipeline
            
            # CRITICAL CHECK: Ensure 'Year_Built' exists before calculating Age
            if 'Year_Built' not in train_df.columns:
                 raise KeyError("Required column 'Year_Built' not found in data for feature engineering.")
            
            train_df['Age_of_Property_Years'] = current_year - train_df['Year_Built']
            test_df['Age_of_Property_Years'] = current_year - test_df['Year_Built']
            
            # --- 2. Define Columns to Drop ---
            # This list includes the target and all features not selected for the model.
            drop_columns = [
                target_column_name, 
                'Property_ID', 'Transaction_Date', 'Transaction_Year', 'Transaction_Month', 'Market_Condition', 
                'Location_Maturity', 'Resale', 'New_Construction', 'Builder_Reputation', 
                'Possession_Status', 'Maintenance_Staff', 'Gymnasium', 'Swimming_Pool', 'Landscaped_Gardens', 
                'Jogging_Track', 'Club_House', '24x7_Security', 'Power_Backup', 'Car_Parking', 'Lift_Available', 
                'School_Proximity_Km', 'Hospital_Proximity_Km', 'IT_Hub_Proximity_Km', 'Metro_Proximity_Km', 
                'Amenities_Score', 'Transaction_Type', 'Price_per_SqFt', 'Period', 
                'Year_Built' # Original year is dropped since 'Age' is engineered
            ]
            
            # --- 3. Separate Features and Target ---
            
            # Isolate the target variable first (CRITICAL CHECKPOINT)
            if target_column_name not in train_df.columns:
                raise KeyError(f"Target variable '{target_column_name}' not found in data.")

            target_feature_train_df = train_df[target_column_name]
            target_feature_test_df = test_df[target_column_name]
            
            # Drop unused columns and the target column from the feature DataFrame
            input_feature_train_df = train_df.drop(columns=drop_columns, axis=1, errors='ignore')
            input_feature_test_df = test_df.drop(columns=drop_columns, axis=1, errors='ignore')
            
            # FINAL SANITY CHECK: The remaining columns must exactly match the list 
            # defined in get_data_transformer_object() + Age_of_Property_Years.
            print(f"Features ready for transformation. Train features remaining: {input_feature_train_df.columns.tolist()}")

            # 4. Get and Apply Preprocessor
            preprocessor = self.get_data_transformer_object()
            
            # Fit/transform on training data
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            # Transform only on test data
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            # 5. Combine transformed features (X) and target (y)
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            print("Data transformation completed. Transformed data ready for model training.")
            
            # Save the preprocessor artifact
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor
            )

            return (
                train_arr, 
                test_arr, 
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except KeyError as e:
            # Re-raise KeyError with specific context if a column is definitively missing
            print(f"ERROR: A critical column name mismatch was detected. Column {e} is missing or misspelled.")
            raise
        except Exception as e:
            print(f"Error during data transformation: {e}")
            raise e