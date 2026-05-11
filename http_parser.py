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
