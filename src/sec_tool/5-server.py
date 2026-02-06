import socket
import json
import os

# Define a pasta onde as mensagens serao guardadas
PASTA_ARQUIVO = "servidor_ficheiros"
if not os.path.exists(PASTA_ARQUIVO): 
    os.makedirs(PASTA_ARQUIVO)

def gerir_cliente(conn):
    try:
        # Recebe os dados do cliente (ate 20MB para garantir)
        dados_recebidos = conn.recv(20048).decode()
        
        # Se nao receber nada, sai da funcao
        if not dados_recebidos: return
        
        # Converte o texto recebido para dicionario (JSON)
        pedido = json.loads(dados_recebidos)
        acao = pedido['acao']
        usuario = pedido.get('usuario')
        
        # Cria ou verifica a pasta especifica desse usuario
        pasta_user = os.path.join(PASTA_ARQUIVO, usuario)
        if not os.path.exists(pasta_user): 
            os.makedirs(pasta_user)

        resposta = {}

        # --- ACAO: ENVIAR (Guardar mensagem) ---
        if acao == "enviar":
            # Gera um nome de ficheiro sequencial (msg_1, msg_2...)
            numero_msg = len(os.listdir(pasta_user)) + 1
            nome_ficheiro = f"msg_{numero_msg}.json"
            caminho_completo = os.path.join(pasta_user, nome_ficheiro)
            
            # Guarda o conteudo cifrado no ficheiro
            with open(caminho_completo, 'w') as f:
                json.dump(pedido['conteudo'], f)
            
            resposta = {"msg": "Mensagem guardada no servidor com sucesso."}
            print(f"-> Guardei mensagem nova para: {usuario}")

        # --- ACAO: LISTAR (Ver ficheiros) ---
        elif acao == "listar":
            # Le todos os nomes de ficheiros na pasta do usuario
            ficheiros = os.listdir(pasta_user)
            resposta = {"lista": ficheiros}
            print(f"-> {usuario} pediu a lista de mensagens.")

        # --- ACAO: LER (Baixar conteudo) ---
        elif acao == "ler":
            # Le o ficheiro pedido e manda o conteudo de volta
            caminho = os.path.join(pasta_user, pedido['nome_ficheiro'])
            with open(caminho, 'r') as f:
                conteudo = json.load(f)
            resposta = conteudo
            
        # --- ACAO: REMOVER (Apagar ficheiro) ---
        elif acao == "remover":
            caminho = os.path.join(pasta_user, pedido['nome_ficheiro'])
            if os.path.exists(caminho):
                os.remove(caminho)
                resposta = {"msg": "Ficheiro removido."}
            else:
                resposta = {"msg": "Ficheiro nao encontrado."}

        # Envia a resposta de volta ao cliente
        conn.send(json.dumps(resposta).encode())
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# --- CONFIGURACAO DO SOCKET ---
# Cria o socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Liga o servidor no localhost, porta 9999
s.bind(('localhost', 9999))
# Comeca a escutar (permite 5 em espera)
s.listen(5)

print("=== SERVIDOR DE MENSAGENS ATIVO ===")
print("Pressione CTRL+C para parar.")

while True:
    # Fica bloqueado a espera de uma conexao
    conn, addr = s.accept() 
    # Quando alguem se conecta, trata do pedido
    gerir_cliente(conn)
    # Fecha a conexao
    conn.close()