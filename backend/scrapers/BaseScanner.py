from scrapers.Scanner import Scanner
from typing import override
from dotenv import load_dotenv
import requests
import os

load_dotenv()

class BaseScanner(Scanner):

    def __init__(self, ):
        super().__init__('base')
        ...

    @override
    def fetch_transactions(self, wallet_address):
        api_key = os.getenv('BASESCAN_API_KEY')

        url = f'https://api.basescan.org/api\
?module=account\
&action=txlist\
&address={wallet_address}\
&startblock=0\
&endblock=99999999\
&page=1\
&offset=10\
&sort=asc\
&apikey={api_key}'                                

        response = requests.get(url)
        data = response.json()

        if data.get("status") != "1":
            print("Erro na resposta da API:", data.get("message"), "Status:", data.get("status"), "Code:", data.get("result"))
            return

        transactions = []

        for t in data.get("result", []):
            from_address = t.get("from")
            to_address = t.get("to")
            value = int(t.get("value", 0)) / 1e18  # Convertendo de wei para ETH/BASE
            token_symbol = "ETH" if t.get("tokenSymbol") is None else t.get("tokenSymbol")  # Se for uma transação normal, é ETH

            transactions.append({
                'transaction_id': t.get("hash"),
                'wallet': wallet_address,
                'from_address': from_address,
                'to_address': to_address,
                'amount': value,
                'token': token_symbol,
                'block_time': int(t.get("timeStamp", 0))
            })

        return transactions