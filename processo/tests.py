from rest_framework.test import APITestCase
from unittest.mock import patch
from django.urls import reverse

""" 
Testes para a view de consulta ao Datajud 
"""

class ConsultaDatajudNumeroViewTest(APITestCase):
    @patch('integrations.datajud_adapter.DatajudAdapter.consultar_por_numero')
    def test_consulta_datajud_numero_view(self, mock_consultar): 
        mock_consultar.return_value = {'numero_processo': '123'} # Simula o retorno do adaptador Datajud
        url = reverse('consulta-datajud-numero')  # url da view de consulta ao Datajud
        response = self.client.get(url, {'numero': '123'}) # Faz uma requisição GET para a view com o número do processo
        self.assertEqual(response.status_code, 200) # Se a requisição foi bem sucedida, o status deve ser 200
        self.assertEqual(response.data['numero_processo'], '123') # Verifica se o número do processo retornado é o mesmo que foi consultado
        mock_consultar.assert_called_once_with('123') 

class ConsultaDatajudDocumentoViewTest(APITestCase):
    @patch('integrations.datajud_adapter.DatajudAdapter.consultar_por_documento')
    def test_consulta_datajud_documento_view(self, mock_consultar):
        mock_consultar.return_value = {'documento': '123.456.789-00'}  
        url = reverse('consulta-datajud-documento')  
        response = self.client.get(url, {'documento': '123.456.789-00'})  # Faz uma requisição GET para a view com o CPF/CNPJ
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(response.data['documento'], '123.456.789-00')  # Verifica se o documento retornado é o mesmo que foi consultado
        mock_consultar.assert_called_once_with('123.456.789-00')