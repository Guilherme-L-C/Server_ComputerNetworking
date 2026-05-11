import os
import respostas
from erros import erro_404


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


def gerar_listagem(caminho_dir, caminho_url):
    # os.listdir() -> lista todos os arquivos e pastas do diretório
    itens = os.listdir(caminho_dir)
    links = ''

    # Link para voltar ao diretório pai
    # ex: estou em /pasta_teste/ -> .. volta para /
    if caminho_url != '/':
        links += '<li><a href="../">📁 ..</a></li>\n'

    for item in sorted(itens):
        # sorted() -> ordena alfabeticamente
        caminho_completo = os.path.join(caminho_dir, item)
        # os.path.join() -> junta o caminho com o nome do item
        # ex: 'pasta_teste' + 'teste.txt' -> 'pasta_teste/teste.txt'

        if os.path.isdir(caminho_completo):
            # É uma pasta -> adiciona / no final do link
            links += f'<li><a href="{item}/">📁 {item}/</a></li>\n'
        else:
            # É um arquivo
            links += f'<li><a href="{item}">📄 {item}</a></li>\n'

    # Monta o HTML completo
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Index of {caminho_url}</title>
    <style>
        body {{ font-family: monospace; padding: 20px; background: #111; color: #eee; }}
        h1 {{ color: #5ee187; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ padding: 6px 0; }}
        a {{ color: #8fb7ff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>Index of {caminho_url}</h1>
    <ul>{links}</ul>
</body>
</html>"""
    return html.encode('utf-8')

def servir_arquivo(conn, caminho):
    # Remove a / do início do caminho
    # ex: /index.html -> index.html
    caminho_arquivo = caminho.lstrip('/')
    
    # Se o caminho estiver vazio, serve index.html
    if not caminho_arquivo:
        caminho_arquivo = 'index.html'
    
    if os.path.isdir(caminho_arquivo):
        index = os.path.join(caminho_arquivo, 'index.html')
        if os.path.exists(index):
            caminho_arquivo = index
        else:
            conteudo = gerar_listagem(caminho_arquivo, caminho)
            respostas.enviar_resposta(conn, '200 OK', {
                'Content-Type': 'text/html',
                'Content-Length': len(conteudo)
            }, conteudo)
            return

    # Verifica se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        erro_404(conn)
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

