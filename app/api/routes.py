from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from app.models.schemas import ProjectAnalysisRequest, AnalysisResponse
from app.services.repository_extractor import GitHubExtractor
from app.core.analyzer import ProjectAnalyzer

router = APIRouter(prefix="/v1/projetos", tags=["Análise de Projetos"])

@router.post("/analise", response_model=AnalysisResponse, summary="Gera o Score de Saúde do Projeto")
def analyze_project(request: ProjectAnalysisRequest):
    try:
        extractor = GitHubExtractor(request.repository)
        
        commits_data = extractor.get_commit_history()
        
        members_map = {}
        for commit in commits_data:
            author = commit.get("author")
            username = author.get("login") if author else commit.get("commit", {}).get("author", {}).get("name", "Unknown")
            
            if username not in members_map:
                members_map[username] = {
                    "username": username,
                    "commits": 0,
                    "lines_added": 0,
                    "lines_deleted": 0,
                    "issues_interacted": 0
                }
            members_map[username]["commits"] += 1

        members_activity = list(members_map.values())

        tracked_docs = []
        if not request.config.uses_external_docs:
            for directory in request.config.doc_directories:
                try:
                    doc_meta = extractor.get_file_metadata("README.md")
                    tracked_docs.append({
                        "file_path": "README.md",
                        "last_modified": doc_meta.get("updated_at", "2026-01-01T00:00:00Z"),
                        "size_bytes": doc_meta.get("size", 0),
                        "modification_count": 1
                    })
                except request.exceptions.HTTPError:
                    pass

        raw_data = {
            "repository_timeline": {
                "commits": commits_data
            },
            "members_activity": members_activity,
            "documents_tracked": tracked_docs
        }

        analyzer = ProjectAnalyzer(request_data=request, raw_data=raw_data)
        analysis_result = analyzer.execute_analysis()

        return analysis_result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Falha ao analisar o projeto: {str(e)}"
        )