#!/usr/bin/env python3
"""
Scanner de Portas TCP Rápido (Threaded)
Utiliza 'socket' para varredura e 'concurrent.futures' para paralelismo.
"""

import socket
import sys
import time
from datetime import datetime
import concurrent.futures

def scan_single_port(target_ip: str, port: int, timeout: float):
    """
    Tenta conectar a uma única porta. Retorna a porta se estiver aberta, ou None se fechada/filtrada.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    
    try:
        result = s.connect_ex((target_ip, port))
        if result == 0:
            return port
    except (socket.timeout, socket.error):
        pass
    finally:
        s.close()
        
    return None

def scan_ports(target_host: str, start_port: int, end_port: int, timeout: float = 1.0, max_threads: int = 100):
    """
    Escaneia um intervalo de portas utilizando múltiplas threads para maior velocidade.
    """
    try:
        target_ip = socket.gethostbyname(target_host)
    except socket.gaierror:
        print(f"[-] Erro: Não foi possível resolver o endereço de '{target_host}'.")
        return

    print("=" * 60)
    print(f"Iniciando Fast TCP Port Scanner")
    print(f"Alvo: {target_host} ({target_ip})")
    print(f"Intervalo: {start_port} até {end_port}")
    print(f"Threads: {max_threads}")
    print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    open_ports = []
    start_time = time.time()

    # O ThreadPoolExecutor gerencia um "pool" (piscina) de threads (trabalhadores).
    # max_workers define quantas portas serão testadas simultaneamente.
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Cria um dicionário mapeando cada "promessa" de execução (future) para a sua porta correspondente
        futures = {
            executor.submit(scan_single_port, target_ip, port, timeout): port 
            for port in range(start_port, end_port + 1)
        }

        # as_completed permite que os resultados sejam processados assim que cada thread termina,
        # independentemente da ordem em que foram iniciadas.
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port is not None:
                print(f"[+] Porta {port:5d}/TCP : ABERTA")
                open_ports.append(port)

    # Ordena a lista no final, já que as threads terminam fora de ordem
    open_ports.sort()
    
    total_time = time.time() - start_time
    print("=" * 60)
    print(f"Varredura finalizada em {total_time:.2f} segundos.")
    if open_ports:
        print(f"Portas abertas encontradas: {open_ports}")
    else:
        print("Nenhuma porta aberta foi encontrada no intervalo especificado.")
    print("=" * 60)

def main():
    # Atualizamos os argumentos para suportar o número de threads
    if len(sys.argv) >= 4:
        target = sys.argv[1]
        start_port = int(sys.argv[2])
        end_port = int(sys.argv[3])
        timeout = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        threads = int(sys.argv[5]) if len(sys.argv) > 5 else 100
    else:
        target = input("Informe o IP ou host alvo (ex: 127.0.0.1): ").strip() or "127.0.0.1"
        start_port = int(input("Porta inicial (ex: 1): ") or 1)
        end_port = int(input("Porta final (ex: 1024): ") or 1024)
        timeout = float(input("Timeout em seg (padrão 1.0): ") or 1.0)
        threads = int(input("Número de threads (padrão 100): ") or 100)

    scan_ports(target, start_port, end_port, timeout, threads)

if __name__ == "__main__":
    main()