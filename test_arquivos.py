"""Testa se servir_arquivo entrega arquivos da pasta servida e bloqueia path traversal."""
import os
import tempfile
import unittest

import arquivos


class ConexaoFalsa:
    """Guarda tudo o que o servidor enviaria pelo socket."""

    def __init__(self):
        self.dados = b''

    def sendall(self, dados):
        self.dados += dados


class TestServirArquivo(unittest.TestCase):
    def setUp(self):
        # Pasta servida dentro de uma pasta com um arquivo "secreto" ao lado
        self.base = tempfile.TemporaryDirectory()
        self.pasta = os.path.join(self.base.name, 'site')
        os.mkdir(self.pasta)
        with open(os.path.join(self.pasta, 'ola.txt'), 'w') as f:
            f.write('ola')
        with open(os.path.join(self.base.name, 'segredo.txt'), 'w') as f:
            f.write('segredo')
        self.cwd = os.getcwd()
        os.chdir(self.pasta)

    def tearDown(self):
        os.chdir(self.cwd)
        self.base.cleanup()

    def test_entrega_arquivo_da_pasta(self):
        conn = ConexaoFalsa()
        self.assertEqual(arquivos.servir_arquivo(conn, '/ola.txt'), 200)
        self.assertTrue(conn.dados.endswith(b'ola'))

    def test_bloqueia_path_traversal(self):
        conn = ConexaoFalsa()
        self.assertEqual(arquivos.servir_arquivo(conn, '/../segredo.txt'), 403)
        self.assertNotIn(b'segredo', conn.dados)

    def test_arquivo_inexistente_da_404(self):
        self.assertEqual(arquivos.servir_arquivo(ConexaoFalsa(), '/nada.txt'), 404)


if __name__ == '__main__':
    unittest.main()
