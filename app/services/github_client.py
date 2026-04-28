import requests
from typing import Dict, Any

class GitHubClient:
    """
    Responsável pela comunicação HTTP com as APIs do GitHub.
    """

    REST_URL = "https://api.github.com"
    GRAPHQL_URL = "https://api.github.com/graphql"

    def __init__(self, access_token: str = None):
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if access_token:
            self.headers["Authorization"] = f"token {access_token}"
        else:
            raise ValueError("O GraphQL do GitHub requer um 'access_token' válido.")

    def fetch_rest(self, endpoint: str) -> Dict[str, Any]:
        """Executa chamadas simples na API REST (GET)."""

        url = f"{self.REST_URL}/{endpoint.lstrip('/')}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_graphql(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Executa chamadas avançadas na API GraphQL (POST)."""
        
        response = requests.post(
            self.GRAPHQL_URL, 
            headers=self.headers, 
            json={"query": query, "variables": variables}
        )
        response.raise_for_status()
        return response.json()