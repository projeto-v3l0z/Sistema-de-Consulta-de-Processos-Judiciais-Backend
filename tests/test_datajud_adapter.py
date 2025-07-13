import unittest
from unittest.mock import patch
from integrations.datajud_adapter import DatajudAdapter

class TestDatajudAdapter(unittest.TestCase):
    def setUp(self): # Configuração inicial do teste, cria uma instância do adaptador
        self.adapter = DatajudAdapter() 

    @patch('integrations.datajud_adapter.logger') # Substitui o logger real por um mock durante o teste
    def test_consultar_por_numero_success(self, mock_logger): 
        numero_processo = '1234567-89.2025.8.26.0001'
        resultado = self.adapter.consultar_por_numero(numero_processo) # Chama o método a ser testado
        self.assertIn('numero_processo', resultado) # Verifica se o resultado contém a chave 'numero_processo'
        self.assertEqual(resultado['numero_processo'], numero_processo) # Verifica se o número do processo retornado é o mesmo que foi consultado
        mock_logger.info.assert_called_with(f'Consultando processo pelo número: {numero_processo}') # Verifica se o logger registrou a mensagem correta

    @patch('integrations.datajud_adapter.logger')
    def test_consultar_por_documento_success(self, mock_logger):
        cpf = '123.456.789-00'
        resultado = self.adapter.consultar_por_documento(cpf)
        self.assertIn('documento', resultado)
        self.assertEqual(resultado['documento'], cpf)
        mock_logger.info.assert_called_with(f'Consultando processos pelo documento: {cpf}')

    @patch('integrations.datajud_adapter.logger')
    def test_consultar_por_numero_exception(self, mock_logger):
        # Simula um erro na consulta
        resultado = self.adapter.consultar_por_numero('erro')
        self.assertIn('erro', resultado)
        self.assertEqual(resultado['erro'], 'Falha na consulta ao Datajud pelo número do processo.')

if __name__ == "__main__": # Garante que o código só será executado se este arquivo for executado diretamente
    unittest.main()