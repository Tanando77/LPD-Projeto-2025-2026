import socket
import subprocess
import sys
from datetime import datetime

# Limpa o terminal (No Windows usa-self 'cls')
subprocess.call('cls', shell=True)

# Entrada de dados do utilizador
rmip = input("\t Enter the remote host IP to scan: ")
r1 = int(input("\t Enter the start port number\t"))
r2 = int(input("\t Enter the last port number\t"))

print(f"\n Scanner is working on {rmip}")

# Registo do tempo de inicio
t1 = datetime.now()

try:
    # O range vai de r1 ate r2 inclusive
    for port in range(r1, r2 + 1):
        # Cria o socket para teste TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Define 1 segundo de espera por porta
        socket.setdefaulttimeout(1)
        
        # Tenta a ligacao
        result = sock.connect_ex((rmip, port))
        
        if result == 0:
            print(f"Porta Aberta:-->\t {port}")
        
        sock.close()

except KeyboardInterrupt:
    print("\n O utilizador parou o processo.")
    sys.exit()

except socket.gaierror:
    print("O Hostname nao pode ser resolvido.")
    sys.exit()

except socket.error:
    print("Nao foi possivel ligar ao servidor.")
    sys.exit()

# Calculo do tempo total
t2 = datetime.now()
total = t2 - t1
print(f"Scan completo em: {total}")
