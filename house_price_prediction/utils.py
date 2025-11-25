import os
import dill
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error

def save_object(file_path, obj):
    """Saves a Python object (e.g., model or preprocessor) to a file using dill."""
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
            
    except Exception as e:
        print(f"Error saving object: {e}")
        raise e

def load_object(file_path):
    """Loads a Python object from a file."""
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        print(f"Error loading object: {e}")
        raise e

def evaluate_models(X_train, y_train, X_test, y_test, models):
    """Trains multiple models and returns a dictionary of R2 scores."""
    try:
        report = {}
        for name, model in models.items():
            model.fit(X_train, y_train)
            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)
            report[name] = test_model_score
        return report

    except Exception as e:
        print(f"Error evaluating models: {e}")
        raise e

def calculate_metrics(y_true, y_pred):
    """Calculates RMSE and R2 score (uses sqrt(MSE) for compatibility)."""
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse) 
    r2_square = r2_score(y_true, y_pred)
    return rmse, r2_square