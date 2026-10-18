from flask import Flask, jsonify, request
import socket

app = Flask(__name__)

INVENTORY_ITEMS = [
    {"sku": "SKU-001", "name": "Apple MacBook Pro 14", "quantity": 15, "warehouse": "BLR-01"},
    {"sku": "SKU-002", "name": "Logitech MX Master 3S", "quantity": 42, "warehouse": "BLR-02"},
    {"sku": "SKU-003", "name": "Keychron Q1 Pro Wireless", "quantity": 28, "warehouse": "BLR-01"}
]

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify({
        "service": "Inventory Management Microservice",
        "served_by_node": socket.gethostname(),
        "total_sku_count": len(INVENTORY_ITEMS),
        "items": INVENTORY_ITEMS
    })

@app.route("/inventory/stock/<sku>", methods=["GET"])
def check_stock(sku):
    item = next((i for i in INVENTORY_ITEMS if i["sku"].lower() == sku.lower()), None)
    if item:
        return jsonify({"found": True, "item": item, "node": socket.gethostname()})
    return jsonify({"found": False, "message": "SKU not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
