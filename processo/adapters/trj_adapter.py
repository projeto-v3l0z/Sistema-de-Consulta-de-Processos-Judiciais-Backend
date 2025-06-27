# Adaptador do trj
import requests
from datetime import datetime
from processo.adapters.base_adapter import BaseAdapter
from processo.dtos import ProcessoDTO

class TrjAdapter(BaseAdapter):
    """
    Adaptador para o Tribunal de Justiça do Rio de Janeiro (TJRJ).
    Realiza requisições ao cpopg do TJRJ e converte para o formato padrão.
    """
    BASE_URL = "https://www3.tjrj.jus.br/cpopg/open.do"

    def fetch_raw(self, numero_processo: str) -> dict:
        """
        Busca os dados brutos do processo no TJRJ.
        """
        params = {
            'gateway': 'true',
            'paginaConsulta': '1',
            'localPesquisa.cdLocal': '1',
            'cbPesquisa': 'NUMPROC',
            'dadosConsulta.nuProcesso': numero_processo
        }
        resp = requests.get(self.BASE_URL, params=params)
        resp.raise_for_status()
        return resp.json()

    def to_standard_format(self, raw_data: dict) -> ProcessoDTO:
        """
        Converte o JSON do TJRJ para ProcessoDTO.
        """
        proc = raw_data.get('processo', {})
        num = proc.get('numero', '')
        data_str = proc.get('dataDistribuicao', '')
        data_iso = ''
        if data_str:
            try:
                # Formato possivelmente 'YYYY-MM-DD'
                data_iso = datetime.strptime(data_str, '%Y-%m-%d').date().isoformat()
            except ValueError:
                data_iso = data_str

        return ProcessoDTO(
            numero_processo=num,
            tribunal='TJRJ',
            classe_processual=proc.get('classe', '').strip(),
            assunto=proc.get('assunto', '').strip(),
            data_distribuicao=data_iso,
            orgao_julgador=proc.get('orgaoJulgador', '').strip(),
            situacao_atual=proc.get('situacao', '').strip(),
        )
