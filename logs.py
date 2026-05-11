import datetime

ARQUIVO_LOG = 'log.txt'
# Nome do arquivo onde os logs serão salvos

def registrar(ip, metodo, caminho, status):
    """
    Registra uma requisição no arquivo de log
    ip      → endereço do cliente ex: 127.0.0.1
    metodo  → GET
    caminho → /index.html
    status  → 200, 404, 400...
    """
    # Pega a data e hora atual
    agora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # strftime → formata a data como string
    # %Y = ano, %m = mês, %d = dia, %H = hora, %M = minuto, %S = segundo

    linha = f"[{agora}] {ip} {metodo} {caminho} {status}\n"

    # Mostra no terminal também
    print(linha, end='')

    # Salva no arquivo
    with open(ARQUIVO_LOG, 'a', encoding='utf-8') as f:
        f.write(linha)
    # 'a' → append, adiciona no final sem apagar o que já tem
    # se fosse 'w' → apagaria tudo e começaria do zero