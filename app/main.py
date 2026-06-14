from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.choices import router as choices_router
from app.api.questions import router as questions_router
from app.api.question_packs import router as question_packs_router
from app.api.rooms import router as rooms_router
from app.api.tags import router as tags_router
from app.api.users import router as users_router

openapi_tags = [
    {"name": "Usuários", "description": "Operações relacionadas aos usuários do jogo."},
    {"name": "Tags", "description": "Gerenciamento de tags de perguntas."},
    {"name": "Perguntas", "description": "CRUD de perguntas do jogo."},
    {"name": "Alternativas", "description": "CRUD de alternativas para perguntas."},
    {"name": "Pacotes de Perguntas", "description": "CRUD de pacotes de perguntas e gerenciamento de questões."},
    {"name": "Salas", "description": "CRUD de salas e gerenciamento de usuários nas salas."},
]

app = FastAPI(
    title="API Dungeon Quest 2",
    description="Backend em FastAPI para o jogo Dungeon Quest 2.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get(
    "/health",
    responses={
        200: {
            "content": {
                "application/json": {"example": {"response": {"status": "ok"}}}
            }
        }
    },
)
def health_check() -> Dict[str, str]:
    return {"response": {"status": "ok"}}

app.include_router(users_router, prefix="/api")
app.include_router(tags_router, prefix="/api")
app.include_router(questions_router, prefix="/api")
app.include_router(choices_router, prefix="/api")
app.include_router(question_packs_router, prefix="/api")
app.include_router(rooms_router, prefix="/api")

