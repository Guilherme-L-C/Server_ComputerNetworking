import socket
import threading

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
            metodo, caminho, versao, cabecalho = parser_requisicao(requisicao)

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
            # versao vazia por enquanto 

    except Exception as e: 
        print(f"Erro: {e}")
    finally: 
        # sempre fecha a conexão 
        conn.close()
        print(f"[-] Conexão encerrada {addr}")


def parser_requisicao(dados):
    """Recebe dados brutos da requisição HTTP
        Retorna: método, caminho, versão, cabeçalhos
    """
    try: 
        # decodifica os bytes para string: 
        texto = dados.decode('utf-8')





        # separa cabeçalhos do corpo (linha vazia \r\n\r\n)
        cabecalhos_raw = texto.split('\r\n\r\n')[0]

        # separa cada linha
        linhas = cabecalhos_raw.split('\r\n')

        # primeira linha -> "GET /index.html HTTP/1.1"
        linha_requisicao = linhas[0].split(' ')

        if len (linha_requisicao) != 3:
            return None, None, None, None
        
        metodo = linha_requisicao[0] #GET
        caminho = linha_requisicao[1] # /index.html
        versao = linha_requisicao[2] # HTTP/1.1


        # extrai os cabeçalhos restantes 
        cabecalhos = {}
        for linha in linhas[1:]:
            if ':' in linha: 
                chave, valor = linha.split (':', 1)
                cabecalhos[chave.strip()] = valor.strip()
        return metodo, caminho, versao, cabecalhos
    
    except Exception:
        return None, None, None, None

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

