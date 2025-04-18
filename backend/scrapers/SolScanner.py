from solana.exceptions import SolanaRpcException
from solders.pubkey import Pubkey
from Scanner import Scanner
from solana.rpc.api import Client
from dotenv import load_dotenv
from typing import override
import random
import pprint
import time
import os

load_dotenv()

class SolScanner(Scanner):

    def __init__(self, ):
        super().__init__('solana')
        self._client = Client("https://api.mainnet-beta.solana.com")

    @override
    def fetch_transactions(self, wallet_address):
        pubkey = Pubkey.from_string(wallet_address)

        try:
            response = self._client.get_signatures_for_address(pubkey, limit=5)
            if not response.value:
                return []
            for tx in response.value:
                tx_details = self._client.get_transaction(tx.signature, encoding="jsonParsed", max_supported_transaction_version=0)
                pprint.pprint(tx_details.value)

            
        except SolanaRpcException as e:
            if "429" in str(e):
                wait_time = backoff + random.uniform(0, 0.5)
                print(f"[Rate Limit] Aguardando {wait_time:.2f}s...")
                time.sleep(wait_time)
                backoff *= 2  # Exponential backoff
            else:
                print("Falha ao obter assinaturas, desistindo.")
                return []

        transactions = []




if __name__ == '__main__':
    c = SolScanner()
    res = c.fetch_transactions('2TmTNypeGeNzHnfssQhpKJWpWnbGTK5TErp3tDmPvQGG')
    print(res)