import time
import json
from abc import ABC, abstractmethod
from pathlib import Path

class Scanner(ABC):
    def __init__(self, network_name: str, db_path: str = "database.json", polling_interval: int = 1800):
        """
        Classe base para scrapers que monitoram carteiras específicas.

        :param network_name: Nome da rede blockchain.
        :param db_path: Caminho do arquivo JSON para armazenamento.
        :param polling_interval: Intervalo entre verificações (em segundos).
        """
        self.network_name = network_name
        self.db_path = Path(db_path)
        self.polling_interval = polling_interval
        self.db_path.touch(exist_ok=True)  # Garante que o arquivo existe
        self.wallets = self.get_monitored_wallets()

    def _load_db(self):
        """Carrega o banco de dados JSON."""
        if self.db_path.stat().st_size == 0:
            return {"monitored_wallets": {}, "transactions": {}}
        with self.db_path.open("r") as f:
            return json.load(f)

    def _save_db(self, data):
        """Salva o banco de dados JSON."""
        with self.db_path.open("w") as f:
            json.dump(data, f, indent=4)

    @abstractmethod
    def fetch_transactions(self, wallet_address):
        """Cada scraper deve implementar a lógica para buscar e processar transações de uma carteira."""
        raise NotImplementedError()

    def get_monitored_wallets(self):
        """Recupera as carteiras cadastradas no JSON para monitoramento."""
        data = self._load_db()
        return data["monitored_wallets"].get(self.network_name, [])

    def get_last_saved_transaction(self, wallet_address):
        """Obtém a última transação salva para uma carteira específica."""
        data = self._load_db()
        transactions = data["transactions"].get(self.network_name, {}).get(wallet_address, [])
        return transactions[-1]["transaction_id"] if transactions else None

    def save_transaction(self, transaction_data):
        """Salva uma nova transação no JSON."""
        data = self._load_db()
        network_transactions = data["transactions"].setdefault(self.network_name, {})
        wallet_transactions = network_transactions.setdefault(transaction_data["wallet"], [])
        
        wallet_transactions.append(transaction_data)
        self._save_db(data)

    def run(self):
        """Executa o scraper em loop, verificando as carteiras monitoradas periodicamente."""
        while True:
            for wallet in self.wallets:
                last_tx = self.get_last_saved_transaction(wallet)
                transactions = self.fetch_transactions(wallet)

                for tx in transactions:
                    if last_tx and tx["transaction_id"] == last_tx:
                        break  # Ignora transações antigas
                    self.save_transaction(tx)
            
            time.sleep(self.polling_interval)
