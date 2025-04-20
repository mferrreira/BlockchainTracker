from solana.exceptions import SolanaRpcException
from solders.pubkey import Pubkey
from scrapers.Scanner import Scanner
from solana.rpc.api import Client
from dotenv import load_dotenv
from typing import override
import random
import pprint
import time
import json
import os

load_dotenv()

class SolScanner(Scanner):

    def __init__(self, ):
        super().__init__('solana')
        self._client = Client("https://api.mainnet-beta.solana.com")
        self.backoff = 1  # Inicia o backoff

    @override
    def fetch_transactions(self, wallet_address):
        pubkey = Pubkey.from_string(wallet_address)

        try:
            # Obtém as transações mais recentes
            response = self._client.get_signatures_for_address(pubkey, limit=5)
            details = response.value
            if not details:
                return []

            transactions = []

            for tx in details:
                try:
                    tx_details = self._client.get_transaction(tx.signature, encoding="jsonParsed", max_supported_transaction_version=0)

                    t = json.loads(tx_details.value.to_json())
                    transaction = t.get("transaction", {})
                    message = transaction.get("message", {})

                    instructions = message.get("instructions", [])

                    for instr in instructions:
                        parsed = instr.get("parsed", {})
                        info = parsed.get("info", {})

                        from_address = info.get("source")
                        to_address = info.get("destination")
                        lamports = info.get("lamports")

                        if from_address and to_address and lamports:
                            transactions.append({
                                'transaction_id': str(tx.signature),
                                'wallet': wallet_address,
                                'from_address': str(from_address),
                                'to_address': str(to_address),
                                'amount': str(lamports),
                                'token': "SOL",
                                'block_time': t.get("blockTime")
                            })
                except Exception as e:
                    print(f"Erro ao processar transação {tx.signature}: {e}")
                    continue

            return transactions

        except Exception as e:
            print(f"Erro ao buscar transações: {e}")




if __name__ == "__main__":
    # Teste rápido da classe SolScanner
    sol_scanner = SolScanner()
    wallet_address = "2TmTNypeGeNzHnfssQhpKJWpWnbGTK5TErp3tDmPvQGG"  # Substitua pelo endereço da carteira que deseja testar
    transactions = sol_scanner.fetch_transactions(wallet_address)
    
    if transactions:
        print("Transações obtidas:")
    else: 
        print("Nenhuma transação encontrada ou erro ao obter transações.")