import datetime

ARQUIVO_LOG = 'log.txt'

def registrar(ip, metodo, caminho, status):
    """
    Registra uma requisição no arquivo de log
    ip      → endereço do cliente ex: 127.0.0.1
    metodo  → GET
    caminho → /index.html
    status  → 200, 404, 400...
    """
    agora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linha = f"[{agora}] {ip} {metodo} {caminho} {status}\n"
    print(linha, end='')
    with open(ARQUIVO_LOG, 'a', encoding='utf-8') as f:
        f.write(linha)