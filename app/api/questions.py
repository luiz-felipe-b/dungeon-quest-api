from typing import Any, Dict, List

from fastapi import APIRouter, Body, HTTPException, Path, Query
from psycopg import sql

from app.api.db import delete_row, fetch_all, fetch_one, insert_row, update_row

router = APIRouter(prefix="/questions", tags=["Perguntas"])


@router.get(
    "",
    response_model=List[Dict[str, Any]],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "00000000-0000-0000-0000-000000000789",
                            "prompt": "Qual e a capital do Brasil?",
                            "answer_id": "00000000-0000-0000-0000-000000000000",
                            "answer_explanation": "Brasilia e a capital do Brasil.",
                            "tag_ids": [
                                "00000000-0000-0000-0000-000000000001",
                                "00000000-0000-0000-0000-000000000002",
                            ],
                        }
                    ]
                }
            }
        }
    },
)
def list_questions(
    limit: int = Query(
        50,
        ge=1,
        le=100,
        examples={"limite": {"summary": "Limite de registros", "value": 20}},
    ),
    offset: int = Query(
        0,
        ge=0,
        examples={"deslocamento": {"summary": "Offset de registros", "value": 0}},
    ),
):
    query = sql.SQL("SELECT * FROM {table} LIMIT %(limit)s OFFSET %(offset)s").format(
        table=sql.Identifier("questions")
    )
    return fetch_all(query, {"limit": limit, "offset": offset})


@router.get(
    "/{question_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "id": "00000000-0000-0000-0000-000000000789",
                        "prompt": "Qual e a capital do Brasil?",
                        "answer_id": "00000000-0000-0000-0000-000000000000",
                        "answer_explanation": "Brasilia e a capital do Brasil.",
                        "tag_ids": [
                            "00000000-0000-0000-0000-000000000001",
                            "00000000-0000-0000-0000-000000000002",
                        ],
                    }
                }
            }
        }
    },
)
def get_question(
    question_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da pergunta",
                "value": "00000000-0000-0000-0000-000000000789",
            }
        },
    )
):
    query = sql.SQL("SELECT * FROM {table} WHERE id = %(target_id)s").format(
        table=sql.Identifier("questions")
    )
    response = fetch_one(query, {"target_id": question_id})
    if not response:
        raise HTTPException(status_code=404, detail="Question not found")
    return response


@router.post(
    "",
    response_model=Dict[str, Any],
    status_code=201,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "id": "00000000-0000-0000-0000-000000000789",
                        "prompt": "Qual e a capital do Brasil?",
                        "answer_id": "00000000-0000-0000-0000-000000000000",
                        "answer_explanation": "Brasilia e a capital do Brasil.",
                        "tag_ids": [
                            "00000000-0000-0000-0000-000000000001",
                            "00000000-0000-0000-0000-000000000002",
                        ],
                    }
                }
            }
        }
    },
)
def create_question(
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "prompt": "Qual e a capital do Brasil?",
            "answer_id": "00000000-0000-0000-0000-000000000000",
            "answer_explanation": "Brasilia e a capital do Brasil.",
            "tag_ids": [
                "00000000-0000-0000-0000-000000000001",
                "00000000-0000-0000-0000-000000000002",
            ],
        },
        examples={
            "criar": {
                "summary": "Criar pergunta",
                "value": {
                    "prompt": "Qual é a capital do Brasil?",
                    "answer_id": "00000000-0000-0000-0000-000000000000",
                    "answer_explanation": "Brasília é a capital do Brasil.",
                    "tag_ids": [
                        "00000000-0000-0000-0000-000000000001",
                        "00000000-0000-0000-0000-000000000002"
                    ]
                },
            }
        },
    )
):
    return insert_row("questions", payload)


@router.patch(
    "/{question_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "id": "00000000-0000-0000-0000-000000000789",
                        "prompt": "Qual e a capital da Argentina?",
                        "answer_id": "00000000-0000-0000-0000-000000000000",
                        "answer_explanation": "Buenos Aires e a capital da Argentina.",
                        "tag_ids": ["00000000-0000-0000-0000-000000000003"],
                    }
                }
            }
        }
    },
)
def update_question(
    question_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da pergunta",
                "value": "00000000-0000-0000-0000-000000000789",
            }
        },
    ),
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "prompt": "Qual e a capital da Argentina?",
            "answer_explanation": "Buenos Aires e a capital da Argentina.",
            "tag_ids": ["00000000-0000-0000-0000-000000000003"],
        },
        examples={
            "atualizar": {
                "summary": "Atualizar pergunta",
                "value": {
                    "prompt": "Qual é a capital da Argentina?",
                    "answer_explanation": "Buenos Aires é a capital da Argentina.",
                    "tag_ids": ["00000000-0000-0000-0000-000000000003"],
                },
            }
        },
    ),
):
    response = update_row("questions", question_id, payload)
    if not response:
        raise HTTPException(status_code=404, detail="Question not found")
    return response


@router.delete("/{question_id}", status_code=204)
def delete_question(
    question_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da pergunta",
                "value": "00000000-0000-0000-0000-000000000789",
            }
        },
    )
):
    response = delete_row("questions", question_id)
    if not response:
        raise HTTPException(status_code=404, detail="Question not found")
    return None