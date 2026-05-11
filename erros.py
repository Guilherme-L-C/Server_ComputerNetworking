from respostas import enviar_resposta

def pagina_erro(conn, codigo, titulo, mensagem):
    """
    Gera e envia uma página HTML de erro personalizada
    codigo   -> 404, 400, 505...
    titulo   -> "Not Found", "Bad Request"...
    mensagem -> explicação amigável para o usuário
    """
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{codigo} - {titulo}</title>
    <style>
        body {{ font-family: monospace; background: #111; color: #eee; 
               display: flex; justify-content: center; align-items: center; 
               height: 100vh; margin: 0; }}
        .container {{ text-align: center; }}
        h1 {{ font-size: 80px; color: #ff6b6b; margin: 0; }}
        h2 {{ color: #aab2bf; }}
        p  {{ color: #69707d; }}
        a  {{ color: #8fb7ff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{codigo}</h1>
        <h2>{titulo}</h2>
        <p>{mensagem}</p>
        <a href="/">← Voltar para o início</a>
    </div>
</body>
</html>""".encode('utf-8')

    enviar_resposta(conn, f'{codigo} {titulo}', {
        'Content-Type': 'text/html',
        'Content-Length': len(html)
    }, html)

# Funções específicas para cada erro
def erro_404(conn):
    pagina_erro(conn, 404, 'Not Found', 
                'O arquivo ou diretório que você procura não existe.')

def erro_400(conn):
    pagina_erro(conn, 400, 'Bad Request', 
                'A requisição enviada é inválida ou malformada.')

def erro_505(conn):
    pagina_erro(conn, 505, 'HTTP Version Not Supported', 
                'Este servidor suporta apenas HTTP/1.1.')