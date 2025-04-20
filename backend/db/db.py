import json
import os
import threading
from typing import List, Dict

class Db:
    _instance = None
    _db_path = os.path.join("db", "db.json")  # Corrigido para o caminho correto
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._initialize_db()
        return cls._instance

    @classmethod
    def _initialize_db(cls):
        if not os.path.exists(os.path.dirname(cls._db_path)):
            os.makedirs(os.path.dirname(cls._db_path))
        
        if not os.path.exists(cls._db_path):
            with open(cls._db_path, 'w') as f:
                json.dump({"wallets": {}, "transactions": []}, f, indent=4)

    def _load_db(self) -> Dict:
        # Ler o banco de dados com lock
        with open(self._db_path, 'r') as f:
            return json.load(f)

    def _save_db(self, data: Dict):
        # Salvar o banco de dados com lock
        with open(self._db_path, 'w') as f:
            json.dump(data, f, indent=4)

    def add_wallet(self, network: str, wallet_address: str):
        data = self._load_db()
        if network not in data["wallets"]:
            data["wallets"][network] = []
        if wallet_address not in data["wallets"][network]:
            data["wallets"][network].append(wallet_address)
            self._save_db(data)
        else:
            print(f"Carteira {wallet_address} já está registrada na rede {network}.")

    def get_wallets(self, network: str) -> List[str]:
        # Usando lock para acesso ao banco
        data = self._load_db()
        return data["wallets"].get(network, [])

    def add_transaction(self, transaction_data: Dict):
        with self._lock:
            data = self._load_db()

            # Identifica a rede da transação
            network = transaction_data['network']
            transaction_data.pop('network', None)  # Remove a chave 'network' da transação

            # Verifica se a rede já existe no dicionário de transações
            if network not in data["transactions"]:
                data["transactions"][network] = []

            # Verifica se a transação já existe (checa pelo transaction_id)
            existing_tx = next((tx for tx in data["transactions"][network] if tx['transaction_id'] == transaction_data['transaction_id']), None)
            
            if existing_tx:
                print(f"Transação {transaction_data['transaction_id']} já existe. Ignorando...")
                return  # Ignora se a transação já existir

            # Adiciona a transação à lista de transações daquela rede
            data["transactions"][network].append(transaction_data)

            self._save_db(data)
            
    def get_transactions(self, network) -> List[Dict]:
        data = self._load_db()
        return data["transactions"].get(network, [])
