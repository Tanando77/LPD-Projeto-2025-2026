# -*- coding: utf-8 -*-
import re
import os
import paramiko
from .db import get_conn  # Importa a conexao que criamos no db.py

# Tenta importar o GeoIP, se falhar continua sem paises
try:
    import geoip2.database
except ImportError:
    geoip2 = None

# --- CONFIGURACOES DA VM LINUX ---
VM_IP = "192.168.1.95"
VM_USER = "root"      # Altera para o teu user da VM
VM_PASS = "root"        # Altera para a tua password da VM

# --- REGEX PARA ANALISE ---
# Captura tentativas falhadas de SSH
SSH_RE = re.compile(r"sshd.*(?:Invalid user|Failed password for).*from\s+(?P<src>\S+)")
# Captura acessos ao Servidor Web (Apache/Nginx)
HTTP_RE = re.compile(r"(?P<src>\S+) - - \[.*?\] \"(?P<method>\S+) (?P<path>\S+).*\"")

def _get_country(reader, ip):
    if not reader: return "Desconhecido"
    try:
        return reader.city(ip).country.name
    except:
        return "Local/Desconhecido"

def download_remote_logs():
    """Liga-se a VM e descarrega os ficheiros de log para o Windows."""
    print(f"[*] A ligar a VM {VM_IP}...")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(VM_IP, username=VM_USER, password=VM_PASS)
        
        sftp = ssh.open_sftp()
        # Logs padrao do Linux
        remote_logs = {
            'ssh': '/var/log/auth.log',
            'http': '/var/log/apache2/access.log'
        }
        
        local_files = {}
        for svc, path in remote_logs.items():
            local_path = f"temp_{svc}.log"
            print(f"[*] A descarregar {path}...")
            try:
                sftp.get(path, local_path)
                local_files[svc] = local_path
            except:
                print(f"[!] Erro: Nao foi possivel ler {path}. Tens permissoes de root?")
        
        sftp.close()
        ssh.close()
        return local_files
    except Exception as e:
        print(f"[!] Erro na ligacao SSH: {e}")
        return {}

def analyze_logs(geoip_db_path="GeoLite2-City.mmdb"):
    """Le os ficheiros descarregados e guarda os eventos na BD."""
    log_files = download_remote_logs()
    if not log_files: return

    # Inicializa o leitor de GeoIP se o ficheiro existir
    reader = None
    if geoip2 and os.path.exists(geoip_db_path):
        reader = geoip2.database.Reader(geoip_db_path)

    with get_conn() as conn:
        cursor = conn.cursor()
        
	# Processar SSH
        if 'ssh' in log_files:
            with open(log_files['ssh'], 'r') as f:
                for line in f:
                    m = SSH_RE.search(line)
                    if m:
                        ip = m.group('src') # Agora isto nunca falhara
                        cursor.execute(
                            "INSERT INTO events (source, src_ip, country, service, raw) VALUES (?,?,?,?,?)",
                            ("ssh", ip, _get_country(reader, ip), "SSH Login Attempt", line.strip()[:100])
                        )

        # Processar HTTP
        if 'http' in log_files:
            with open(log_files['http'], 'r') as f:
                for line in f:
                    m = HTTP_RE.search(line)
                    if m:
                        ip = m.group('src')
                        cursor.execute(
                            "INSERT INTO events (source, src_ip, country, service, raw) VALUES (?,?,?,?,?)",
                            ("http", ip, _get_country(reader, ip), m.group('method'), line.strip()[:100])
                        )
    
    if reader: reader.close()
    print("[+] Analise concluida e guardada na base de dados.")

if __name__ == "__main__":
    analyze_logs()