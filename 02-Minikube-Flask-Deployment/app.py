from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Zepto Product Catalog Microservice",
        "status": "UP",
        "container_id": socket.gethostname(),
        "environment": os.environ.get("ENV", "development"),
        "message": "Welcome to Zepto fast-delivery catalog API on Kubernetes!"
    })

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "hostname": socket.gethostname()
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
