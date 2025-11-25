import os

def create_project_structure(base_dir="."):
    """
    Creates the project structure (house_price_prediction/ and root files) 
    relative to the current execution directory (base_dir).
    """
    
    # 1. Define all necessary directories relative to the current working directory
    # Note: 'house_price_prediction/' must be explicitly included as a folder here.
    directories = [
        "house_price_prediction/components/",
        "house_price_prediction/pipeline/",
        "house_price_prediction/artifacts/",
        "Notebooks/",
        "frontend/",
    ]

    # 2. Define all necessary files relative to the current working directory
    files_to_create = [
        # Main ML Package Files
        "house_price_prediction/__init__.py", # Essential for Python package
        "house_price_prediction/utils.py",
        
        # Components
        "house_price_prediction/components/data_ingestion.py",
        "house_price_prediction/components/data_transformation.py",
        "house_price_prediction/components/model_trainer.py",
        
        # Pipelines
        "house_price_prediction/pipeline/training_pipeline.py",
        "house_price_prediction/pipeline/prediction_pipeline.py",
        
        # Root Level Files
        "app.py",
        "requirements.txt",
        "setup.py",
        
        # Notebooks
        "Notebooks/EDA_and_Testing.ipynb",
        
        # Frontend
        "frontend/index.html",
        "frontend/style.css",
        "frontend/script.js",
    ]

    print(f"Starting creation of project structure inside: **{os.getcwd()}**")

    # --- Create Directories ---
    for dir_path in directories:
        full_path = os.path.join(base_dir, dir_path)
        os.makedirs(full_path, exist_ok=True)
        print(f"Created directory: {full_path}")

    # --- Create Files ---
    for file_path in files_to_create:
        full_path = os.path.join(base_dir, file_path)
        try:
            # Ensure parent directories exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Create the file
            with open(full_path, "a"):
                pass 
            print(f"Created file: {full_path}")
        except Exception as e:
            print(f"Error creating file {full_path}. Details: {e}")

    # --- Create Placeholder Artifacts (For completeness) ---
    artifacts_dir = os.path.join(base_dir, "house_price_prediction", "artifacts")
    # The artifacts directory is already created above, just ensuring files are there.
    open(os.path.join(artifacts_dir, "preprocessor.pkl"), "a").close()
    open(os.path.join(artifacts_dir, "model.pkl"), "a").close()
    print(f"Created placeholder artifact files.")


    print("\n🎉 **Project Structure Creation Complete!**")
    print("The necessary files and folders are now in your current directory.")

if __name__ == "__main__":
    create_project_structure()