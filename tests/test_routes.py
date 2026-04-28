from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_compute_health_score_success(mocker):
    dados_falsos_graphql = {
        "data": {
            "repository": {
                "ref": {
                    "target": {
                        "history": {
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                            "nodes": [
                                {
                                    "oid": "12345abcde",
                                    "committedDate": "2026-04-20T10:00:00Z",
                                    "additions": 150,
                                    "deletions": 20,
                                    "author": {"user": {"login": "EstudanteA"}, "name": "Estudante A"}
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
    
    mocker.patch("app.services.github_client.GitHubClient.fetch_graphql", return_value=dados_falsos_graphql)
    mocker.patch("app.services.github_client.GitHubClient.fetch_rest", return_value={"size": 2048})

    payload = {
        "repository": {
            "provider": "github",
            "url": "https://github.com/fake/repo",
            "branch": "main",
            "access_token": "token_falso"
        },
        "deadline": "2026-12-31T23:59:59Z",
        "expected_members": ["EstudanteA"]
    }

    response = client.post("/v1/services/analyzer/compute-health-score", json=payload)

    assert response.status_code == 200
    dados = response.json()
    
    assert dados["jsonrpc"] == "2.0"
    assert "id" in dados
    assert "result" in dados
    assert dados["result"]["metrics"]["member_equity_score"] == 70.0