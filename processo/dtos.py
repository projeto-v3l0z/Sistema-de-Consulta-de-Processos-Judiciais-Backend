# isso define como vai ser o formato padrão
from dataclasses import dataclass

@dataclass
class ProcessoDTO:
    numero_processo: str
    tribunal: str
    classe_processual: str
    assunto: str
    data_distribuicao: str   
    orgao_julgador: str
    situacao_atual: str
