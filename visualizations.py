import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from io import BytesIO
import base64
import os

def generate_sample_data():
    """Generate sample data for visualizations"""
    np.random.seed(42)
    
    # Create fraud detection data
    fraud_data = {
        'transaction_amount': np.random.uniform(1, 10000, 1000),
        'account_age_days': np.random.randint(1, 3650, 1000),
        'num_transactions_today': np.random.randint(1, 20, 1000),
        'hour_of_day': np.random.randint(0, 24, 1000),
        'merchant_category': np.random.randint(0, 5, 1000),
        'is_weekend': np.random.choice([0, 1], 1000),
        'location_risk_score': np.random.uniform(0, 1, 1000)
    }
    
    # Create fraud labels based on some heuristics
    fraud_probability = (
        (fraud_data['transaction_amount'] > 5000) * 0.3 +
        (fraud_data['num_transactions_today'] > 10) * 0.2 +
        (fraud_data['location_risk_score'] > 0.8) * 0.4 +
        np.random.random(1000) * 0.1
    )
    fraud_data['is_fraud'] = (fraud_probability > 0.5).astype(int)
    
    return pd.DataFrame(fraud_data)

def create_visualizations():
    """Create visualizations for the AI banking application"""
    df = generate_sample_data()
    
    # Set up the plotting style
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('AI in Banking - Data Visualizations', fontsize=16, fontweight='bold')
    
    # 1. Fraud Distribution by Transaction Amount
    axes[0, 0].hist(df[df['is_fraud']==0]['transaction_amount'], bins=30, alpha=0.5, label='Legitimate', color='green')
    axes[0, 0].hist(df[df['is_fraud']==1]['transaction_amount'], bins=30, alpha=0.5, label='Fraudulent', color='red')
    axes[0, 0].set_xlabel('Transaction Amount ($)')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_title('Transaction Amount Distribution by Fraud Status')
    axes[0, 0].legend()
    
    # 2. Fraud Rate by Hour of Day
    hourly_fraud_rate = df.groupby('hour_of_day')['is_fraud'].mean()
    axes[0, 1].plot(hourly_fraud_rate.index, hourly_fraud_rate.values, marker='o', color='blue')
    axes[0, 1].set_xlabel('Hour of Day')
    axes[0, 1].set_ylabel('Fraud Rate')
    axes[0, 1].set_title('Fraud Rate by Hour of Day')
    axes[0, 1].grid(True, linestyle='--', alpha=0.6)
    
    # 3. Merchant Category vs Fraud
    fraud_by_merchant = df.groupby('merchant_category')['is_fraud'].mean()
    merchant_labels = ['Grocery', 'Gas Station', 'Restaurant', 'Online Retail', 'ATM']
    axes[1, 0].bar(range(len(merchant_labels)), fraud_by_merchant.values, color='orange', alpha=0.7)
    axes[1, 0].set_xlabel('Merchant Category')
    axes[1, 0].set_ylabel('Fraud Rate')
    axes[1, 0].set_title('Fraud Rate by Merchant Category')
    axes[1, 0].set_xticks(range(len(merchant_labels)))
    axes[1, 0].set_xticklabels(merchant_labels, rotation=45)
    
    # 4. Location Risk vs Fraud
    scatter = axes[1, 1].scatter(df['location_risk_score'], df['transaction_amount'], 
                                 c=df['is_fraud'], cmap='viridis', alpha=0.6)
    axes[1, 1].set_xlabel('Location Risk Score')
    axes[1, 1].set_ylabel('Transaction Amount')
    axes[1, 1].set_title('Location Risk vs Transaction Amount (Colored by Fraud)')
    plt.colorbar(scatter, ax=axes[1, 1], label='Fraud (0=No, 1=Yes)')
    
    plt.tight_layout()
    
    # Save the plot to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    
    # Encode the image to base64 for embedding in HTML
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return img_base64

