import socket
import threading
import arquivos
import http_parser
from erros import erro_400, erro_505
from logs import registrar

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
                erro_505(conn)
                break
            if metodo != 'GET': 
                print(f"Método não suportado {metodo}")
                erro_400(conn)
                break

            print(f"[{addr}] {metodo} {caminho} {versao}")
            arquivos.servir_arquivo(conn, caminho)
            arquivos.servir_arquivo(conn, caminho)
            registrar(addr[0], metodo, caminho, 200)
            
            # versao vazia por enquanto 

    except ConnectionResetError:
        print(f"[!] Cliente {addr} desconectou abruptamente")

    except TimeoutError:
        print(f"[!] Timeout na conexão {addr}")

    except PermissionError:
        print(f"[!] Sem permissão para acessar arquivo — {addr}")

    except OSError as e:
        print(f"[!] Erro de socket {addr}: {e}")

    except Exception as e:
        print(f"[!] Erro inesperado {addr}: {e}")

    finally:
        try:
            conn.close()
        except OSError:
            pass
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

