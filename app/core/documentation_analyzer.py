from typing import List, Dict, Tuple

class DocumentationAnalyzer:
    MIN_VALID_SIZE_BYTES = 1024

    @classmethod
    def calculate(
        cls, 
        tracked_docs: List[Dict], 
        uses_external_docs: bool, 
        is_post_deadline: bool
    ) -> Tuple[float, List[Dict]]:
        """
        Avalia a saúde da documentação baseada em volume e configurações externas.
        """

        if not tracked_docs:
            message = "Nenhum arquivo de documentação encontrado nos diretórios configurados."
            return 0.0, [{"type": "missing_docs", "severity": "high", "message": message}]
        
        alerts = []
        valid_docs_count = 0
        total_docs = len(tracked_docs)

        for doc in tracked_docs:
            size = doc.get("size_bytes", 0)
            
            if size >= cls.MIN_VALID_SIZE_BYTES:
                valid_docs_count += 1
            else:
                alerts.append({
                    "type": "insufficient_doc_volume",
                    "severity": "medium",
                    "message": f"O arquivo {doc.get('file_path')} parece ser apenas um template vazio ({size} bytes)."
                })

        base_score = (valid_docs_count / total_docs) * 100

        if uses_external_docs:
            if is_post_deadline and base_score < 100:
                alerts.append({
                    "type": "external_docs_missing",
                    "severity": "high",
                    "message": "Uso de docs externos declarado, mas a versão final não foi anexada ao repositório dentro do prazo."
                })
                return 0.0, alerts
            
            elif not is_post_deadline:
                return 100.0, []
        
        return round(base_score, 2), alerts