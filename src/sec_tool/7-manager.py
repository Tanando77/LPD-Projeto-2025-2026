import json
import os
import importlib

# Importa as funcoes do nosso ficheiro de seguranca
# (O ficheiro 7-seguranca.py tem de estar na mesma pasta)
seguranca = importlib.import_module("7-seguranca")

# Nome do ficheiro onde guardamos os registos
ARQUIVO_DB = "passwords.json"

# --- FUNCOES DE BASE DE DADOS ---

# Le o ficheiro JSON e retorna uma lista de dados
def carregar_banco():
    if not os.path.exists(ARQUIVO_DB):
        return [] # Se nao existe, retorna lista vazia
    try:
        with open(ARQUIVO_DB, "r") as f:
            return json.load(f)
    except:
        return []

# Guarda a lista de dados no ficheiro JSON
def salvar_banco(dados):
    with open(ARQUIVO_DB, "w") as f:
        # indent=4 serve para deixar o ficheiro bonito e legivel
        json.dump(dados, f, indent=4)

# --- PROGRAMA PRINCIPAL ---
def main():
    print("--- INICIALIZANDO PASSWORD MANAGER ---")
    
    # 1. Verificar se as chaves RSA existem
    seguranca.verificar_chaves()
    
    # 2. Configurar o sistema 2FA
    segredo_2fa = seguranca.configurar_2fa()
    
    # Mostra informacoes de login (Simulacao)
    print("\n[SISTEMA DE SEGURANCA 2FA]")
    print(f"O seu Segredo (Secret): {segredo_2fa}")
    # Nota: Numa app real, usariamos o Google Authenticator.
    # Aqui, mostramos o codigo gerado para facilitar o teste.
    print(f"(MODO TESTE) Codigo valido agora: {seguranca.obter_codigo_atual(segredo_2fa)}")
    
    # 3. Processo de Login
    print("\n--- LOGIN OBRIGATORIO ---")
    autenticado = False
    tentativas = 0
    
    while tentativas < 3:
        codigo = input("Digite o codigo 2FA (6 digitos): ")
        
        # Valida se o codigo bate certo com o segredo e a hora atual
        if seguranca.validar_codigo_2fa(segredo_2fa, codigo):
            print("Login aceite. Bem-vindo!")
            autenticado = True
            break
        else:
            print("Codigo incorreto.")
            tentativas += 1
    
    if not autenticado:
        print("Demasiadas tentativas erradas. O programa vai fechar.")
        return # Sai do programa

    # 4. Loop do Menu (CRUD)
    while True:
        print("\n=== MENU GESTOR DE SENHAS ===")
        print("1. Criar novo registo")
        print("2. Consultar registos (Ler)")
        print("3. Atualizar registo")
        print("4. Apagar registo")
        print("0. Sair")
        
        opcao = input("Escolha uma opcao: ")
        
        # Carrega os dados mais recentes
        dados = carregar_banco()

        # --- CRIAR (CREATE) ---
        if opcao == "1":
            print("\n--- NOVO REGISTO ---")
            url = input("URL/Site: ")
            usuario = input("Usuario: ")
            senha = input("Password: ")
            
            # A password nunca e guardada em texto claro!
            # Encriptamos com a Chave Publica RSA
            senha_encriptada = seguranca.encriptar_senha(senha)
            
            novo_item = {
                "url": url,
                "user": usuario,
                "pass_enc": senha_encriptada
            }
            
            dados.append(novo_item)
            salvar_banco(dados)
            print("Password guardada com seguranca!")

        # --- LER/CONSULTAR (READ) ---
        elif opcao == "2":
            print("\n--- AS SUAS SENHAS ---")
            if not dados:
                print("Base de dados vazia.")
            else:
                for i, item in enumerate(dados):
                    # Para mostrar, temos de desencriptar com a Chave Privada
                    senha_real = seguranca.desencriptar_senha(item["pass_enc"])
                    print(f"ID[{i}] Site: {item['url']} | User: {item['user']} | Pass: {senha_real}")

        # --- ATUALIZAR (UPDATE) ---
        elif opcao == "3":
            print("\n--- ATUALIZAR ---")
            # Lista primeiro para saber o ID
            for i, item in enumerate(dados):
                print(f"ID[{i}] {item['url']} ({item['user']})")
            
            try:
                escolha = int(input("Qual o ID para editar? "))
                if 0 <= escolha < len(dados):
                    print("Deixe em branco para nao mudar.")
                    
                    # Pede novos dados
                    novo_url = input(f"Novo URL [{dados[escolha]['url']}]: ")
                    novo_user = input(f"Novo User [{dados[escolha]['user']}]: ")
                    nova_pass = input("Nova Pass (vazio mantem a antiga): ")
                    
                    # Atualiza apenas se o utilizador escreveu algo
                    if novo_url: dados[escolha]['url'] = novo_url
                    if novo_user: dados[escolha]['user'] = novo_user
                    
                    # Se mudou a senha, tem de re-encriptar
                    if nova_pass:
                        dados[escolha]['pass_enc'] = seguranca.encriptar_senha(nova_pass)
                    
                    salvar_banco(dados)
                    print("Registo atualizado.")
                else:
                    print("ID invalido.")
            except ValueError:
                print("Erro: Tem de digitar um numero.")

        # --- APAGAR (DELETE) ---
        elif opcao == "4":
            print("\n--- APAGAR ---")
            for i, item in enumerate(dados):
                print(f"ID[{i}] {item['url']}")
                
            try:
                escolha = int(input("Qual o ID para apagar? "))
                if 0 <= escolha < len(dados):
                    removido = dados.pop(escolha)
                    salvar_banco(dados)
                    print(f"Registo do site {removido['url']} foi apagado.")
                else:
                    print("ID invalido.")
            except ValueError:
                print("Erro: Tem de digitar um numero.")

        # --- SAIR ---
        elif opcao == "0":
            print("A sair... Ate logo!")
            break
        else:
            print("Opcao invalida.")

if __name__ == "__main__":
    main()