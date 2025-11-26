import os
from dataclasses import dataclass

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor # Compatible with pre-encoded data

# CatBoost is intentionally removed to resolve the 'continuous is not supported' error

from house_price_prediction.utils import save_object, evaluate_models, calculate_metrics

@dataclass
class ModelTrainerConfig:
    """Stores configuration paths for model trainer artifacts."""
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    """Trains, evaluates, and selects the best machine learning model."""
    
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        print("Starting model training and selection...")
        
        try:
            # Separate features (X) and target (y)
            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            # Define the models to be evaluated (ONLY stable models for pre-encoded data)
            models = {
                "Linear Regression": LinearRegression(),
                "Lasso": Lasso(),
                "Ridge": Ridge(),
                "Decision Tree": DecisionTreeRegressor(random_state=42),
                "Random Forest": RandomForestRegressor(random_state=42),
                "Gradient Boosting": GradientBoostingRegressor(random_state=42),
                "XGBRegressor": XGBRegressor(use_label_encoder=False, eval_metric='rmse', random_state=42),
            }
            
            # Evaluate all models using the utility function
            # model_report contains {'ModelName': {'R2': score, 'RMSE': value}}
            model_report: dict = evaluate_models(X_train, y_train, X_test, y_test, models)
            
            print("\n--- Model Evaluation Report (R2 and RMSE) ---")
            
            # Find the best model based on R2 score (the highest value)
            best_model_score_r2 = -float('inf')
            best_model_name = ''
            
            for model_name, metrics in model_report.items():
                # Print both RMSE and R2 for each model as requested
                print(f"{model_name}: R2 = {metrics['R2']:.4f}, RMSE = {metrics['RMSE']:.2f}")
                
                if metrics['R2'] > best_model_score_r2:
                    best_model_score_r2 = metrics['R2']
                    best_model_name = model_name
            
            print("----------------------------------------------------\n")

            best_model = models[best_model_name]
            
            # Guard against a poorly performing model
            if best_model_score_r2 < 0.6: 
                print(f"Warning: Max R2 score is low ({best_model_score_r2:.4f}). Saving model anyway.")
            
            print(f"**Best Model Found: {best_model_name}** with R2 Score: **{best_model_score_r2:.4f}**")

            # Save the best model artifact
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            # Final check on the test set using the best model
            predicted_prices = best_model.predict(X_test)
            rmse_final, r2_final = calculate_metrics(y_test, predicted_prices)
            
            # Print the final performance metrics (RMSE and R2)
            print(f"Final Test Metrics for {best_model_name}:")
            print(f"  Root Mean Squared Error (RMSE): {rmse_final:.2f}")
            print(f"  R2 Score: {r2_final:.4f}")

            # CRITICAL: Return 2 values (RMSE and R2) to the training pipeline orchestrator
            return rmse_final, r2_final
            
        except Exception as e:
            print(f"Error during model training: {e}")
            raise e