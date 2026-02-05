import sqlite3
import os
from contextlib import contextmanager

# Isto garante que a BD e criada na mesma pasta que este ficheiro .py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "projeto_seguranca.db")

def init_db(db_path=DB_NAME):
    print(f"[*] A tentar criar base de dados em: {db_path}")
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT,
                    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    src_ip TEXT,
                    dst_ip TEXT,
                    country TEXT,
                    service TEXT,
                    raw TEXT
                )
            """)
            conn.commit()
        print("[+] Base de dados inicializada com sucesso!")
    except Exception as e:
        print(f"[!] Erro ao criar base de dados: {e}")

@contextmanager
def get_conn(db_path=DB_NAME):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()