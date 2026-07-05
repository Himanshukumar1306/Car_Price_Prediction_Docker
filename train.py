import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle

def main():
    print("Loading dataset...")
    # Load dataset
    df = pd.read_csv('car_data.csv')
    
    print("Processing features...")
    # Calculate Age feature using 2020 as reference year
    df['Age'] = 2020 - df['Year']
    
    # Map categorical columns to numerical values
    # Petrol=0, Diesel=1, CNG=2
    df['Fuel_Type_Num'] = df['Fuel_Type'].map({'Petrol': 0, 'Diesel': 1, 'CNG': 2})
    
    # Dealer=0, Individual=1
    df['Seller_Type_Num'] = df['Seller_Type'].map({'Dealer': 0, 'Individual': 1})
    
    # Manual=0, Automatic=1
    df['Transmission_Num'] = df['Transmission'].map({'Manual': 0, 'Automatic': 1})
    
    # Features list matching user inputs in frontend
    features = ['Present_Price', 'Kms_Driven', 'Fuel_Type_Num', 'Seller_Type_Num', 'Transmission_Num', 'Owner', 'Age']
    
    X = df[features]
    y = df['Selling_Price']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Testing set size: {X_test.shape[0]}")
    
    # Initialize and train Random Forest Regressor
    model = RandomForestRegressor(
        n_estimators=150,
        random_state=42,
        max_depth=15,
        min_samples_split=2,
        min_samples_leaf=1
    )
    
    print("Training model...")
    model.fit(X_train, y_train)
    
    # Calculate and display metrics
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"Train R2 Score: {train_score:.4f}")
    print(f"Test R2 Score: {test_score:.4f}")
    
    # Save the model
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model saved to model.pkl successfully!")

if __name__ == '__main__':
    main()
