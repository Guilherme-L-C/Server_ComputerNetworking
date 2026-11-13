# Servidor HTTP/1.1 — Redes de Computadores

🇺🇸 [Read in English](README.md)

> Projeto desenvolvido para a disciplina de Redes de Computadores (UAB00078)  
> Bacharelado em Engenharia da Computação — UFRPE / UABJ  
> Professor: Ygor Amaral Barbosa Leite de Sena  
> Autor: [Guilherme Leite Cavalcanti](https://github.com/Guilherme-L-C)

---

## Sobre o Projeto

Servidor HTTP/1.1 implementado do zero em Python, sem uso de frameworks ou bibliotecas que abstraiam o protocolo. A comunicação é feita diretamente via sockets TCP, seguindo a especificação do protocolo HTTP/1.1.

---

## Funcionalidades

- Suporte ao método GET
- Conexões persistentes HTTP/1.1 (Keep-Alive)
- Servir arquivos de texto e binários com lazy evaluation (chunks de 8KB)
- Detecção automática de MIME type por extensão
- Navegação de diretórios dinâmica (similar ao Apache)
- Serve `index.html` automaticamente quando disponível
- Códigos de status: 200, 400, 403, 404, 505
- Bloqueio de path traversal (`/../`): nada fora da pasta servida é entregue
- Páginas HTML personalizadas para cada erro
- Sistema de logs com registro em arquivo
- Tratamento de exceções de conexão
- Suporte a múltiplos clientes simultâneos com threading

---

## Estrutura do Projeto

```
Server_ComputerNetworking/
├── servidor.py      → ponto de entrada, loop principal e threading
├── http_parser.py   → parser da requisição HTTP/1.1
├── arquivos.py      → serving de arquivos e listagem de diretórios
├── respostas.py     → montagem e envio de respostas HTTP
├── erros.py         → páginas de erro personalizadas
├── logs.py          → sistema de logs e auditoria
├── test_arquivos.py → testes (unittest)
└── README.md
```

---

## Como Executar

### Pré-requisitos

Python 3.10 ou superior. Nenhuma dependência externa necessária.

### Iniciar o servidor

```bash
python servidor.py
```

Saída esperada:

```
Servidor HTTP rodando em: http://localhost:8080
```

### Acessar no navegador

```
http://localhost:8080
```

---

## Como Testar

### Arquivo estático
```
http://localhost:8080/index.html
```

### Listagem de diretório
```
http://localhost:8080/pasta/
```
Se não houver `index.html` na pasta, o servidor gera uma página com a listagem dos arquivos.

### Erro 404
```
http://localhost:8080/arquivo_que_nao_existe.html
```

### Logs
Os logs são salvos automaticamente em `log.txt` no formato:
```
[2026-05-11 14:30:22] 127.0.0.1 GET /index.html 200
[2026-05-11 14:30:23] 127.0.0.1 GET /naoexiste.html 404
```

---

## Códigos de Status Suportados

| Código | Descrição | Quando ocorre |
|---|---|---|
| 200 | OK | Arquivo encontrado e entregue |
| 400 | Bad Request | Método diferente de GET |
| 403 | Forbidden | Caminho sai da pasta servida (ex.: `/../`) |
| 404 | Not Found | Arquivo ou diretório não encontrado |
| 505 | HTTP Version Not Supported | Versão HTTP diferente de 1.1 |

---

## MIME Types Suportados

| Extensão | MIME Type |
|---|---|
| .html | text/html |
| .css | text/css |
| .js | application/javascript |
| .txt | text/plain |
| .png | image/png |
| .jpg / .jpeg | image/jpeg |
| .gif | image/gif |
| .ico | image/x-icon |
| .pdf | application/pdf |

---

## Arquitetura

```
Navegador
    ↓ requisição HTTP/1.1
servidor.py → aceita conexão → cria thread
    ↓
http_parser.py → extrai método, caminho, versão
    ↓
arquivos.py → localiza arquivo ou gera listagem
    ↓
respostas.py → monta e envia resposta HTTP
    ↓
logs.py → registra em log.txt
```

---

## Testes

```bash
python -m unittest -v
```
