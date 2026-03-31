from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Allow cross-origin requests from the React frontend
CORS(app)

todos = [
    {"id": 1, "task": "Understand Jenkins architecture"},
    {"id": 2, "task": "Build React app"},
    {"id": 3, "task": "Deploy artifacts"},
    {"id": 4, "task": "Build Docker Image!!"},
]

@app.route('/api/v1/get-todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

if __name__ == '__main__':
    # Runs on port 5000 by default
    app.run(host='0.0.0.0', port=5000, debug=True)
