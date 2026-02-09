from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import json
import os
from visualizations import create_visualizations, create_loan_approval_visualizations

app = Flask(__name__)

# Sample data generators for demonstration
def generate_sample_transaction_data(n_samples=1000):
    """Generate sample transaction data for fraud detection"""
    np.random.seed(42)
    data = {
        'transaction_amount': np.random.uniform(1, 10000, n_samples),
        'account_age_days': np.random.randint(1, 3650, n_samples),
        'num_transactions_today': np.random.randint(1, 20, n_samples),
        'hour_of_day': np.random.randint(0, 24, n_samples),
        'merchant_category': np.random.randint(0, 5, n_samples),
        'is_weekend': np.random.choice([0, 1], n_samples),
        'location_risk_score': np.random.uniform(0, 1, n_samples)
    }
    
    # Create fraud labels based on some heuristics
    fraud_probability = (
        (data['transaction_amount'] > 5000) * 0.3 +
        (data['num_transactions_today'] > 10) * 0.2 +
        (data['location_risk_score'] > 0.8) * 0.4 +
        np.random.random(n_samples) * 0.1
    )
    data['is_fraud'] = (fraud_probability > 0.5).astype(int)
    
    return pd.DataFrame(data)

def generate_sample_loan_data(n_samples=1000):
    """Generate sample loan application data"""
    np.random.seed(42)
    data = {
        'credit_score': np.random.randint(300, 850, n_samples),
        'annual_income': np.random.uniform(20000, 200000, n_samples),
        'debt_to_income': np.random.uniform(0.1, 0.6, n_samples),
        'employment_length_years': np.random.uniform(0, 40, n_samples),
        'loan_amount': np.random.uniform(5000, 50000, n_samples),
        'loan_term_months': np.random.choice([36, 60], n_samples),
        'home_ownership': np.random.randint(0, 3, n_samples)
    }
    
    # Calculate approval probability based on features
    approval_probability = (
        (data['credit_score'] - 300) / 550 * 0.4 +
        (data['annual_income'] / 200000) * 0.3 +
        (1 - data['debt_to_income']) * 0.2 +
        (data['employment_length_years'] / 40) * 0.1
    )
    data['approved'] = (approval_probability > 0.5).astype(int)
    
    return pd.DataFrame(data)

# Initialize models
fraud_model = None
loan_model = None

def train_models():
    global fraud_model, loan_model
    
    # Train fraud detection model
    fraud_data = generate_sample_transaction_data(1000)
    X_fraud = fraud_data.drop(['is_fraud'], axis=1)
    y_fraud = fraud_data['is_fraud']
    
    fraud_model = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=10)
    fraud_model.fit(X_fraud, y_fraud)
    
    # Train loan approval model
    loan_data = generate_sample_loan_data(1000)
    X_loan = loan_data.drop(['approved'], axis=1)
    y_loan = loan_data['approved']
    
    loan_model = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=10)
    loan_model.fit(X_loan, y_loan)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualizations')
def show_visualizations():
    fraud_viz = create_visualizations()
    loan_viz = create_loan_approval_visualizations()
    return render_template('visualizations.html', fraud_viz=fraud_viz, loan_viz=loan_viz)

@app.route('/api/fraud_detection', methods=['POST'])
def fraud_detection():
    data = request.json
    
    # Prepare input for prediction
    input_features = np.array([[
        data['transaction_amount'],
        data['account_age_days'],
        data['num_transactions_today'],
        data['hour_of_day'],
        data['merchant_category'],
        data['is_weekend'],
        data['location_risk_score']
    ]])
    
    # Make prediction
    prediction = fraud_model.predict(input_features)[0]
    probability = fraud_model.predict_proba(input_features)[0][1]
    
    return jsonify({
        'is_fraud': bool(prediction),
        'fraud_probability': float(probability),
        'risk_level': 'HIGH' if probability > 0.7 else 'MEDIUM' if probability > 0.3 else 'LOW'
    })

@app.route('/api/loan_approval', methods=['POST'])
def loan_approval():
    data = request.json
    
    # Prepare input for prediction
    input_features = np.array([[
        data['credit_score'],
        data['annual_income'],
        data['debt_to_income'],
        data['employment_length_years'],
        data['loan_amount'],
        data['loan_term_months'],
        data['home_ownership']
    ]])
    
    # Make prediction
    prediction = loan_model.predict(input_features)[0]
    probability = loan_model.predict_proba(input_features)[0][1]
    
    return jsonify({
        'approved': bool(prediction),
        'approval_probability': float(probability),
        'decision_reasons': get_loan_decision_reasons(data)
    })

def get_loan_decision_reasons(applicant_data):
    """Generate reasons for loan approval/rejection"""
    reasons = []
    
    if applicant_data['credit_score'] < 600:
        reasons.append("Low credit score")
    elif applicant_data['credit_score'] > 750:
        reasons.append("Excellent credit score")
    
    if applicant_data['debt_to_income'] > 0.4:
        reasons.append("High debt-to-income ratio")
    elif applicant_data['debt_to_income'] < 0.2:
        reasons.append("Low debt-to-income ratio")
        
    if applicant_data['annual_income'] < 40000:
        reasons.append("Low annual income")
    elif applicant_data['annual_income'] > 100000:
        reasons.append("High annual income")
        
    return reasons[:2]  # Return top 2 reasons

@app.route('/api/chatbot', methods=['POST'])
def chatbot_response():
    data = request.json
    user_message = data.get('message', '').lower()
    
    # Simple rule-based responses for banking queries
    responses = {
        'balance': 'Your account balance is $2,540.32.',
        'transactions': 'You have 5 transactions this week: $25.40 at Coffee Shop, $67.89 at Supermarket, $45.00 gas station, $12.50 online purchase, $120.00 rent payment.',
        'hours': 'Our branches are open Monday-Friday 9AM-5PM, Saturday 10AM-2PM. Our online services are available 24/7.',
        'fees': 'There are no monthly maintenance fees if your balance stays above $1,500. ATM fees are $2.50 for out-of-network ATMs.',
        'contact': 'You can reach our customer service at 1-800-BANK-HELP or visit our website for live chat support.',
        'default': 'Thank you for your inquiry. I\'ve forwarded your question to a customer service representative who will contact you shortly.'
    }
    
    for keyword, response in responses.items():
        if keyword in user_message and keyword != 'default':
            return jsonify({'response': response})
    
    return jsonify({'response': responses['default']})

if __name__ == '__main__':
    print("Training models...")
    train_models()
    print("Models trained successfully!")
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))