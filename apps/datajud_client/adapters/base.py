from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    """
    Interface comum para adaptadores de tribunais.
    """
    
    @abstractmethod
    def consultar_por_numero(self, numero_processo: str) -> dict:
        pass

    @abstractmethod
    def consultar_por_documento(self, documento: str) -> dict:
        pass
