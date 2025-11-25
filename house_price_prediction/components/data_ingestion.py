import os
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    """Stores configuration paths for data ingestion artifacts."""
    # Paths for output artifacts (saved in the 'artifacts' directory)
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "raw.csv")
    
    # Path for the source data (loaded from the 'data' directory)
    # This reflects the user-specified filename: hyderabad_real_estate_dataset3.csv
    source_data_file_path: str = os.path.join('data', 'hyderabad_real_estate_dataset3.csv') 

class DataIngestion:
    """
    Handles reading the raw data from the specified path, saving a raw copy,
    and splitting it into training and testing datasets.
    """
    
    def __init__(self):
        # Initialize configuration paths
        self.ingestion_config = DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        print("Starting data ingestion...")
        
        try:
            # 1. Read Data
            df = pd.read_csv(self.ingestion_config.source_data_file_path)
            print(f"Data read successfully from source. Shape: {df.shape}")

            # Ensure the artifacts directory exists before saving files
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            # 2. Save the raw data copy (Good practice for auditing)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            print("Raw data copy saved to artifacts.")

            # 3. Split Data (Using a standard 80/20 split)
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # 4. Save Train/Test Artifacts
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            
            print("Train/Test data splitting and saving complete.")
            
            # Return paths to be used by the next component (Data Transformation)
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

if __name__ == '__main__':
    # This block allows testing the component independently
    # Note: Requires the 'data' folder and CSV to be present relative to the project root.
    # ingestion = DataIngestion()
    # train_path, test_path = ingestion.initiate_data_ingestion()
    pass