from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as projeto_router

app = FastAPI(
    title="Lighthouse Academic API",
    description="Motor stateless de análise de saúde para repositórios acadêmicos.",
    version="1.0.0"
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projeto_router)

@app.get("/", tags=["Health Check"])
def root():
    return {"message": "Lighthouse Academic API operante. Acesse /docs para o Swagger."}