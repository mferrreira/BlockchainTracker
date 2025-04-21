from flask import Flask, request, jsonify
from db.db import Db
from scrapers.EthScanner import EthScanner
from scrapers.SolScanner import SolScanner
from scrapers.BaseScanner import BaseScanner
import threading

app = Flask(__name__)

# Função para inicializar os scanners
def initialize_scanners():
    return [
        EthScanner(),
        SolScanner(),
        BaseScanner()
    ]

@app.route('/wallets', methods=['GET'])
def get_wallets():
    network = request.args.get('network')
    if not network:
        return jsonify({"error": "Rede não especificada"}), 400

    db = Db()
    wallets = db.get_wallets(network)
    return jsonify(wallets)

@app.route('/wallets', methods=['POST'])
def add_wallet():
    data = request.get_json()
    network = data.get('network')
    wallet_address = data.get('wallet_address')

    if not network or not wallet_address:
        return jsonify({"error": "Rede ou endereço de carteira não fornecidos"}), 400

    db = Db()
    db.add_wallet(network, wallet_address)

    scanners = initialize_scanners()
    for scanner in scanners:
        if scanner.network_name == network:
            threading.Thread(target=scanner.run, daemon=True).start()

    return jsonify({"message": f"Carteira {wallet_address} adicionada com sucesso na rede {network}"}), 201

@app.route('/wallets', methods=['DELETE'])
def remove_wallet():
    data = request.get_json()
    network = data.get('network')
    wallet_address = data.get('wallet_address')

    if not network or not wallet_address:
        return jsonify({"error": "Rede ou endereço de carteira não fornecidos"}), 400

    db = Db()
    wallets = db.get_wallets(network)
    if wallet_address in wallets:
        wallets.remove(wallet_address)
        db._save_db({"wallets": db._load_db()["wallets"], "transactions": db._load_db()["transactions"]})
        return jsonify({"message": f"Carteira {wallet_address} removida com sucesso da rede {network}"}), 200
    else:
        return jsonify({"error": "Carteira não encontrada"}), 404

@app.route('/transactions', methods=['GET'])
def get_transactions():
    network = request.args.get('network')
    if not network:
        return jsonify({"error": "Rede não especificada"}), 400

    db = Db()
    transactions = db.get_transactions(network)
    return jsonify(transactions)

if __name__ == "__main__":
    app.run(debug=True)
