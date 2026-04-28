from datetime import datetime, timezone
from typing import Dict, Any

from app.models.schemas import ProjectAnalysisRequest
from app.core.equity_analyzer import EquityAnalyzer
from app.core.frequency_analyzer import FrequencyAnalyzer
from app.core.documentation_analyzer import DocumentationAnalyzer

class ProjectAnalyzer:
    """
    Orquestrador central que une a extração de dados brutos com as regras de negócio
    para gerar o Score de Saúde final do projeto.
    """

    def __init__(self, request_data: ProjectAnalysisRequest, raw_data: Dict[str, Any]):
        self.request_data = request_data
        self.config = request_data.config
        self.raw_data = raw_data
        
        self.deadline = request_data.deadline
        if self.deadline.tzinfo is None:
            self.deadline = self.deadline.replace(tzinfo=timezone.utc)
            
        now = datetime.now(timezone.utc)
        self.is_post_deadline = now > self.deadline

    def execute_analysis(self) -> Dict[str, Any]:
        """
        Aciona os três pilares analíticos, calcula a média ponderada e consolida os alertas.
        """

        commits = self.raw_data.get("repository_timeline", {}).get("commits", [])
        members_activity = self.raw_data.get("members_activity", [])
        tracked_docs = self.raw_data.get("documents_tracked", [])

        start_date = self._get_project_start_date(commits)

        freq_score, freq_alerts = FrequencyAnalyzer.calculate(
            commits=commits,
            start_date=start_date,
            deadline=self.deadline,
            bucket_size_days=self.config.bucket_size_days
        )

        doc_score, doc_alerts = DocumentationAnalyzer.calculate(
            tracked_docs=tracked_docs,
            uses_external_docs=self.config.uses_external_docs,
            is_post_deadline=self.is_post_deadline
        )

        equity_score, equity_alerts = EquityAnalyzer.calculate(
            members_activity=members_activity
        )

        weights = self.config.weights
        final_score = (
            (freq_score * weights.get("commit_frequency", 0.4)) +
            (doc_score * weights.get("doc_presence", 0.4)) +
            (equity_score * weights.get("member_equity", 0.2))
        )

        all_alerts = freq_alerts + doc_alerts + equity_alerts
        status = self._determine_overall_status(final_score, all_alerts)

        return {
            "summary": {
                "health_score": round(final_score, 2),
                "status": status,
                "alerts": all_alerts
            },
            "metrics": {
                "commit_frequency_score": freq_score,
                "doc_presence_score": doc_score,
                "member_equity_score": equity_score
            },
            "raw_data": self.raw_data
        }

    def _get_project_start_date(self, commits: list) -> datetime:
        """
        Itera sobre o histórico bruto para descobrir o dia em que o projeto realmente começou.
        """

        if not commits:
            return datetime.now(timezone.utc)
            
        oldest_date = None
        for c in commits:
            c_date_str = c.get("date")
            if c_date_str:
                c_date = datetime.fromisoformat(c_date_str.replace('Z', '+00:00'))
                if oldest_date is None or c_date < oldest_date:
                    oldest_date = c_date
                    
        return oldest_date or datetime.now(timezone.utc)

    def _determine_overall_status(self, final_score: float, alerts: list) -> str:
        """
        Determina a 'cor' do semáforo do projeto. Se houver um alerta de severidade alta,
        o status cai imediatamente para crítico, independentemente da nota.
        """
        
        has_critical = any(a.get("severity") == "high" for a in alerts)
        
        if final_score < 50.0 or has_critical:
            return "critical"
        elif final_score < 80.0 or len(alerts) > 0:
            return "warning"
        return "healthy"