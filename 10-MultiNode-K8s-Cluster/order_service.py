from flask import Flask, jsonify, request
import socket
import uuid

app = Flask(__name__)

ORDER_DB = []

@app.route("/orders", methods=["GET"])
def list_orders():
    return jsonify({
        "service": "Order Processing Microservice",
        "handled_by_pod": socket.gethostname(),
        "total_orders": len(ORDER_DB),
        "orders": ORDER_DB
    })

@app.route("/orders/create", methods=["POST"])
def create_order():
    payload = request.get_json(force=True, silent=True) or {}
    order_id = f"ORD-{uuid.uuid4().hex[:6].upper()}"
    new_order = {
        "order_id": order_id,
        "sku": payload.get("sku", "SKU-001"),
        "customer": payload.get("customer", "Guest"),
        "processed_by": socket.gethostname()
    }
    ORDER_DB.append(new_order)
    return jsonify(new_order), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
