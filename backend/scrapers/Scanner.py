from abc import ABC, abstractmethod
from db.db import Db 
import time

class Scanner(ABC):
    def __init__(self, network_name: str, polling_interval: int = 1800):
        print(f"[{network_name}] Inicializando scanner...")
        self.network_name = network_name
        self.polling_interval = polling_interval
        self.db = Db()
        self.wallets = self.db.get_wallets(self.network_name)
        print(f"[{network_name}] Scanner inicializado com {len(self.wallets)} carteiras monitoradas.")

    @abstractmethod
    def fetch_transactions(self, wallet_address):
        raise NotImplementedError()

    def save_transaction(self, transaction_data):
        """Salva uma transação no banco de dados."""
        transaction_data["network"] = self.network_name
        transaction_data["block_time"] = int(transaction_data["block_time"])
        self.db.add_transaction(transaction_data)


    def get_last_saved_transaction(self, wallet_address):
        all_txs = self.db.get_transactions(self.network_name)
        wallet_txs = [t for t in all_txs if t["wallet"] == wallet_address and t["token"].lower() == self.network_name.lower()]
        if not wallet_txs:
            return None
        return sorted(wallet_txs, key=lambda x: x["block_time"], reverse=True)[0]["transaction_id"]

    def run(self):
        """Executa o scraper em loop, verificando as carteiras monitoradas periodicamente."""
        while True:
            print(f"[{self.network_name}] Rodando scanner para {len(self.wallets)} carteiras.")
            for wallet in self.wallets:
                try:
                    print(f"[{self.network_name}] Verificando carteira: {wallet}")
                    last_tx = self.get_last_saved_transaction(wallet)
                    transactions = self.fetch_transactions(wallet)

                    if not transactions:
                        print(f"[{self.network_name}] Nenhuma transação encontrada para {wallet}")
                        continue

                    new_txs = []

                    for tx in reversed(transactions):  # do mais antigo pro mais novo
                        if last_tx and tx["transaction_id"] == last_tx:
                            break  # Parou, já temos essa salva
                        new_txs.insert(0, tx)  # Inserindo no início pra manter ordem correta

                    if new_txs:
                        for tx in new_txs:
                            self.save_transaction(tx)
                            print(f"[{self.network_name}] Nova transação salva: {tx['transaction_id']}")

                    else:
                        print(f"[{self.network_name}] Nenhuma nova transação pra {wallet}")

                except Exception as e:
                    print(f"[{self.network_name}] Erro ao processar {wallet}: {e}")

            print(f"[{self.network_name}] Aguardando {self.polling_interval} segundos...\n")
            time.sleep(self.polling_interval)