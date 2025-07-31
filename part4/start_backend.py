#!/usr/bin/env python3
"""
Simple script to start the HBnB backend server
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        print("Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "hbnb/requirements.txt"])
        print("Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        sys.exit(1)

def start_server():
    """Start the Flask server"""
    try:
        print("\nStarting HBnB backend server on http://localhost:5000")
        print("API documentation available at: http://localhost:5000/api/v1/")
        print("Press Ctrl+C to stop the server\n")
        
        # Change to the hbnb directory
        os.chdir("hbnb")
        
        # Start the server
        subprocess.run([sys.executable, "run.py"])
        
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    print("HBnB Backend Server Startup Script")
    print("=" * 40)
    
    install_requirements()
    start_server()