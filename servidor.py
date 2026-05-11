import socket
import threading
import arquivos
import http_parser
from erros import erro_400, erro_505
from logs import registrar

HOST = '0.0.0.0'
PORTA = 8080

def handle_cliente(conn, addr):
    print(f"[+] Conexão {addr}")
    try:
        while True:
            requisicao = conn.recv(4096)
            if not requisicao:
                break
            metodo, caminho, versao, cabecalho = http_parser.parser_requisicao(requisicao)
            if metodo is None:
                print(f"Requisição malformada de {addr}")
                break
            if versao != 'HTTP/1.1':
                print(f"Versão não suportada {versao}")
                erro_505(conn)
                registrar(addr[0], metodo, caminho, 505)
                break
            if metodo != 'GET':
                print(f"Método não suportado {metodo}")
                erro_400(conn)
                registrar(addr[0], metodo, caminho, 400)
                break
            print(f"[{addr}] {metodo} {caminho} {versao}")
            status = arquivos.servir_arquivo(conn, caminho)
            registrar(addr[0], metodo, caminho, status)

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
