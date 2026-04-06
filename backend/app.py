from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sqlite3

app = Flask(__name__)
CORS(app)

# VULNERABILITY 1: Hardcoded AWS Secret (SonarQube Security Hotspot/Blocker)
AWS_SECRET_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"

todos = [
    {"id": 1, "task": "Understand Jenkins architecture"},
    {"id": 2, "task": "Build React app"},
    {"id": 3, "task": "Deploy artifacts"},
    {"id": 4, "task": "Build Docker Image!!"},
]

@app.route('/api/v1/get-todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

# VULNERABILITY 2: Blind Command Injection (Critical RCE)
# An attacker can pass ?target=127.0.0.1;cat /etc/passwd
@app.route('/api/v1/ping', methods=['GET'])
def ping_server():
    target = request.args.get('target', '127.0.0.1')
    os.system(f"ping -c 1 {target}") # Directly executing unescaped user input
    return jsonify({"status": "ping executed"})

# VULNERABILITY 3: SQL Injection (Critical)
# An attacker can pass ?id=1' OR '1'='1
@app.route('/api/v1/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id', '1')
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    # Dangerous string concatenation instead of parameterized queries
    cursor.execute("SELECT * FROM users WHERE id = '" + user_id + "'")
    return jsonify({"status": "query executed"})

if __name__ == '__main__':
    # VULNERABILITY 4: Running Debug mode in production (Security Hotspot)
    app.run(host='0.0.0.0', port=5000, debug=True)
