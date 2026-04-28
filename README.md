# Lighthouse Academic API

![Lighthouse CI](https://github.com/Danil0Ribeir0/LighthouseAcademic/actions/workflows/ci.yml/badge.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.136.1-009485)
![License](https://img.shields.io/badge/license-MIT-green)

**Lighthouse Academic** é um mecanismo stateless de análise de saúde para repositórios acadêmicos, implementado como uma API RPC 2.0. Fornece diagnósticos quantitativos e automatizados sobre engajamento, consistência e equidade de colaboração em projetos de software, integrando-se nativamente com a API GraphQL v4 do GitHub.

## Visão Geral

A plataforma avalia repositórios acadêmicos através de três pilares analíticos ortogonais, gerando um score de saúde consolidado (0-100) e alertas contextualizados. Ideal para professores, gestores e estudantes que necessitam de auditoria objetiva sobre dinâmica colaborativa.

### Arquitetura Técnica

- **RPC 2.0 Compliant**: Interface baseada em JSON-RPC com envelope padronizado, versionamento de API e ID de rastreabilidade.
- **GraphQL Native**: Integração com GitHub API v4, eliminando problemas de N+1 queries.
- **Arquitetura de Adaptadores**: Padrão Strategy/Adapter para persistência. Core analítico desacoplado de banco de dados.
- **Motor Analítico Ponderado**: Algoritmos customizados para detecção de padrões críticos (Risco de Herói, Procrastinação).
- **Containerizado**: Dockerfile fornecido para deployment em Cloud-native environments.
- **CORS Ativo**: Integração transparente com frontends modernos (React, Vue, Angular).

## Modelo Analítico

O score final é calculado como uma média ponderada de três dimensões ortogonais:

| Métrica | Peso Padrão | Descrição |
|---------|-------------|-----------|
| **Frequência de Commits** | 40% | Mede constância e distribuição temporal do trabalho ao longo do cronograma. Baseado em análise de "buckets" temporais com detecção de períodos de inatividade crítica. |
| **Presença de Documentação** | 40% | Avalia volume (bytes) e completude de artefatos de documentação essenciais (README.md, wikis, specifications). |
| **Equidade de Membros** | 20% | Analisa distribuição de linhas de código e commits, acionando alertas para desequilíbrios (membros fantasmas ou heróis). |

**Fórmula**: `score = (freq × 0.4) + (doc × 0.4) + (equity × 0.2)`

## Pré-requisitos

- **Python 3.10+**
- **GitHub Personal Access Token (PAT)** com escopos: `repo`, `read:org` (obtém histórico de commits e metadados)
- **Docker** (opcional, para containerização)

## Instalação e Execução

### Setup Local (Desenvolvimento)

1. **Clone o repositório**
   ```bash
   git clone https://github.com/Danil0Ribeir0/LighthouseAcademic.git
   cd LighthouseAcademic
   ```

2. **Crie e ative o ambiente virtual**
   ```bash
   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure variáveis de ambiente** (opcional)
   ```bash
   export GITHUB_TOKEN="ghp_seu_token_aqui"  # Linux/macOS
   # ou
   $env:GITHUB_TOKEN = "ghp_seu_token_aqui"  # Windows PowerShell
   ```

5. **Inicie o servidor de desenvolvimento**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   
   Acesse: `http://localhost:8000/docs` (Swagger UI interativo)

### Setup com Docker

```bash
# Build da imagem
docker build -t lighthouse-academic:latest .

# Execução do container
docker run -d \
  --name lighthouse \
  -p 8000:8000 \
  -e GITHUB_TOKEN="ghp_seu_token_aqui" \
  lighthouse-academic:latest
```

**Health Check**: `curl http://localhost:8000/`
## Contrato da API (RPC 2.0)

### Endpoint Principal

```
POST /v1/services/analyzer/compute-health-score
Content-Type: application/json
```

### Request (Payload)

```json
{
  "repository": {
    "provider": "github",
    "url": "https://github.com/Danil0Ribeir0/LighthouseAcademic",
    "branch": "main",
    "access_token": "ghp_xxxxxxxxxxxxxxxxx"
  },
  "deadline": "2026-12-31T23:59:59Z",
  "expected_members": ["Danil0Ribeir0", "contributor2"],
  "config": {
    "weights": {
      "commit_frequency": 0.4,
      "doc_presence": 0.4,
      "member_equity": 0.2
    },
    "bucket_size_days": 7,
    "uses_external_docs": false,
    "doc_directories": ["docs/", "wikis/"]
  }
}
```

**Campos obrigatórios**:
- `repository.provider` (string): `"github"` (versão inicial; `"gitlab"` em roadmap)
- `repository.url` (string): URL completa do repositório
- `repository.access_token` (string): GitHub PAT com escopo mínimo `repo:read`
- `deadline` (ISO 8601): Data limite do projeto
- `expected_members` (array): Lista de usernames esperados como colaboradores

**Campos opcionais em `config`**:
- `weights` (object): Pesos customizados (default: 0.4/0.4/0.2)
- `bucket_size_days` (integer): Granularidade temporal da análise (default: 7)
- `uses_external_docs` (boolean): Se documentação é hospedada externamente (default: false)
- `doc_directories` (array): Diretórios a rastrear (default: `["docs/", "README.md"]`)

### Response (Envelope RPC 2.0)

```json
{
  "jsonrpc": "2.0",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-04-28T14:30:00Z",
  "result": {
    "summary": {
      "health_score": 85.5,
      "status": "healthy",
      "alerts": [
        {
          "type": "hero_risk",
          "severity": "warning",
          "message": "Membros com >50% das contribuições detectados",
          "member": "Danil0Ribeir0"
        }
      ]
    },
    "metrics": {
      "commit_frequency_score": 90.0,
      "doc_presence_score": 100.0,
      "member_equity_score": 70.0
    },
    "raw_data": {
      "repository_timeline": {
        "commits": [...],
        "date_range": { "start": "2026-01-15T00:00:00Z", "end": "2026-04-28T14:30:00Z" }
      },
      "members_activity": [
        {
          "username": "Danil0Ribeir0",
          "commits": 42,
          "lines_added": 3250,
          "lines_deleted": 1100,
          "issues_interacted": 8
        }
      ],
      "documents_tracked": [
        {
          "file_path": "README.md",
          "last_modified": "2026-04-20T10:15:00Z",
          "size_bytes": 4096,
          "modification_count": 5
        }
      ]
    }
  }
}
```

**Interpretação dos Status**:

| Status | Intervalo Score | Significado |
|--------|-----------------|-------------|
| `excellent` | 90-100 | Projeto em excelente saúde |
| `healthy` | 75-89 | Projeto saudável, monitorar alertas |
| `concerning` | 50-74 | Projeto com problemas moderados; investigar |
| `critical` | <50 | Projeto em risco severo; ação imediata recomendada |

### Tratamento de Erros

```json
{
  "jsonrpc": "2.0",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "error": {
    "code": -32600,
    "message": "Invalid Request",
    "data": "GitHub token inválido ou expirado"
  }
}
```

**Códigos de erro comuns**:
- `-32600`: Invalid Request (payload malformado)
- `-32601`: Method not found (endpoint inválido)
- `-32700`: Parse error (JSON inválido)
- `401`: Autenticação GitHub falhou
- `404`: Repositório não encontrado
- `403`: Sem permissão para acessar (token insuficiente)
## Arquitetura e Extensibilidade

### Padrão de Adaptadores

O projeto utiliza o **padrão Strategy/Adapter** para desacoplamento de persistência. Por padrão, análises são salvaguardadas em JSON no diretório `data/analyses/`, mas o core analítico permanece totalmente independente de banco de dados.

**Estrutura de diretórios**:
```
app/
├── core/                    # Lógica analítica pura (engine)
│   ├── analyzer.py         # Orquestrador central
│   ├── frequency_analyzer.py
│   ├── documentation_analyzer.py
│   └── equity_analyzer.py
├── adapters/                # Camada de persistência plugável
│   ├── output_adapter.py   # Interface abstrata
│   └── json_file_adapter.py # Implementação padrão (JSON)
├── services/                # Integração externa
│   ├── github_client.py
│   ├── github_queries.py
│   └── repository_extractor.py
├── api/                     # Camada HTTP/RPC
│   ├── routes.py
│   ├── dependencies.py     # Injeção de dependência
│   └── middleware/
├── models/
│   └── schemas.py          # Pydantic models (validação)
└── main.py                 # Aplicação FastAPI
```

### Implementar Adapter Customizado

Para integrar sua própria base de dados (PostgreSQL, MongoDB, etc.):

1. **Crie uma classe herdando de `AnalysisOutputAdapter`** em `app/adapters/custom_adapter.py`:
   ```python
   from app.adapters.output_adapter import AnalysisOutputAdapter
   from app.models.schemas import RPCResponse
   
   class PostgreSQLAdapter(AnalysisOutputAdapter):
       def __init__(self, connection_string: str):
           self.conn_string = connection_string
       
       def save_result(self, response: RPCResponse) -> None:
           # Implementação: persistir RPCResponse em PostgreSQL
           pass
   ```

2. **Registre a dependência em `app/api/dependencies.py`**:
   ```python
   from app.adapters.custom_adapter import PostgreSQLAdapter
   
   def get_output_adapter() -> AnalysisOutputAdapter:
       return PostgreSQLAdapter("postgresql://user:pass@localhost/lighthouse")
   ```

3. **Reinicie a aplicação** — a injeção de dependência cuidará do resto.

### Fluxo de Processamento

```
Cliente (POST request)
    ↓
[RPC Validation Layer]
    ↓
[GitHub Extractor]  ← Consultas GraphQL v4
    ↓
[Raw Data Pipeline]
    ├─→ Frequency Analyzer
    ├─→ Documentation Analyzer
    └─→ Equity Analyzer
    ↓
[Consolidation Engine]  ← Ponderação e alertas
    ↓
[Output Adapter]  ← Persistência abstrata
    ↓
[RPC Response Envelope] → Cliente
```
## Testes

O projeto inclui suite completa de testes unitários e de integração com mocks para GitHub API.

### Executar todos os testes
```bash
pytest -v
```

### Executar com cobertura
```bash
pytest --cov=app --cov-report=html
```

### Filtrar por módulo
```bash
pytest tests/test_logic.py -v              # Testes de lógica analítica
pytest tests/test_routes.py -v             # Testes de API
pytest -k "frequency" -v                   # Testes contendo "frequency"
```

**Estrutura de testes**:
- `tests/test_logic.py`: Testes unitários dos analisadores (sem I/O externo)
- `tests/test_routes.py`: Testes de integração das rotas (com mocks de GitHub)

## Troubleshooting

### Erro: `401 Unauthorized` ao contactar GitHub

**Causa**: Token inválido, expirado ou sem permissões.

**Solução**:
```bash
# Valide o token no GitHub Settings → Developer settings → Personal access tokens
# Verifique escopos mínimos: repo, read:org
# Regenere o token se necessário
```

### Erro: `404 Repository not found`

**Causa**: Repositório privado ou URL inválida.

**Solução**:
- Verifique que a URL está completa: `https://github.com/owner/repo`
- Confirme que o token tem acesso ao repositório (mesmo sendo privado)

### Erro: `CORS error` no frontend

**Solução**: Verifique `app/main.py` — os origins configurados incluem seu frontend:
```python
origins = [
    "http://localhost:3000",  # React
    "http://localhost:5173",  # Vite
    "*",  # Desenvolvimento (remover em produção)
]
```

### Container Docker não inicia

**Causa**: Variável `GITHUB_TOKEN` não definida ou porta 8000 já em uso.

**Solução**:
```bash
# Verifique se a porta está disponível
lsof -i :8000

# Libere a porta ou use outra
docker run -p 8080:8000 lighthouse-academic:latest

# Confirme a variável de ambiente
docker logs lighthouse
```

## Performance e Benchmarks

- **GitHub API GraphQL**: ~500ms-1s por análise (depende do tamanho do histórico)
- **Processamento analítico**: ~100-200ms (core puro)
- **Memory footprint**: ~150MB (container Docker slim)
- **Throughput**: ~50 análises/min (com rate limiting do GitHub: 5000 req/hora)

**Otimizações recomendadas**:
- Implemente cache de repositórios analisados recentemente (Redis)
- Batch requests para múltiplos repositórios
- Use branch específico para reduzir histórico de commits

## Roadmap

- [ ] Suporte a GitLab (API v4)
- [ ] Suporte a Gitea
- [ ] Alertas em tempo real (webhooks)
- [ ] Dashboard visual (React/Vue)
- [ ] Exportação em PDF
- [ ] Análise de Issues e Pull Requests
- [ ] Métricas de qualidade de código (Sonarqube integration)

## Exemplos de Uso

### cURL

```bash
curl -X POST http://localhost:8000/v1/services/analyzer/compute-health-score \
  -H "Content-Type: application/json" \
  -d '{
    "repository": {
      "provider": "github",
      "url": "https://github.com/owner/repo",
      "branch": "main",
      "access_token": "ghp_xxxxx"
    },
    "deadline": "2026-12-31T23:59:59Z",
    "expected_members": ["user1", "user2"]
  }'
```

### Python

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/services/analyzer/compute-health-score",
    json={
        "repository": {
            "provider": "github",
            "url": "https://github.com/owner/repo",
            "branch": "main",
            "access_token": "ghp_xxxxx"
        },
        "deadline": "2026-12-31T23:59:59Z",
        "expected_members": ["user1", "user2"]
    }
)
print(response.json())
```

## Documentação Adicional

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [GitHub GraphQL API v4](https://docs.github.com/en/graphql)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [Docker Documentation](https://docs.docker.com)

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFuncionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

**Diretrizes**:
- Mantenha o padrão de código (Type hints em Python 3.10+)
- Adicione testes para novas funcionalidades
- Atualize documentação conforme necessário
- Siga princípios de Clean Architecture

## Licença

Este projeto é distribuído sob licença MIT. Veja o arquivo LICENSE para detalhes.

## Autoria e Suporte

Desenvolvido por **Danilo Ribeiro**.

Para reportar bugs, sugestões ou questões:
- 📧 Abra uma [Issue no GitHub](https://github.com/Danil0Ribeir0/LighthouseAcademic/issues)
- 💬 Veja as [Discussions](https://github.com/Danil0Ribeir0/LighthouseAcademic/discussions)

---

**Última atualização**: Abril 2026  
**Versão Stable**: 1.0.0  
**Status**: ✅ Produção