from flask import Flask, render_template, request, jsonify
from logic.crypto_utils import decrypt_aes, encrypt_aes
import redis
import json
import os

app = Flask(__name__)

redis_host = os.getenv('REDIS_HOST', 'redis-db')
db = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    text = data.get('text')
    key = data.get('key')
    result = encrypt_aes(text, key)
    
    log_data = json.dumps({"input": text, "output": result['ciphertext']})
    db.lpush('crypto_history', log_data)
    
    return jsonify(result)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    ciphertext = data.get('text')
    key = data.get('key')
    result_text = decrypt_aes(ciphertext, key)
    
    return jsonify({"result": result_text})

@app.route('/save', methods=['POST'])
def save_password():
    data = request.json
    label = data.get('label')
    encrypted_pass = data.get('ciphertext')

    entry = json.dumps({"label": label, "value": encrypted_pass})
    db.lpush('vault_data', entry)
    
    return jsonify({"status": "Success saved to Redis"})

@app.route('/get_vault', methods=['GET'])
def get_vault():
    raw_data = db.lrange('vault_data', 0, -1)
    vault_list = [json.loads(x) for x in raw_data]
    return jsonify(vault_list)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)