from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import List, Optional, Dict, Any

class RepositoryInfo(BaseModel):
    provider: str = Field(..., json_schema_extra={"example": "github"})
    url: HttpUrl
    branch: str = "main"
    access_token: Optional[str] = None

class AnalysisConfig(BaseModel):
    doc_directories: List[str] = ["/docs"]
    doc_extensions: List[str] = [".text", ".md", ".pdf"]
    weights: Dict[str, float] = {
        "commit_frequency": 0.4,
        "doc_presence": 0.4,
        "member_equity": 0.2
    }
    bucket_size_days: Optional[int] = None
    uses_external_docs: bool = False

class ProjectAnalysisRequest(BaseModel):
    repository: RepositoryInfo
    deadline: datetime
    expected_members: List[str]
    config: AnalysisConfig = Field(default_factory=AnalysisConfig)

class Alert(BaseModel):
    type: str
    severity: str
    message: str

class MemberActivity(BaseModel):
    username: str
    commits: int
    lines_added: int
    lines_deleted: int
    issues_interacted: int

class DocumentInfo(BaseModel):
    file_path: str
    last_modified: datetime
    size_bytes: int
    modification_count: int

class Summary(BaseModel):
    health_score: float
    status: str
    alerts: List[Alert]

class AnalysisResponse(BaseModel):
    summary: Summary
    metrics: Dict[str, float]
    raw_data: Dict[str, Any]

class RPCResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    timestamp: datetime
    result: AnalysisResponse