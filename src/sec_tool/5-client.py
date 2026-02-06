import socket
import json
import importlib

# Importa o nosso modulo de criptografia (5-crypto.py)
ferramentas = importlib.import_module("5-crypto")

# Funcao auxiliar para enviar dados ao servidor e receber resposta
def falar_com_servidor(dados):
    # Cria socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta a porta 9999 (onde o servidor esta)
    s.connect(('localhost', 9999))
    # Envia os dados em formato JSON
    s.send(json.dumps(dados).encode())
    # Fica a espera da resposta (ate 20MB)
    resposta = s.recv(20048).decode()
    s.close()
    # Converte resposta de JSON para dicionario
    return json.loads(resposta)

# --- INICIO DO PROGRAMA ---
meu_nome = input("Digite o seu nome de utilizador: ")

# Garante que as chaves RSA existem para este usuario
ferramentas.verificar_chaves(meu_nome)

while True:
    print(f"\n--- BEM-VINDO {meu_nome.upper()} ---")
    print("1. Enviar mensagem segura")
    print("2. Ver minha Caixa de Entrada")
    print("3. Fazer Backup das minhas mensagens")
    print("0. Sair")
    
    opcao = input("Escolha uma opcao: ")

    # OPCAO 1: ENVIAR
    if opcao == "1":
        destinatario = input("Para quem quer enviar? ")
        mensagem_texto = input("Escreva a mensagem: ")
        
        # 1. Encriptar a mensagem localmente (no computador do cliente)
        # Isto garante que o servidor so recebe lixo cifrado
        pacote_cifrado = ferramentas.encriptar_mensagem(destinatario, mensagem_texto)
        
        if pacote_cifrado:
            # 2. Enviar o pacote cifrado para o servidor guardar
            resp = falar_com_servidor({
                'acao': 'enviar', 
                'usuario': destinatario, 
                'conteudo': pacote_cifrado
            })
            print(f"Servidor diz: {resp['msg']}")
        else:
            print("ERRO: Nao encontrei a chave Publica desse utilizador.")
            print("Dica: Pecam a essa pessoa para correr este programa uma vez.")

    # OPCAO 2: LER CAIXA DE ENTRADA
    elif opcao == "2":
        # 1. Pede a lista de ficheiros ao servidor
        resp = falar_com_servidor({'acao': 'listar', 'usuario': meu_nome})
        lista_ficheiros = resp['lista']
        
        if not lista_ficheiros:
            print("Caixa de entrada vazia.")
        else:
            print(f"Voce tem {len(lista_ficheiros)} mensagens:")
            # Mostra as mensagens numeradas (0, 1, 2...)
            for i, f_nome in enumerate(lista_ficheiros):
                print(f"[{i}] {f_nome}")
            
            escolha = input("Qual numero quer ler? ")
            try:
                indice = int(escolha)
                nome_f = lista_ficheiros[indice]
                
                # 2. Pede o conteudo cifrado ao servidor
                pacote = falar_com_servidor({
                    'acao': 'ler', 
                    'usuario': meu_nome, 
                    'nome_ficheiro': nome_f
                })
                
                # 3. Decifra usando a chave Privada local
                texto_limpo = ferramentas.decriptar_mensagem(meu_nome, pacote)
                print(f"\n>>> CONTEUDO SECRETO: {texto_limpo} <<<\n")
                
                # Pergunta se quer apagar
                apagar = input("Apagar mensagem do servidor? (s/n): ")
                if apagar.lower() == 's':
                    falar_com_servidor({
                        'acao': 'remover', 
                        'usuario': meu_nome, 
                        'nome_ficheiro': nome_f
                    })
                    print("Mensagem apagada.")
            except:
                print("Numero invalido ou erro ao decifrar.")

    # OPCAO 3: BACKUP
    elif opcao == "3":
        # Baixa todas as mensagens, decifra e guarda num ficheiro unico
        print("A descarregar tudo...")
        resp = falar_com_servidor({'acao': 'listar', 'usuario': meu_nome})
        
        todas_mensagens = []
        for f_nome in resp['lista']:
            # Baixa
            pacote = falar_com_servidor({'acao': 'ler', 'usuario': meu_nome, 'nome_ficheiro': f_nome})
            # Decifra
            msg_claro = ferramentas.decriptar_mensagem(meu_nome, pacote)
            # Adiciona a lista
            todas_mensagens.append(f"Ficheiro {f_nome}: {msg_claro}")
        
        # Guarda no disco local encriptado com AES (chave fixa)
        nome_backup = f"backup_{meu_nome}.bck"
        ferramentas.fazer_backup(todas_mensagens, nome_backup)
        print(f"Backup completo guardado em: {nome_backup}")

    # OPCAO 0: SAIR
    elif opcao == "0":
        print("A sair...")
        break