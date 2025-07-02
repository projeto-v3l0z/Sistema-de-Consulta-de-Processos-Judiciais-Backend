import unittest
from integrations.tjrj_adapter import TJRJAdapter

class TestTJRJAdapter(unittest.TestCase):
    def setUp(self): # Configuração inicial do teste, cria uma instância do adaptador
        self.adapter = TJRJAdapter()

    def test_consultar_por_numero_mock(self):
        numero = '1234567-89.2025.8.26.0001'
        resultado = self.adapter.consultar_por_numero(numero)
        self.assertEqual(resultado['fonte'], 'TJRJ') # Verifica se a fonte da resposta é 'TJRJ'
        self.assertEqual(resultado['resultado']['numero_processo'], numero) # Verifica se o número do processo retornado é o mesmo que foi consultado
        self.assertIn('dados', resultado['resultado']) # Verifica se a resposta contém dados do processo

    def test_consultar_por_documento_mock(self):
        documento = '123.456.789-00'
        resultado = self.adapter.consultar_por_documento(documento)
        self.assertEqual(resultado['fonte'], 'TJRJ')
        self.assertEqual(resultado['resultado']['documento'], documento)
        self.assertIn('processos', resultado['resultado'])

    def test_consultar_por_numero_exception(self):
        # Força uma exceção simulando um erro interno
        original_method = self.adapter._padronizar_resposta # Guarda o método original para restaurar depois
        self.adapter._padronizar_resposta = lambda x: 1 / 0  # Simula uma divisão por zero para gerar uma exceção
        resultado = self.adapter.consultar_por_numero('qualquer') # Chama o método com um valor que causará erro
        self.assertIn('erro', resultado) 
        self.adapter._padronizar_resposta = original_method  # Restaura o método original

    def test_consultar_por_documento_exception(self):
        original_method = self.adapter._padronizar_resposta
        self.adapter._padronizar_resposta = lambda x: 1 / 0
        resultado = self.adapter.consultar_por_documento('qualquer')
        self.assertIn('erro', resultado)
        self.adapter._padronizar_resposta = original_method

if __name__ == "__main__":
    unittest.main()