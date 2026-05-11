import socket
import threading
import arquivos
import http_parser

HOST = '0.0.0.0'
PORTA = 8080

# porta 8080 é a convencional para servidor HTTP 

def handle_cliente (conn, addr):
    # addr -> address -> endereço que foi conectado -> uma tupla que contem (ip, porta)
    # conn -> connection -> objeto socket que é criado para gerenciar a conexão com o cliente
   

    # função vai rodar a thread separada para cada cliente
    print(f"[+] Coneção {addr}")
    try:
        while True: 
            # HTTP 1.1 é o persistente, então tem que ter um loop para multiplas requisições
            requisicao = conn.recv(4096)

            if not requisicao:
                # cliente fechou a conexão 
                break
            metodo, caminho, versao, cabecalho = http_parser.parser_requisicao(requisicao)

            # Validações: 
            if metodo is None: 
                print(f"Requisição malformada de {addr}")
                break
            if versao != 'HTTP/1.1':
                print(f"Versão não suportada {versao}")
                break
            if metodo != 'GET': 
                print(f"Método não suportado {metodo}")
                break

            print(f"[{addr}] {metodo} {caminho} {versao}")
            arquivos.servir_arquivo(conn, caminho)
            # versao vazia por enquanto 

    except Exception as e: 
        print(f"Erro: {e}")
    finally: 
        # sempre fecha a conexão 
        conn.close()
        print(f"[-] Conexão encerrada {addr}")








"""
Criando o servidor: 
"""

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((HOST, PORTA))
servidor.listen(5)

print(f"Servidor HTTP rodando em: http://localhost:{PORTA}")

while True:
    conn, addr = servidor.accept()
    thread = threading.Thread(target=handle_cliente, args=(conn, addr))
    thread.daemon = True
    thread.start()

