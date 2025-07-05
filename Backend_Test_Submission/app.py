from flask import Flask, request, jsonify, redirect
import sys
import os
import string
import random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Logging_Middleware.logger import Log

app = Flask(__name__)

url_db = {}


@app.route('/shorturls', methods=['POST'])
def create_short_url():

    Log("backend", "info", "handler", "Request received to create a new short URL.")
    data = request.get_json()
    if not data or 'url' not in data:
        Log("backend", "error", "handler", "Validation failed: 'url' field is missing from request body.")
        return jsonify({"error": "The 'url' field is required."}), 400

    long_url = data['url']

    if 'shortcode' in data and data['shortcode']:
        shortcode = data['shortcode']
        if shortcode in url_db:
            Log("backend", "warn", "db", f"Collision: Custom shortcode '{shortcode}' already exists.")
            return jsonify({"error": f"Shortcode '{shortcode}' is already in use."}), 409  # 409 Conflict
    else:
        shortcode = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        while shortcode in url_db:
            shortcode = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

    validity_minutes = data.get('validity', 30)
    created_at = datetime.utcnow()
    expires_at = created_at + timedelta(minutes=int(validity_minutes))

    url_db[shortcode] = {
        "long_url": long_url,
        "created_at": created_at.isoformat() + "Z",
        "expires_at": expires_at.isoformat() + "Z",
        "clicks": []
    }

    Log("backend", "info", "service", f"Successfully created shortcode '{shortcode}' for URL: {long_url}")

    response_body = {
        "shortLink": f"{request.host_url}{shortcode}",
        "expiry": expires_at.isoformat() + "Z"
    }
    return jsonify(response_body), 201  # 201 Created

@app.route('/<string:shortcode>')
def handle_redirect(shortcode):

    Log("backend", "info", "route", f"Redirect request received for shortcode: '{shortcode}'")

    if shortcode in url_db:
        entry = url_db[shortcode]
        if datetime.utcnow() > datetime.fromisoformat(entry['expires_at'].replace('Z', '')):
            Log("backend", "warn", "handler", f"Attempted to access expired link with shortcode: '{shortcode}'")
            return jsonify({"error": "This link has expired."}), 404  # 404 Not Found


        click_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source_ip": request.remote_addr,
            "referrer": request.referrer or "Direct"
        }
        entry['clicks'].append(click_data)

        Log("backend", "info", "service", f"Redirecting '{shortcode}' to '{entry['long_url']}'")
        return redirect(entry['long_url'])
    else:
        Log("backend", "warn", "handler", f"Attempted to access non-existent shortcode: '{shortcode}'")
        return jsonify({"error": "Short URL not found."}), 404  # 404 Not Found


@app.route('/shorturls/<string:shortcode>/stats')
def get_stats(shortcode):

    Log("backend", "info", "route", f"Statistics request received for shortcode: '{shortcode}'")
    if shortcode in url_db:
        entry = url_db[shortcode]

        # Prepare the statistics response
        stats_response = {
            "total_clicks": len(entry['clicks']),
            "original_url": entry['long_url'],
            "created_at": entry['created_at'],
            "expires_at": entry['expires_at'],
            "click_details": entry['clicks']
        }
        return jsonify(stats_response), 200
    else:
        Log("backend", "warn", "handler", f"Statistics requested for non-existent shortcode: '{shortcode}'")
        return jsonify({"error": "Short URL not found."}), 404  # 404 Not Found


if __name__ == '__main__':
    Log("backend", "info", "config", "URL Shortener microservice is starting up.")
    app.run(host='0.0.0.0', port=5000, debug=True)
