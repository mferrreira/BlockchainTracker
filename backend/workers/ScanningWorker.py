from scrapers.EthScanner import EthScanner
from scrapers.SolScanner import SolScanner
from scrapers.BaseScanner import BaseScanner
from scrapers.Scanner import Scanner
import threading
import time
stop_event = threading.Event()

def scanner_worker(scanner: Scanner, stop_event):
    print(f"[WORKERS] Iniciando worker para {scanner.network_name}...")

    try:
        while not stop_event.is_set():
            for wallet in scanner.wallets:
                print(f"[{scanner.network_name}] Verificando transações da carteira {wallet}")
                
                last_tx = scanner.get_last_saved_transaction(wallet)
                transactions = scanner.fetch_transactions(wallet)

                for tx in transactions:
                    if last_tx and tx["transaction_id"] == last_tx:
                        print(f"[{scanner.network_name}] Transação {tx['transaction_id']} já salva. Ignorando.")
                        break
                    
                    print(f"[{scanner.network_name}] Salvando transação {tx['transaction_id']}")
                    scanner.save_transaction(tx)

            print(f"[{scanner.network_name}] Aguardando {scanner.polling_interval}s...")
            stop_event.wait(timeout=scanner.polling_interval)

    except Exception as e:
        print(f"[{scanner.network_name}] Erro: {e}")
    finally:
        print(f"[{scanner.network_name}] Finalizando...")

def run_all_workers():
    scanners = [
        EthScanner(),
        BaseScanner(),
        SolScanner()
    ]

    threads = []

    for scanner in scanners:
        t = threading.Thread(target=scanner_worker, args=(scanner, stop_event), daemon=True)
        t.start()
        threads.append(t)
    
    print("[WORKERS] Todos os workers iniciados.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[WORKERS] Encerrando o sistema...")
        stop_event.set()
        for t in threads:
            t.join()
        print("[WORKERS] Todos os workers finalizados.")

if __name__ == "__main__":
    run_all_workers()