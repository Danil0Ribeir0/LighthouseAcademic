from datetime import datetime, timezone, timedelta
from app.core.frequency_analyzer import FrequencyAnalyzer

def test_frequency_analyzer_calculates_correct_score():
    deadline = datetime(2026, 12, 31, tzinfo=timezone.utc)
    start_date = deadline - timedelta(days=70)

    commits_falsos = [
        {"commit": {"author": {"date": (start_date + timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ")}}},
        {"commit": {"author": {"date": (start_date + timedelta(days=12)).strftime("%Y-%m-%dT%H:%M:%SZ")}}},
    ]

    score, alerts = FrequencyAnalyzer.calculate(
        commits=commits_falsos,
        start_date=start_date,
        deadline=deadline,
        bucket_size_days=7
    )

    assert score > 0
    assert isinstance(alerts, list)
    
    alert_types = [a["type"] for a in alerts]
    assert "low_consistency" in alert_types