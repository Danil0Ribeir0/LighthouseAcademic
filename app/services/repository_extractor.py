import requests
from typing import List, Dict
from datetime import datetime
from app.models.schemas import RepositoryInfo

class GitHubExtractor:
    """
    Classe responsável por interagir com a API do GitHub e extrair 
    os dados brutos necessários para a análise de saúde do projeto.
    """

    BASE_URL = "https://api.github.com"

    def __init__(self, repo_info: RepositoryInfo):
        self.repo_info = repo_info
        self.headers = {
            "Accpet": "application/vnd.github.v3+json"
        }

        if repo_info.access_token:
            self.headers["Authorization"] = f"token {repo_info.access_token}"
        
    def get_file_metadata(self, path: str) -> Dict:
        """
        Busca metadados de um arquivo específico (tamanho, data de modificação).
        Útil para validar a presença e estagnação da documentação. [cite: 8, 27]
        """

        repo_path = self._parse_repo_url(str(self.repo_info.url))
        url = f"{self.BASE_URL}/repos/{repo_path}/contents/{path}?ref={self.repo_info.branch}"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def _parse_repo_url(self, url: str) -> str:
        """
        Método auxiliar para limpar a URL e retornar apenas 'dono/repositorio'.
        """
        
        return url.rstrip("/").split("github.com/")[-1]