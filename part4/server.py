#!/usr/bin/env python3
"""
Simple HTTP server for serving the HBnB client files
Usage: python server.py [port]
Default port: 8000
"""

import http.server
import socketserver
import os
import sys

def main():
    # Get port from command line argument or use default
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create handler
    handler = http.server.SimpleHTTPRequestHandler
    
    # Create server
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"HBnB Client Server running at http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    main()