import pandas as pd
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def train_and_save_complex_model():
    print("⚙️  Initializing Training Sequence...")
    
    # 1. Load Data
    try:
        df = pd.read_csv("ayurvedic_dosha_dataset.csv")
    except FileNotFoundError:
        print("❌ Error: Dataset not found!")
        return

    # 2. Advanced Encoding (Saving encoders to handle user input later)
    encoders = {}
    for col in df.columns:
        # We use LabelEncoder, but in a real complex app, 
        # we might map specific ordinal values (e.g., Low=1, Med=2, High=3)
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    # 3. Split Features and Target
    X = df.drop('dosha', axis=1)
    y = df['dosha']

    # 4. Train a robust Random Forest
    # n_estimators=200 increases complexity/stability
    # min_samples_split prevents overfitting on tiny details
    model = RandomForestClassifier(n_estimators=200, min_samples_split=5, random_state=42)
    model.fit(X, y)

    # 5. Save the "Brain" (Model) and "Dictionary" (Encoders)
    joblib.dump(model, 'dietveda_complex_model.pkl')
    joblib.dump(encoders, 'dietveda_encoders.pkl')
    
    print("✅ Model trained successfully.")
    print("✅ Model saved as 'dietveda_complex_model.pkl'")
    print("🔒 Technical details (Confusion Matrix) hidden from user interface.")

if __name__ == "__main__":
    train_and_save_complex_model()