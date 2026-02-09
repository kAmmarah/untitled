"""
AI in Banking Application
Created by Ammara Dawood
"""

from flask import Flask, render_template, request, jsonify
import json
import os
import random

app = Flask(__name__)

# Simplified AI logic using basic Python instead of heavy ML libraries
def simple_fraud_detection(transaction_data):
    """Simple rule-based fraud detection"""
    risk_score = 0
    
    # High amount transactions
    if transaction_data['transaction_amount'] > 5000:
        risk_score += 0.3
    
    # Unusual timing
    if transaction_data['hour_of_day'] < 6 or transaction_data['hour_of_day'] > 22:
        risk_score += 0.2
    
    # High-risk merchant categories
    high_risk_merchants = [3, 4]  # Online retail, ATM withdrawals
    if transaction_data['merchant_category'] in high_risk_merchants:
        risk_score += 0.25
    
    # Multiple transactions in short time
    if transaction_data['num_transactions_today'] > 5:
        risk_score += 0.15
    
    # Location risk
    risk_score += transaction_data['location_risk_score'] * 0.3
    
    # Weekend transactions (slightly higher risk)
    if transaction_data['is_weekend'] == 1:
        risk_score += 0.1
    
    # Add some randomness for realistic variation
    risk_score += random.uniform(-0.1, 0.1)
    
    is_fraud = risk_score > 0.6
    return {
        'is_fraud': is_fraud,
        'fraud_probability': max(0, min(1, risk_score)),
        'risk_level': 'HIGH' if risk_score > 0.7 else 'MEDIUM' if risk_score > 0.3 else 'LOW'
    }

def simple_loan_approval(loan_data):
    """Simple rule-based loan approval"""
    approval_score = 0
    reasons = []
    
    # Credit score factor (40% weight)
    if loan_data['credit_score'] >= 700:
        approval_score += 0.4
        reasons.append("Excellent credit score")
    elif loan_data['credit_score'] >= 650:
        approval_score += 0.3
        reasons.append("Good credit score")
    elif loan_data['credit_score'] >= 600:
        approval_score += 0.2
        reasons.append("Fair credit score")
    else:
        reasons.append("Low credit score")
    
    # Income factor (25% weight)
    if loan_data['annual_income'] >= 80000:
        approval_score += 0.25
        reasons.append("High income")
    elif loan_data['annual_income'] >= 50000:
        approval_score += 0.15
        reasons.append("Adequate income")
    else:
        reasons.append("Low income")
    
    # Debt-to-income ratio (20% weight)
    if loan_data['debt_to_income'] <= 0.2:
        approval_score += 0.2
        reasons.append("Low debt-to-income ratio")
    elif loan_data['debt_to_income'] <= 0.35:
        approval_score += 0.1
        reasons.append("Reasonable debt-to-income ratio")
    else:
        reasons.append("High debt-to-income ratio")
    
    # Employment length (10% weight)
    if loan_data['employment_length_years'] >= 5:
        approval_score += 0.1
        reasons.append("Stable employment")
    elif loan_data['employment_length_years'] >= 2:
        approval_score += 0.05
    
    # Home ownership (5% weight)
    if loan_data['home_ownership'] in [1, 2]:  # Own or Mortgage
        approval_score += 0.05
        reasons.append("Homeowner")
    
    # Add some randomness for realistic variation
    approval_score += random.uniform(-0.1, 0.1)
    
    is_approved = approval_score > 0.5
    return {
        'approved': is_approved,
        'approval_probability': max(0, min(1, approval_score)),
        'decision_reasons': reasons[:2]  # Top 2 reasons
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualizations')
def show_visualizations():
    # Return simplified visualization data
    return render_template('visualizations.html', 
                         fraud_viz="placeholder_fraud_data",
                         loan_viz="placeholder_loan_data")

@app.route('/api/fraud_detection', methods=['POST'])
def fraud_detection():
    data = request.json
    result = simple_fraud_detection(data)
    return jsonify(result)

@app.route('/api/loan_approval', methods=['POST'])
def loan_approval():
    data = request.json
    result = simple_loan_approval(data)
    return jsonify(result)

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
    print("AI in Banking Application Starting...")
    print("Created by Ammara Dawood")
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))