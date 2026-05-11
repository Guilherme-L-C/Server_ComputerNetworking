import os
import respostas

# Tabela de MIME types 
MIME_TYPES = {
    '.html': 'text/html',
    '.css':  'text/css',
    '.js':   'application/javascript',
    '.txt':  'text/plain',
    '.png':  'image/png',
    '.jpg':  'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif':  'image/gif',
    '.ico':  'image/x-icon',
    '.pdf':  'application/pdf',
}


def get_mime_type(caminho):
    # Pega a extensão do arquivo e retorna o MIME type
    _, extensao = os.path.splitext(caminho)
    return MIME_TYPES.get(extensao.lower(), 'application/octet-stream')
    # application/octet-stream -> tipo genérico para arquivos desconhecidos
    # faz o navegador baixar o arquivo



def servir_arquivo(conn, caminho):
    # Remove a / do início do caminho
    # ex: /index.html -> index.html
    caminho_arquivo = caminho.lstrip('/')
    
    # Se o caminho estiver vazio, serve index.html
    if not caminho_arquivo:
        caminho_arquivo = 'index.html'
    
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        respostas.enviar_resposta(conn, '404 Not Found', {
            'Content-Type': 'text/html'
        }, b'<h1>404 - Arquivo nao encontrado</h1>')
        return
    
    # Descobre o MIME type
    mime = get_mime_type(caminho_arquivo)
    
    # Verifica se é binário ou texto
    modo = 'rb'  # rb = read binary
    
    # Envia os cabeçalhos primeiro
    tamanho = os.path.getsize(caminho_arquivo)
    respostas.enviar_resposta(conn, '200 OK', {
        'Content-Type': mime,
        'Content-Length': tamanho,
    })
    
    # Lazy evaluation — lê e envia em chunks de 8KB
    with open(caminho_arquivo, modo) as arquivo:
        while True:
            chunk = arquivo.read(8192)
            if not chunk:
                break
            conn.sendall(chunk)
            