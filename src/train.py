# src/train.py
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def generate_mock_data(samples=2000):
    """Generates a synthetic loan applicant dataset."""
    np.random.seed(42)
    income = np.random.randint(20000, 150000, size=samples)
    credit_score = np.random.randint(300, 850, size=samples)
    loan_amount = np.random.randint(5000, 50000, size=samples)
    
    # Operational rule for default probability
    default_prob = (1.0 - (credit_score / 850.0)) * 0.6 + (loan_amount / income) * 0.4
    default = (default_prob > 0.5).astype(int)
    
    df = pd.DataFrame({
        'income': income,
        'credit_score': credit_score,
        'loan_amount': loan_amount,
        'default': default
    })
    return df

def train_pipeline():
    print("Step 1: Fetching and parsing dataset...")
    df = generate_mock_data()
    
    X = df[['income', 'credit_score', 'loan_amount']]
    y = df['default']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Step 2: Initializing and fitting RandomForest model...")
    model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluation
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, predictions))
    
    # Save Model Asset
    os.makedirs('models', exist_ok=True)
    model_path = 'models/loan_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model successfully optimized and serialized to {model_path}")

if __name__ == '__main__':
    train_pipeline()