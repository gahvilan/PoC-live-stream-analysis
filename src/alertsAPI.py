from flask import Flask, jsonify, request
import threading
import time


class AlertService:
    def __init__(self, port=5000 , host="0.0.0.0"):
        self.alerts = []
        self.app = Flask(__name__)
        self.port = port
        self.host = host
        # Register routes
        self.app.add_url_rule("/alerts", "get_alerts", self.get_alerts_list, methods=["GET"])
        self.app.add_url_rule("/alerts", "add_alert", self.add_alert, methods=["POST"])
        self.app.add_url_rule("/version", "version", self.get_version, methods=["GET"])

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
