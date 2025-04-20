from scrapers.EthScanner import EthScanner
from scrapers.SolScanner import SolScanner
from scrapers.BaseScanner import BaseScanner
import threading
import time

def scanner_worker(scanner):
    print(f"🛰️ Iniciando worker para {scanner.network_name}...")

    try:
        while True:
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
            time.sleep(scanner.polling_interval)

    except KeyboardInterrupt:
        print(f"[{scanner.network_name}] Interrompido pelo usuário.")
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

    # Inicia todas as threads simultaneamente
    for scanner in scanners:
        t = threading.Thread(target=scanner_worker, args=(scanner,), daemon=True)
        t.start()
        threads.append(t)
    
    print("✅ Todos os workers iniciados.")

    try:
        while True:
            time.sleep(1)  # Aguardar sem bloquear
    except KeyboardInterrupt:
        print("👋 Encerrando o sistema...")
    
    # Aguarda todas as threads finalizarem ao encerrar o sistema
    for t in threads:
        t.join()

if __name__ == "__main__":
    run_all_workers()

