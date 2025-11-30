from flask import Flask, render_template, jsonify
import requests
from datetime import timezone, timedelta

app = Flask(__name__)

API_BASE = "https://femboy-banner.vercel.app/api/banner"

# Kyrgyzstan timezone UTC+6
KG_TZ = timezone(timedelta(hours=6))

@app.route('/')
def index():
    return render_template('index.html')

# Match frontend expected path: /api/banner/<mode>/s444
@app.route('/api/banner/<mode>/s444')
def banner_data(mode):
    if mode not in ('sg', 'cis'):
        return jsonify({"error": "Invalid mode"}), 400

    url = f"{API_BASE}/{mode}/s444"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        # Convert the API data to the format frontend expects
        banners = []
        for key, val in data.items():
            if isinstance(val, dict) and "messages" in val:
                for msg in val["messages"]:
                    banners.append({
                        "name": msg.get("title"),
                        "url": msg.get("image_url"),
                        "region": msg.get("region"),
                        "timestamp": int(msg.get("start_time")) if msg.get("start_time") else None
                    })

        return jsonify({"banners": banners})

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
