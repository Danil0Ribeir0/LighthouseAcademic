from abc import ABC, abstractmethod
from app.models.schemas import RPCResponse

class AnalysisOutputAdapter(ABC):
    """
    Interface abstrata para persistência de dados.
    Qualquer banco de dados deve herdar desta classe.
    """
    
    @abstractmethod
    def save_result(self, response: RPCResponse) -> None:
        pass