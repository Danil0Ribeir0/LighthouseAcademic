from app.adapters.output_adapter import AnalysisOutputAdapter
from app.adapters.json_file_adapter import JSONFileAdapter

def get_output_adapter() -> AnalysisOutputAdapter:
    """
    Fábrica de Adaptadores. 
    Caso queira trocar o banco de dados, basta trocar a classe aqui e 
    todo o sistema passa a usar o novo banco sem tocar em nenhuma regra de negócio.
    """
    return JSONFileAdapter()