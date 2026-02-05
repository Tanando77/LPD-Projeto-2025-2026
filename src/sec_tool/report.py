from .db import get_conn

def gerar_relatorio():
    print("\n" + "="*50)
    print("       RELATORIO DE EVENTOS DE SEGURANCA")
    print("="*50)

    with get_conn() as conn:
        cursor = conn.cursor()
        
        # 1. Resumo por Pais (Exigencia do enunciado)
        print("\n[+] ORIGEM POR PAIS:")
        res_paises = cursor.execute(
            "SELECT country, COUNT(*) FROM events GROUP BY country ORDER BY COUNT(*) DESC"
        ).fetchall()
        
        for row in res_paises:
            print(f" - {row[0]}: {row[1]} ocorrencias")

        # 2. Ultimos 10 Eventos Detetados
        print("\n[+] ULTIMOS 10 EVENTOS DETETADOS:")
        print(f"{'DATA':<20} | {'IP ORIGEM':<15} | {'SERVICO':<10} | {'PAIS'}")
        print("-" * 65)
        
        res_recentes = cursor.execute(
            "SELECT ts, src_ip, service, country FROM events ORDER BY id DESC LIMIT 10"
        ).fetchall()
        
        for row in res_recentes:
            print(f"{row[0]:<20} | {row[1]:<15} | {row[2]:<10} | {row[3]}")

if __name__ == "__main__":
    gerar_relatorio()