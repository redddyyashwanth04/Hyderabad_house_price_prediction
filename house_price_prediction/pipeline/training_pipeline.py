import os
import sys 
from house_price_prediction.components.data_ingestion import DataIngestion
from house_price_prediction.components.data_transformation import DataTransformation
from house_price_prediction.components.model_trainer import ModelTrainer

def run_training_pipeline(data_source_path):
    """Orchestrates the execution of the entire data science pipeline."""
    print("--- Starting End-to-End Training Pipeline ---")
    
    # 1. DATA INGESTION
    try:
        print("\n[Stage 1/3] Starting Data Ingestion...")
        ingestion = DataIngestion()
        ingestion.ingestion_config.source_data_file_path = data_source_path 
        # CRITICAL FIX: Expect 4 return values (paths + shapes)
        train_data_path, test_data_path, train_shape, test_shape = ingestion.initiate_data_ingestion()
        print(f"Data Ingestion Complete.")
        # Print data split numbers
        print(f"  Train Data Shape: {train_shape}")
        print(f"  Test Data Shape: {test_shape}")

    except Exception as e:
        print(f"FATAL ERROR in Data Ingestion: {e}")
        return

    # 2. DATA TRANSFORMATION
    try:
        print("\n[Stage 2/3] Starting Data Transformation...")
        transformation = DataTransformation()
        train_arr, test_arr, preprocessor_path = transformation.initiate_data_transformation(
            train_data_path, 
            test_data_path
        )
        print(f"Data Transformation Complete. Preprocessor saved to: {preprocessor_path}")

    except Exception as e:
        print(f"FATAL ERROR in Data Transformation: {e}")
        return
        
    # 3. MODEL TRAINING
    try:
        print("\n[Stage 3/3] Starting Model Training...")
        trainer = ModelTrainer()
        # CRITICAL FIX: Expect 2 return values (RMSE, R2)
        rmse_score, r2_score = trainer.initiate_model_trainer(train_arr, test_arr)
        
        print("\n--- Training Pipeline Successfully Completed ---")
        # Print final metrics
        print(f"Final Model RMSE Score: {rmse_score:.2f}")
        print(f"Final Best Model R2 Score: {r2_score:.4f}")

    except Exception as e:
        print(f"FATAL ERROR in Model Training: {e}")
        return

if __name__ == '__main__':
    DATA_FILENAME = 'hyderabad_real_estate_dataset3.csv'
    DATA_PATH = os.path.join(os.getcwd(), 'data', DATA_FILENAME) 
    
    if os.path.exists(DATA_PATH):
        run_training_pipeline(DATA_PATH)
    else:
        print(f"Error: Data file not found at {DATA_PATH}. Please place your housing data CSV file there.")