from flask import Flask, request, jsonify
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Logging_Middleware.logger import Log


app = Flask(__name__)

@app.route('/')
def index():
    Log("backend", "info", "route", "Index route was accessed.")
    return "Welcome to the URL Shortener!"

@app.route('/some-action', methods=['POST'])
def some_action():
    data = request.get_json()

    if not data or 'email' not in data:

        Log("backend", "error", "handler", "Request body is missing 'email' field.")
        return jsonify({"error": "Bad Request"}), 400


    Log("backend", "debug", "service", f"Processing action for user: {data['email']}")
    

    
    return jsonify({"message": "Action completed successfully"}), 200

if __name__ == '__main__':
    Log("backend", "info", "config", "Application starting up.")
    app.run(debug=True, port=5000)