import os
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    """Stores configuration paths for data ingestion artifacts."""
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "raw.csv")
    
    # CRITICAL: Reference your specific file name
    source_data_file_path: str = os.path.join('data', 'hyderabad_real_estate_dataset3.csv') 

class DataIngestion:
    """Handles the ingestion of raw data and splitting into train/test sets."""
    
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        print("Starting data ingestion...")
        
        try:
            df = pd.read_csv(self.ingestion_config.source_data_file_path)
            print(f"Data read successfully from source. Shape: {df.shape}")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            
            print("Train/Test data splitting and saving complete.")
            
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        
        except FileNotFoundError:
            print(f"Error: Source file not found at {self.ingestion_config.source_data_file_path}. Please check your path.")
            raise
        except Exception as e:
            print(f"Error during data ingestion: {e}")
            raise e