from flask import Flask, jsonify, request
import socket
import time

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "app": "Order Management Service",
        "version": "2.1.0",
        "status": "online",
        "host": socket.gethostname()
    }), 200

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "health": "UP",
        "timestamp": time.time()
    }), 200

@app.route("/api/v1/orders", methods=["GET"])
def list_orders():
    return jsonify({
        "orders_count": 2,
        "items": [
            {"id": "ORD-101", "item": "Keyboard", "status": "Shipped"},
            {"id": "ORD-102", "item": "Mouse", "status": "Pending"}
        ]
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
