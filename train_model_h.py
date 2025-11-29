import pandas as pd
import numpy as np
import statsmodels.api as sm
import joblib 

CLEANED_FILE = 'final_feature_set.csv'
MODEL_FILE = 'traffic_predictor_model.pkl'

def train_and_save_model_adapted():
    print("🧠 Starting FINAL Model Training...")
    
    try:
        df = pd.read_csv(CLEANED_FILE)
        
        # Define Features (X) and Target (Y)
        df['X_Feature'] = df.index.values 
        
        # StatsModels requires an 'intercept' for the regression
        X = sm.add_constant(df[['X_Feature']]) 
        Y = df['Traffic_Score']
        
        # Train the Model (The final AI step!)
        model = sm.OLS(Y, X)
        results = model.fit() 
        
        # Score and Save
        score = results.rsquared
        joblib.dump(results, MODEL_FILE)
        
        print("✅ FINAL Model Training Successful! 🎉")
        print(f"   The model accuracy (R-squared score) is: {score:.4f}")
        print(f"   Trained AI Model saved to: {MODEL_FILE}")
        
    except Exception as e:
        print(f"❌ Critical Error during training: {e}")
        
if __name__ == "__main__":
    train_and_save_model_adapted()
