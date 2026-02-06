import socket
import time

# --- CONFIGURACOES ---
# A sequencia que o servidor espera ouvir
sequencia_esperada = [7000, 8000, 9000]

# Porta que sera aberta se a sequencia for correta
porta_secreta = 9999

# Funcao auxiliar para esperar por um pacote UDP numa porta especifica
def esperar_batida_udp(porta):
    try:
        # Cria socket UDP (Baseado no PDF Pagina 3)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Liga o socket ao endereco local e a porta desejada
        # '0.0.0.0' significa que escuta de qualquer IP
        s.bind(('0.0.0.0', porta))
        
        print(f"[BLOQUEADO] A espera de batida na porta {porta}...")
        
        # Fica parado aqui ate receber dados (buffer de 1024 bytes)
        dados, endereco = s.recvfrom(1024)
        
        print(f"-> Recebi sinal de {endereco} na porta {porta}!")
        
        # Fecha o socket para libertar a porta e seguir em frente
        s.close()
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False

# Funcao para abrir o servico secreto (TCP) temporariamente
def abrir_servico_secreto():
    print(f"\n>>> SEQUENCIA CORRETA! ABRINDO PORTA {porta_secreta} <<<")
    
    # Cria socket TCP (Baseado no PDF Pagina 2)
    servico = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servico.bind(('0.0.0.0', porta_secreta))
    servico.listen(1)
    
    # Define um timeout: a porta so fica aberta por 10 segundos
    servico.settimeout(10)
    
    try:
        print("A aguardar conexao do cliente (tem 10 segundos)...")
        conn, addr = servico.accept()
        print(f"Cliente conectado: {addr}")
        
        msg = "ACESSO AUTORIZADO! Bem-vindo ao sistema secreto."
        conn.send(msg.encode())
        conn.close()
    except socket.timeout:
        print("Tempo esgotado. Ninguem se conectou.")
    
    servico.close()
    print(">>> PORTA SECRETA FECHADA NOVAMENTE <<<\n")

# --- LOOP PRINCIPAL DO SERVIDOR ---
print("=== SERVIDOR PORT KNOCKING ATIVO ===")

while True:
    # Passo 1: Espera pela primeira porta (7000)
    if esperar_batida_udp(sequencia_esperada[0]):
        
        # Passo 2: Espera pela segunda porta (8000)
        # Nota: Num sistema real haveria timeouts entre passos
        if esperar_batida_udp(sequencia_esperada[1]):
            
            # Passo 3: Espera pela terceira porta (9000)
            if esperar_batida_udp(sequencia_esperada[2]):
                
                # Se chegou aqui, a sequencia foi completa!
                abrir_servico_secreto()
            else:
                print("Sequencia quebrada no passo 3.")
        else:
            print("Sequencia quebrada no passo 2.")