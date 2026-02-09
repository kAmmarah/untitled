#!/usr/bin/env python3
"""
Script to run the AI in Banking application
"""

import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def install_requirements():
    """Install required packages from requirements.txt"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Packages installed successfully!")
    except subprocess.CalledProcessError:
        print("Error installing packages. Please install manually using: pip install -r requirements.txt")
        sys.exit(1)

def generate_visualizations():
    """Generate visualization images"""
    print("Generating data visualizations...")
    try:
        import visualizations
        # Generate and save visualizations
        fraud_viz = visualizations.create_visualizations()
        loan_viz = visualizations.create_loan_approval_visualizations()
        
        # Save visualizations to static directory
        os.makedirs('static', exist_ok=True)
        
        with open('static/fraud_visualization.png', 'wb') as f:
            f.write(__import__('base64').b64decode(fraud_viz))
        
        with open('static/loan_visualization.png', 'wb') as f:
            f.write(__import__('base64').b64decode(loan_viz))
        
        print("Visualizations created successfully!")
    except Exception as e:
        print(f"Error generating visualizations: {e}")

def run_application():
    """Run the Flask application"""
    print("\nStarting the AI in Banking application...")
    print("Access the application at: http://localhost:5000")
    
    try:
        # Run the Flask app
        subprocess.check_call([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except subprocess.CalledProcessError as e:
        print(f"Error running application: {e}")
        sys.exit(1)

def open_browser():
    """Open the web browser after a delay"""
    time.sleep(3)  # Wait for the server to start
    webbrowser.open("http://localhost:5000")

def main():
    """Main function to set up and run the application"""
    print("AI in Banking Application Setup")
    print("=" * 40)
    
    # Change to the application directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Install requirements
    install_requirements()
    
    # Generate visualizations
    generate_visualizations()
    
    # Start the browser opening in a separate thread
    browser_thread = Thread(target=open_browser)
    browser_thread.start()
    
    # Run the application
    run_application()

if __name__ == "__main__":
    main()