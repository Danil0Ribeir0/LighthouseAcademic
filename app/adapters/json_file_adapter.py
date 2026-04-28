import os
from app.models.schemas import RPCResponse
from app.adapters.output_adapter import AnalysisOutputAdapter

class JSONFileAdapter(AnalysisOutputAdapter):
    """
    Implementação concreta que salva as respostas em arquivos .json.
    Ótimo para testes ou como banco de dados NoSQL de baixo custo.
    """
    
    def __init__(self, output_dir: str = "data/analyses"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_result(self, response: RPCResponse) -> None:
        file_path = os.path.join(self.output_dir, f"{response.id}.json")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.model_dump_json(indent=2))