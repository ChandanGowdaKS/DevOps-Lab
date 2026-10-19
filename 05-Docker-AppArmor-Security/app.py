from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "active",
        "service": "AppArmor Secured Flask Container",
        "container_id": socket.gethostname(),
        "security_policy": "docker-flask-secure",
        "description": "Running in restricted confinement mode with denied system directories"
    })

@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "pid": os.getpid(),
        "user_uid": os.getuid()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