def create_loan_approval_visualizations():
    """Create visualizations for loan approval data"""
    np.random.seed(42)
    
    # Generate loan data
    loan_data = {
        'credit_score': np.random.randint(300, 850, 1000),
        'annual_income': np.random.uniform(20000, 200000, 1000),
        'debt_to_income': np.random.uniform(0.1, 0.6, 1000),
        'employment_length_years': np.random.uniform(0, 40, 1000),
        'loan_amount': np.random.uniform(5000, 50000, 1000),
        'loan_term_months': np.random.choice([36, 60], 1000),
        'home_ownership': np.random.randint(0, 3, 1000)
    }
    
    # Calculate approval probability based on features
    approval_probability = (
        (loan_data['credit_score'] - 300) / 550 * 0.4 +
        (loan_data['annual_income'] / 200000) * 0.3 +
        (1 - loan_data['debt_to_income']) * 0.2 +
        (loan_data['employment_length_years'] / 40) * 0.1
    )
    loan_data['approved'] = (approval_probability > 0.5).astype(int)
    
    df = pd.DataFrame(loan_data)
    
    # Create visualizations
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Loan Approval Analysis - AI Model Insights', fontsize=16, fontweight='bold')
    
    # 1. Credit Score vs Approval Rate
    credit_bins = pd.cut(df['credit_score'], bins=20)
    approval_by_credit = df.groupby(credit_bins)['approved'].mean()
    axes[0, 0].plot(range(len(approval_by_credit)), approval_by_credit.values, marker='o', color='green')
    axes[0, 0].set_xlabel('Credit Score Range')
    axes[0, 0].set_ylabel('Approval Rate')
    axes[0, 0].set_title('Loan Approval Rate by Credit Score')
    axes[0, 0].grid(True, linestyle='--', alpha=0.6)
    
    # 2. Annual Income vs Approval Rate
    income_bins = pd.cut(df['annual_income'], bins=20)
    approval_by_income = df.groupby(income_bins)['approved'].mean()
    axes[0, 1].plot(range(len(approval_by_income)), approval_by_income.values, marker='o', color='purple')
    axes[0, 1].set_xlabel('Annual Income Range')
    axes[0, 1].set_ylabel('Approval Rate')
    axes[0, 1].set_title('Loan Approval Rate by Annual Income')
    axes[0, 1].grid(True, linestyle='--', alpha=0.6)
    
    # 3. Debt-to-Income vs Approval Rate
    axes[1, 0].scatter(df['debt_to_income'], df['approved'], alpha=0.5, color='red')
    axes[1, 0].set_xlabel('Debt-to-Income Ratio')
    axes[1, 0].set_ylabel('Approved (0=No, 1=Yes)')
    axes[1, 0].set_title('Loan Approval vs Debt-to-Income Ratio')
    
    # 4. Feature Importance (Simulated)
    feature_importance = [0.25, 0.20, 0.30, 0.10, 0.08, 0.05, 0.02]  # Simulated importance
    features = ['Credit Score', 'Annual Income', 'Debt-to-Income', 
                'Employment Length', 'Loan Amount', 'Loan Term', 'Home Ownership']
    axes[1, 1].barh(features, feature_importance, color='skyblue')
    axes[1, 1].set_xlabel('Importance Score')
    axes[1, 1].set_title('Feature Importance in Loan Approval Model')
    
    plt.tight_layout()
    
    # Save the plot to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    
    # Encode the image to base64 for embedding in HTML
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return img_base64

if __name__ == "__main__":
    # Generate visualizations when run directly
    fraud_viz = create_visualizations()
    loan_viz = create_loan_approval_visualizations()
    
    # Save visualizations to files
    os.makedirs('static', exist_ok=True)
    
    with open('static/fraud_visualization.png', 'wb') as f:
        f.write(base64.b64decode(fraud_viz))
    
    with open('static/loan_visualization.png', 'wb') as f:
        f.write(base64.b64decode(loan_viz))
    
    print("Visualizations created and saved to static/ directory")