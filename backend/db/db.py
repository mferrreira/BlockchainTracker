import json
import os
import threading
from typing import List, Dict


class Db:
    _instance = None
    _db_path = "db.json"
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._initialize_db()
        return cls._instance

    @classmethod
    def _initialize_db(cls):
        
        if not os.path.exists(cls._db_path):
            with open(cls._db_path, 'w') as f:
                json.dump({"wallets": {}, "transactions": []}, f, indent=4)

    def _load_db(self) -> Dict:
        
        with self._lock:
            with open(self._db_path, 'r') as f:
                return json.load(f)

    def _save_db(self, data: Dict):
        with self._lock:
            with open(self._db_path, 'w') as f:
                json.dump(data, f, indent=4)

    def add_wallet(self, network: str, wallet_address: str):
        with self._lock:  
            data = self._load_db()
            if network not in data["wallets"]:
                data["wallets"][network] = []
            if wallet_address not in data["wallets"][network]:
                data["wallets"][network].append(wallet_address)
                self._save_db(data)
            else:
                print(f"Carteira {wallet_address} já está registrada na rede {network}.")

    def get_wallets(self, network: str) -> List[str]:
        
        with self._lock: 
            data = self._load_db()
            return data["wallets"].get(network, [])

    def add_transaction(self, transaction_data: Dict):
        
        with self._lock: 
            data = self._load_db()
            data["transactions"].append(transaction_data)
            self._save_db(data)

    def get_transactions(self) -> List[Dict]:
        
        with self._lock: 
            data = self._load_db()
            return data["transactions"]
