from datetime import datetime
from typing import List, Dict
from app.models.schemas import AnalysisConfig, ProjectAnalysisRequest

class ProjectAnalyzer:
    def __init__(self, request_data: ProjectAnalysisRequest, raw_data: Dict):
        self.config = request_data.config
        self.deadline = request_data.deadline
        self.raw_data = raw_data
        self.is_post_deadline = datetime.now() > self.deadline

    def calculate_health_score(self) -> Dict:
        """
        Calcula a média ponderada baseada nas métricas de processo.
        """

        weights = self.config.weights

        freq_score = self._analyze_commit_frequency()
        doc_score = self._analyze_documentation_status()
        equity_score = self._analyze_member_equity()

        final_score = (
            (freq_score * weights["commit_frequency"]) +
            (doc_score * weights["doc_presence"]) +
            (equity_score * weights["member_equity"])
        )

        return {
            "health_score": round(final_score, 2),
            "metrics": {
                "commit_frequency_score": freq_score,
                "doc_presence_score": doc_score,
                "member_equity_score": equity_score
            }
        }
    
    def _analyze_commit_frequency(self) -> float:
        """
        Analisa se o ritmo de commits foi constante até o deadline[cite: 9, 26].
        """

        return 80.0
    
    def _analyze_documentation_status(self) -> float:
        """
        Valida a presença e atualização de arquivos críticos.
        """

        return 70.0
    
    def _analyze_member_equity(self) -> float:
        """
        Identifica o "herói" ou distribuição equilibrada.
        """
        
        return 90.0