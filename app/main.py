from fastapi import FastAPI
from app.api.routes import router as projeto_router

app = FastAPI(
    title="Lighthouse Academic API",
    description="Motor stateless de análise de saúde para repositórios acadêmicos.",
    version="1.0.0"
)

app.include_router(projeto_router)

@app.get("/", tags=["Health Check"])
def root():
    return {"message": "Lighthouse Academic API operante. Acesse /docs para o Swagger."}