import math
from typing import List, Dict, Tuple

class EquityAnalyzer:
    WEIGHT_COMMITS = 0.2
    WEIGHT_CODE = 0.6
    WEIGHT_ISSUES = 0.2

    HERO_THRESHOLD = 0.70
    GHOST_THRESHOLD = 0.10

    @classmethod
    def calculate(cls, members_activity: List[Dict]) -> Tuple[float, List[Dict]]:
        """
        Calcula a nota de equidade (0 a 100) e retorna a lista de alertas associados.
        """

        if not members_activity:
            return 0.0, []
        
        individual_scores = {}
        total_score = 0.0

        for member in members_activity:
            username = member["username"]
            commits = member.get("commits", 0)
            lines_added = member.get("lines_added", 0)
            lines_deleted = member.get("lines_deleted", 0)
            issues = member.get("issues_interacted", 0)

            peso_codigo = math.log10(lines_added + 1) + math.log10(lines_deleted + 1)

            s_ind = (commits * cls.WEIGHT_COMMITS) + (peso_codigo * cls.WEIGHT_CODE) + (issues * cls.WEIGHT_ISSUES)

            individual_scores[username] = s_ind
            total_score += s_ind
        
        if total_score == 0:
            return 0.0, [{"type": "no_activity", "severity": "high", "message": "Nenhuma atividade detectada no repositório."}]
        
        alerts = []
        equity_penalty = 0.0

        for username, s_ind in individual_scores.items():
            fatia = s_ind / total_score

            if fatia > cls.HERO_THRESHOLD:
                alerts.append({
                    "type": "collaboration_imbalance",
                    "severity": "high",
                    "message": f"Risco de Herói: '{username}' concentrou {fatia:.1%} do esforço do projeto."
                })
                equity_penalty += 30.0
                
            elif fatia < cls.GHOST_THRESHOLD:
                alerts.append({
                    "type": "ghost_member",
                    "severity": "medium",
                    "message": f"Omissão detectada: '{username}' contribuiu com apenas {fatia:.1%} do esforço."
                })
                equity_penalty += 15.0

        final_equity_score = max(0.0, 100.0 - equity_penalty)

        return round(final_equity_score, 2), alerts