from typing import List, Dict
from app.models.schemas import RepositoryInfo
from app.services.github_client import GitHubClient
from app.services.github_queries import COMMIT_HISTORY_QUERY

class GitHubExtractor:
    """
    Orquestra as chamadas ao GitHubClient e adapta os dados brutos 
    para o formato interno que o ProjectAnalyzer espera.
    """

    def __init__(self, repo_info: RepositoryInfo):
        self.repo_info = repo_info
        self.client = GitHubClient(repo_info.access_token)
        
    def get_file_metadata(self, path: str) -> Dict:
        repo_owner, repo_name = self._parse_repo_url(str(self.repo_info.url)).split("/")
        endpoint = f"repos/{repo_owner}/{repo_name}/contents/{path}?ref={self.repo_info.branch}"
        return self.client.fetch_rest(endpoint)

    def get_commit_history(self) -> List[Dict]:
        repo_owner, repo_name = self._parse_repo_url(str(self.repo_info.url)).split("/")
        
        all_commits = []
        has_next_page = True
        cursor = None
        
        while has_next_page:
            variables = {
                "owner": repo_owner,
                "name": repo_name,
                "branch": self.repo_info.branch,
                "cursor": cursor
            }
            
            data = self.client.fetch_graphql(COMMIT_HISTORY_QUERY, variables)
            
            try:
                history = data["data"]["repository"]["ref"]["target"]["history"]
                
                for node in history["nodes"]:
                    login = node.get("author", {}).get("user", {}).get("login") if node.get("author") and node["author"].get("user") else None
                    name = node.get("author", {}).get("name", "Unknown")
                    
                    all_commits.append({
                        "sha": node.get("oid"),
                        "author": {"login": login} if login else None,
                        "commit": {
                            "author": {"name": name, "date": node.get("committedDate")}
                        },
                        "stats": {
                            "additions": node.get("additions", 0),
                            "deletions": node.get("deletions", 0)
                        }
                    })
                
                has_next_page = history["pageInfo"]["hasNextPage"]
                cursor = history["pageInfo"]["endCursor"]
                
                if len(all_commits) >= 500:
                    break
                    
            except (KeyError, TypeError):
                break
                
        return all_commits

    def _parse_repo_url(self, url: str) -> str:
        return url.rstrip("/").split("github.com/")[-1]