import math
from datetime import datetime, timezone
from typing import List, Dict, Tuple, Optional

class FrequencyAnalyzer:
    MAX_COMMITS_PER_BUCKET = 10
    
    PROCRASTINATION_THRESHOLD = 0.70
    LATE_STAGE_PERCENTAGE = 0.25
    LOW_CONSISTENCY_THRESHOLD = 0.30

    @classmethod
    def calculate(
        cls, 
        commits: List[Dict], 
        start_date: datetime, 
        deadline: datetime, 
        bucket_size_days: Optional[int] = None
    ) -> Tuple[float, List[Dict]]:
        """
        Calcula a consistência do ritmo de commits e retorna alertas.
        """

        if not commits:
            return 0.0, [{"type": "no_commits", "severity": "high", "message": "Nenhum commit encontrado no repositório."}]
        
        total_days = (deadline - start_date).days
        if total_days <= 0:
            total_days = 1

        if bucket_size_days:
            bucket_size = bucket_size_days
        else:
            bucket_size = max(1, total_days // 10)
        
        num_buckets = math.ceil(total_days / bucket_size)
        buckets = [0] * num_buckets

        for commit in commits:
            c_date_str = commit.get("date")

            if not c_date_str:
                continue
            
            c_date = datetime.fromisoformat(c_date_str.replace('Z', '+00:00'))

            if start_date <= c_date <= deadline:
                delta_days = (c_date - start_date).days
                bucket_index = min(delta_days // bucket_size, num_buckets - 1)
                buckets[bucket_index] += 1
        
        capped_buckets = [min(b, cls.MAX_COMMITS_PER_BUCKET) for b in buckets]
        total_capped_commits = sum(capped_buckets)

        if total_capped_commits == 0:
            return 0.0, [{"type": "zero_valid_commits", "severity": "high", "message": "Nenhum commit válido dentro do prazo estipulado."}]
        
        alerts = []
        penalty = 0.0

        active_buckets = sum(1 for b in capped_buckets if b > 0)
        consistency_ratio = active_buckets / num_buckets
        
        base_score = consistency_ratio * 100

        if consistency_ratio < cls.LOW_CONSISTENCY_THRESHOLD:
            alerts.append({
                "type": "low_consistency",
                "severity": "medium",
                "message": f"Baixa consistência: O projeto teve atividade em apenas {consistency_ratio:.1%} do tempo disponível."
            })
            penalty += 15.0

        late_stage_buckets_count = max(1, int(num_buckets * cls.LATE_STAGE_PERCENTAGE))
        
        late_stage_commits = sum(capped_buckets[-late_stage_buckets_count:])
        late_stage_ratio = late_stage_commits / total_capped_commits

        if late_stage_ratio > cls.PROCRASTINATION_THRESHOLD:
            alerts.append({
                "type": "procrastination_risk",
                "severity": "high",
                "message": f"Risco de Atraso/Qualidade: {late_stage_ratio:.1%} do esforço válido foi concentrado na reta final do projeto."
            })
            penalty += 30.0

        final_frequency_score = max(0.0, base_score - penalty)

        return round(final_frequency_score, 2), alerts