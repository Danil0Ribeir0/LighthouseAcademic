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
            "Accept": "application/vnd.github.v3+json"
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
    
    def get_commit_history(self, since: datetime = None) -> List[Dict]:
        """
        Extrai a lista de commits para calcular frequência e equidade entre membros.
        """
        
        repo_path = self._parse_repo_url(str(self.repo_info.url))
        url = f"{self.BASE_URL}/repos/{repo_path}/commits"
        
        params = {"sha": self.repo_info.branch}
        if since:
            params["since"] = since.isoformat()

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_commit_details(self, commit_sha: str) -> Dict:
        """
        Busca os detalhes profundos de um commit específico usando o seu SHA,
        incluindo as estatísticas de linhas adicionadas e removidas.
        """
        
        repo_path = self._parse_repo_url(str(self.repo_info.url))
        url = f"{self.BASE_URL}/repos/{repo_path}/commits/{commit_sha}"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def _parse_repo_url(self, url: str) -> str:
        """
        Método auxiliar para limpar a URL e retornar apenas 'dono/repositorio'.
        """
        
        return url.rstrip("/").split("github.com/")[-1]