def enviar_resposta(conn, status, cabecalhos, corpo=b''):
    # Monta e envia a resposta HTTP completa
    resposta = f"HTTP/1.1 {status}\r\n"
    for chave, valor in cabecalhos.items():
        resposta += f"{chave}: {valor}\r\n"
    resposta += "\r\n"
    # Envia os cabeçalhos
    conn.sendall(resposta.encode('utf-8'))
    # Envia o corpo se existir
    if corpo:
        conn.sendall(corpo)