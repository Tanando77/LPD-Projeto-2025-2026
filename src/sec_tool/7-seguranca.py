import os
import pyotp
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# --- PARTE 1: CRIPTOGRAFIA ASSIMETRICA (RSA) ---

# Verifica se os ficheiros de chaves ja existem na pasta
# Se nao existirem, cria um novo par (Publica e Privada)
def verificar_chaves():
    # Cria a pasta 'chaves' se nao existir
    if not os.path.exists("chaves"):
        os.makedirs("chaves")
        
    caminho_privada = "chaves/manager_priv.pem"
    caminho_publica = "chaves/manager_pub.pem"

    # Se faltar alguma chave, geramos tudo de novo
    if not os.path.exists(caminho_privada) or not os.path.exists(caminho_publica):
        print("-> A gerar chaves RSA (2048 bits)...")
        
        # Gera a chave mestra de 2048 bits
        key = RSA.generate(2048)
        
        # Guarda a chave PRIVADA (Segredo do sistema)
        with open(caminho_privada, "wb") as f:
            f.write(key.export_key())
            
        # Guarda a chave PUBLICA (Usada para encriptar)
        with open(caminho_publica, "wb") as f:
            f.write(key.publickey().export_key())
            
        print("-> Chaves geradas com sucesso.")

# Recebe uma senha normal (texto) e encripta usando a Chave Publica
# Retorna a senha cifrada em formato Hexadecimal para guardar no JSON
def encriptar_senha(senha_texto):
    # Carregar a chave publica do disco
    with open("chaves/manager_pub.pem", "rb") as f:
        chave_publica = RSA.import_key(f.read())
    
    # Prepara o cifrador usando o padrao PKCS1 OAEP (Mais seguro)
    cifra = PKCS1_OAEP.new(chave_publica)
    
    # Converte o texto para bytes
    senha_bytes = senha_texto.encode("utf-8")
    
    # Encripta os dados
    senha_cifrada = cifra.encrypt(senha_bytes)
    
    # Converte bytes estranhos para texto hexadecimal (0-9, A-F)
    return senha_cifrada.hex()

# Recebe a senha cifrada (Hex) e descobre a original usando a Chave Privada
def desencriptar_senha(senha_hex):
    try:
        # Carregar a chave privada do disco
        with open("chaves/manager_priv.pem", "rb") as f:
            chave_privada = RSA.import_key(f.read())
        
        # Prepara o decifrador
        cifra = PKCS1_OAEP.new(chave_privada)
        
        # Converte o Hex de volta para bytes cifrados
        bytes_cifrados = bytes.fromhex(senha_hex)
        
        # Tenta decifrar
        senha_original = cifra.decrypt(bytes_cifrados)
        
        # Retorna o texto legivel
        return senha_original.decode("utf-8")
    except Exception as e:
        # Se a chave estiver errada ou o texto corrompido
        return f"[Erro: {e}]"

# --- PARTE 2: AUTENTICACAO 2FA (Two-Factor) ---

# Cria ou le o segredo unico do utilizador para o 2FA
def configurar_2fa():
    arquivo_secret = "chaves/2fa_secret.txt"
    
    # Se ja existe um segredo guardado, le e devolve
    if os.path.exists(arquivo_secret):
        with open(arquivo_secret, "r") as f:
            return f.read().strip()
    else:
        # Se nao existe, gera um codigo aleatorio base32
        # Isto seria o que o QR Code contem numa app real
        segredo = pyotp.random_base32()
        with open(arquivo_secret, "w") as f:
            f.write(segredo)
        return segredo

# Verifica se o codigo de 6 digitos que o usuario digitou esta correto
# Compara com o relogio atual (TOTP - Time-based One-Time Password)
def validar_codigo_2fa(segredo, codigo_usuario):
    totp = pyotp.TOTP(segredo)
    return totp.verify(codigo_usuario)

# Funcao de AJUDA para testes:
# Gera o codigo valido no momento atual (ja que nao estamos a usar telemovel real)
def obter_codigo_atual(segredo):
    totp = pyotp.TOTP(segredo)
    return totp.now()