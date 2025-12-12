from flask import Flask, jsonify, request
import threading
import time
import json
import os
from config import OUTPUT_ALERTS_DIR


class AlertService:
    def __init__(self, port=5001 , host="0.0.0.0"):
        self.alerts = []
        self.app = Flask(__name__)
        self.port = port
        self.host = host
        # Register routes
        self.app.add_url_rule("/alerts", "get_alerts", self.get_alerts_list, methods=["GET"])
        self.app.add_url_rule("/alerts", "add_alert", self.add_alert, methods=["POST"])
        self.app.add_url_rule("/version", "version", self.get_version, methods=["GET"])
        self.app.add_url_rule("/alerts/file", "get_alerts_file", self.get_alerts_from_file, methods=["GET"])

    # -----------------------------------------
    # REST API Methods
    # -----------------------------------------
    def set_alerts(self, alerts):
        self.alerts = alerts
        
    def get_alerts_list(self):
        return jsonify({"alerts": self.alerts})

    def add_alert(self):
        data = request.json
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        self.alerts.append(data)
        return jsonify({"status": "ok"})

    def get_version(self):
        return jsonify({"version": "1.0.0", "time": time.time()})

    def get_alerts_from_file(self):
        json_path = f"{OUTPUT_ALERTS_DIR}/alerts.json"
        if not os.path.exists(json_path):
             return jsonify({"alerts": []})
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
            return jsonify({"alerts": data})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # -----------------------------------------
    # Run Flask in a background thread
    # -----------------------------------------

    def run(self):
        thread = threading.Thread(
            target=lambda: self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False),
            daemon=True
        )
        thread.start()
        return thread
