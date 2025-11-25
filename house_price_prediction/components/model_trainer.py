import os
from dataclasses import dataclass

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

from house_price_prediction.utils import save_object, evaluate_models, calculate_metrics

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        print("Starting model training and selection...")
        
        try:
            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            models = {
                "Linear Regression": LinearRegression(),
                "Lasso": Lasso(),
                "Ridge": Ridge(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest": RandomForestRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "XGBRegressor": XGBRegressor(use_label_encoder=False, eval_metric='rmse'),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
            }
            
            model_report: dict = evaluate_models(X_train, y_train, X_test, y_test, models)
            
            print("\n--- Model Evaluation Report ---")
            for model_name, r2_score in model_report.items():
                print(f"{model_name}: R2 Score = {r2_score:.4f}")
            print("-------------------------------\n")

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score < 0.6: 
                raise Exception(f"No model achieved an acceptable R2 score (Max R2: {best_model_score:.4f})")
            
            print(f"**Best Model Found: {best_model_name}** with R2 Score: **{best_model_score:.4f}**")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted_prices = best_model.predict(X_test)
            rmse, r2_square = calculate_metrics(y_test, predicted_prices)
            
            print(f"Final Test Metrics for {best_model_name}:")
            print(f"  Root Mean Squared Error (RMSE): {rmse:.2f}")
            print(f"  R2 Score: {r2_square:.4f}")

            return r2_square
            
        except Exception as e:
            print(f"Error during model training: {e}")
            raise e