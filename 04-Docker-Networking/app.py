from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "application": "Multi-Tier Web Service",
        "container_name": socket.gethostname(),
        "network": "custom-app-network",
        "available_endpoints": ["/", "/api/status", "/network-info"]
    })

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "online",
        "service": "Flask REST Gateway",
        "connected_tiers": {
            "database": "mysql-db:3306",
            "cache": "redis-cache:6379"
        }
    })

@app.route("/network-info", methods=["GET"])
def network_info():
    return jsonify({
        "hostname": socket.gethostname(),
        "local_ip": socket.gethostbyname(socket.gethostname())
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
