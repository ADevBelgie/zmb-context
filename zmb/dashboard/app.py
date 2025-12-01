from flask import Flask, render_template, jsonify
import json
import os
import sys

# Ensure zmb package is in path
sys.path.append(os.getcwd())

from zmb.state import STATE_FILE

app = Flask(__name__)

def get_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def get_logs(lines=50):
    log_file = 'zmb.log'
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            return f.readlines()[-lines:]
    return []

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/data')
def api_data():
    return jsonify({
        'state': get_state(),
        'logs': get_logs()
    })

if __name__ == '__main__':
    print("Starting ZMB Dashboard on http://localhost:5000")
    app.run(debug=True, port=5000)
