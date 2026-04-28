from fastapi import FastAPI

app = FastAPI(
    title="Lighthouse Academic API",
    description="Motor stateless de análise de saúde para repositórios acadêmicos.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Lighthouse Academic API operante. Acesse /docs para o Swagger."}