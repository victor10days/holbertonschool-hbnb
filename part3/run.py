#!/usr/bin/env python3
"""
Entry point script for the HBnB application.
Runs the Flask development server.
"""
from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
