# Defina uma interface (ou classe abstrata) para garantir que todos tenham to_standard_format()
from abc import ABC, abstractmethod
from processo.dtos import ProcessoDTO

class BaseAdapter(ABC):

    @abstractmethod
    def fetch_raw(self, numero_processo: str) -> dict:
        """Chama a API externa e retorna o JSON cru."""
        pass

    @abstractmethod
    def to_standard_format(self, raw_data: dict) -> ProcessoDTO:
        """Converte o raw_data para ProcessoDTO."""
        pass
