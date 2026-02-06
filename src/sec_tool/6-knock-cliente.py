import socket
import time
import sys

# --- CONFIGURACOES DO ALVO ---
# Define o IP do servidor (localhost para teste local)
ip_alvo = "127.0.0.1"

# Esta e a "senha" secreta: bater nestas portas por ordem
# Se o servidor receber esta sequencia, abre a porta final
sequencia_secreta = [7000, 8000, 9000]

# Porta onde o servico real esta escondido (ex: site ou chat)
porta_final_servico = 9999

print("--- INICIANDO PROTOCOLO PORT KNOCKING ---")

try:
    # 1. FASE DE BATIDA (KNOCKING)
    # Vamos percorrer a lista de portas da sequencia
    for porta in sequencia_secreta:
        print(f"-> A bater na porta {porta} (UDP)...")
        
        # Cria o socket UDP
        # AF_INET = IPv4
        # SOCK_DGRAM = Protocolo UDP (Referencia: PDF Pagina 3 - UDP Flooding)
        # Usamos UDP porque e mais rapido e nao precisa de resposta (connectionless)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Envia um pacote vazio ou com mensagem curta para a porta
        mensagem = b'KnockKnock'
        s.sendto(mensagem, (ip_alvo, porta))
        
        # Fecha o socket imediatamente (nao esperamos resposta)
        s.close()
        
        # Pequena pausa para garantir que o servidor processa a ordem
        time.sleep(0.5)

    print("--- BATIDAS CONCLUIDAS ---")
    
    # 2. FASE DE CONEXAO
    print(f"A tentar ligar ao servico secreto na porta {porta_final_servico} (TCP)...")
    
    # Agora usamos TCP (SOCK_STREAM) como no Port Scanner (PDF Pagina 2)
    # para tentar aceder ao servico que (esperamos) foi desbloqueado
    s_final = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define um tempo limite de 3 segundos
    s_final.settimeout(3)
    
    # Tenta conectar
    s_final.connect((ip_alvo, porta_final_servico))
    
    # Se conectar, recebe a mensagem de boas-vindas
    dados = s_final.recv(1024)
    print(f"\n[SUCESSO] Resposta do Servidor: {dados.decode()}")
    
    s_final.close()

except socket.error as e:
    # Se falhar (ex: Connection Refused), significa que a porta nao abriu
    print(f"\n[FALHA] Nao foi possivel conectar. A porta {porta_final_servico} ainda esta fechada.")
    print("Verifique se o servidor esta a correr ou se a sequencia esta correta.")