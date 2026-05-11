import datetime

ARQUIVO_LOG = 'log.txt'

def registrar(ip, metodo, caminho, status):
    agora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linha = f"[{agora}] {ip} {metodo} {caminho} {status}\n"
    print(linha, end='')
    with open(ARQUIVO_LOG, 'a', encoding='utf-8') as f:
        f.write(linha)
