import os
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

# --- FUNCAO 1: GERAR CHAVES (RSA) ---
# Verifica se o utilizador ja tem chaves (Publica e Privada).
# Se nao tiver, cria um par novo e guarda na pasta 'chaves'.
def verificar_chaves(nome_utilizador):
    # Cria a pasta 'chaves' se ela nao existir
    if not os.path.exists('chaves'): 
        os.makedirs('chaves')
    
    caminho_priv = f'chaves/{nome_utilizador}_priv.pem'
    caminho_pub = f'chaves/{nome_utilizador}_pub.pem'
    
    # Se os ficheiros nao existem, geramos novas chaves
    if not os.path.exists(caminho_priv):
        print(f"-> A gerar chaves RSA para {nome_utilizador}...")
        # Gera uma chave RSA de 2048 bits (Seguro)
        key = RSA.generate(2048)
        
        # Guarda a chave privada (Segredo do utilizador)
        with open(caminho_priv, 'wb') as f: 
            f.write(key.export_key())
            
        # Guarda a chave publica (Para os outros usarem)
        with open(caminho_pub, 'wb') as f: 
            f.write(key.publickey().export_key())

# --- FUNCAO 2: ENCRIPTAR (MISTURA AES + RSA) ---
# Usa a chave Publica do destino para proteger uma chave AES aleatoria.
# Usa a chave AES para proteger o texto (porque e mais rapido).
def encriptar_mensagem(usuario_destino, texto):
    try:
        # 1. Tenta ler a chave Publica de quem vai receber
        caminho_pub = f'chaves/{usuario_destino}_pub.pem'
        with open(caminho_pub, 'rb') as f:
            chave_publica = RSA.import_key(f.read())
    except FileNotFoundError:
        # Se nao encontrar a chave, devolve None (Erro)
        return None 

    # 2. Cria uma senha temporaria para esta mensagem (16 bytes)
    chave_sessao_aes = get_random_bytes(16)

    # 3. Encripta o texto com essa senha temporaria (AES)
    cipher_aes = AES.new(chave_sessao_aes, AES.MODE_EAX)
    # Transforma texto em bytes e cifra
    texto_cifrado, tag = cipher_aes.encrypt_and_digest(texto.encode('utf-8'))

    # 4. Protege a senha temporaria usando a chave RSA Publica
    cipher_rsa = PKCS1_OAEP.new(chave_publica)
    chave_sessao_protegida = cipher_rsa.encrypt(chave_sessao_aes)

    # 5. Retorna um dicionario com todas as pecas necessarias
    return {
        'enc_key': chave_sessao_protegida.hex(), # Chave AES protegida
        'nonce': cipher_aes.nonce.hex(),         # Numero unico do AES
        'tag': tag.hex(),                        # Verificacao de integridade
        'ciphertext': texto_cifrado.hex()        # A mensagem secreta
    }

# --- FUNCAO 3: DESENCRIPTAR ---
# Faz o processo inverso: Usa chave Privada para recuperar a chave AES,
# e depois usa a chave AES para ler o texto.
def decriptar_mensagem(meu_nome, pacote):
    # 1. Le a minha chave Privada
    caminho_priv = f'chaves/{meu_nome}_priv.pem'
    with open(caminho_priv, 'rb') as f:
        chave_privada = RSA.import_key(f.read())

    # 2. Usa a chave Privada para descobrir a chave AES da sessao
    cipher_rsa = PKCS1_OAEP.new(chave_privada)
    # Converte de hexadecimal para bytes antes de decifrar
    chave_sessao = cipher_rsa.decrypt(bytes.fromhex(pacote['enc_key']))

    # 3. Usa a chave AES descoberta para ler a mensagem
    cipher_aes = AES.new(chave_sessao, AES.MODE_EAX, nonce=bytes.fromhex(pacote['nonce']))
    mensagem_bytes = cipher_aes.decrypt_and_verify(
        bytes.fromhex(pacote['ciphertext']),
        bytes.fromhex(pacote['tag'])
    )
    
    # Devolve o texto legivel
    return mensagem_bytes.decode('utf-8')

# --- FUNCAO 4: BACKUP (SIMETRICO) ---
# Guarda todas as mensagens num unico ficheiro, protegido por uma senha fixa.
def fazer_backup(lista_mensagens, nome_ficheiro):
    # Chave fixa para o backup (em projeto real seria derivada de password)
    chave_backup = b'chave_segura_123' 
    
    # Prepara a cifra AES
    cipher = AES.new(chave_backup, AES.MODE_EAX)
    
    # Transforma a lista de mensagens em texto JSON e depois em bytes
    dados = json.dumps(lista_mensagens).encode('utf-8')
    
    # Cifra tudo
    texto_cifrado, tag = cipher.encrypt_and_digest(dados)
    
    # Guarda no disco
    pacote_backup = {
        'nonce': cipher.nonce.hex(),
        'dados': texto_cifrado.hex(),
        'tag': tag.hex()
    }
    with open(nome_ficheiro, 'w') as f:
        json.dump(pacote_backup, f)