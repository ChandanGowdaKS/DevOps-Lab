from flask import Flask, jsonify, request
import socket
import random
import time
import uuid

app = Flask(__name__)

DEAL_ITEMS = [
    {"item_id": 101, "name": "Sony WH-1000XM5 Headphones", "price": 24999},
    {"item_id": 102, "name": "Apple Watch Ultra 2", "price": 89900},
    {"item_id": 103, "name": "Mechanical Keyboard RGB", "price": 4500},
    {"item_id": 104, "name": "4K Ultra-Wide Gaming Monitor", "price": 32000}
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "event": "Big Flash Sale 2026",
        "node_hostname": socket.gethostname(),
        "server_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "ready"
    })

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    selected_deal = random.choice(DEAL_ITEMS)
    buyer = request.args.get("buyer", f"customer_{random.randint(1000, 9999)}")
    order_id = uuid.uuid4().hex[:8].upper()

    return jsonify({
        "order_id": order_id,
        "buyer": buyer,
        "product": selected_deal["name"],
        "price_inr": selected_deal["price"],
        "processed_by_pod": socket.gethostname(),
        "status": "CONFIRMED"
    }), 201

@app.route("/healthz", methods=["GET"])
def healthz():
    # Liveness and readiness probe endpoint
    return jsonify({
        "health": "OK",
        "pod": socket.gethostname(),
        "timestamp": time.time()
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
