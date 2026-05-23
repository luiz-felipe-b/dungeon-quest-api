from typing import Any, Dict, List

from fastapi import APIRouter, Body, HTTPException, Path, Query
from psycopg import sql

from app.api.db import delete_row, fetch_all, fetch_one, insert_row, update_row

router = APIRouter(prefix="/choices", tags=["Alternativas"])


@router.get(
    "",
    response_model=List[Dict[str, Any]],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "00000000-0000-0000-0000-000000000321",
                            "label": "Brasilia",
                            "question_id": "00000000-0000-0000-0000-000000000010",
                        }
                    ]
                }
            }
        }
    },
)
def list_choices(
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
        table=sql.Identifier("choices")
    )
    return fetch_all(query, {"limit": limit, "offset": offset})


@router.get(
    "/{choice_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "id": "00000000-0000-0000-0000-000000000321",
                        "label": "Brasilia",
                        "question_id": "00000000-0000-0000-0000-000000000010",
                    }
                }
            }
        }
    },
)
def get_choice(
    choice_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da alternativa",
                "value": "00000000-0000-0000-0000-000000000321",
            }
        },
    )
):
    query = sql.SQL("SELECT * FROM {table} WHERE id = %(target_id)s").format(
        table=sql.Identifier("choices")
    )
    response = fetch_one(query, {"target_id": choice_id})
    if not response:
        raise HTTPException(status_code=404, detail="Choice not found")
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
                        "id": "00000000-0000-0000-0000-000000000321",
                        "label": "Brasilia",
                        "question_id": "00000000-0000-0000-0000-000000000010",
                    }
                }
            }
        }
    },
)
def create_choice(
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "label": "Brasilia",
            "question_id": "00000000-0000-0000-0000-000000000010",
        },
        examples={
            "criar": {
                "summary": "Criar alternativa",
                "value": {
                    "label": "Brasília",
                    "question_id": "00000000-0000-0000-0000-000000000010",
                },
            }
        },
    )
):
    return insert_row("choices", payload)


@router.patch(
    "/{choice_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "id": "00000000-0000-0000-0000-000000000321",
                        "label": "Rio de Janeiro",
                        "question_id": "00000000-0000-0000-0000-000000000010",
                    }
                }
            }
        }
    },
)
def update_choice(
    choice_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da alternativa",
                "value": "00000000-0000-0000-0000-000000000321",
            }
        },
    ),
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "label": "Rio de Janeiro",
        },
        examples={
            "atualizar": {
                "summary": "Atualizar alternativa",
                "value": {
                    "label": "Rio de Janeiro",
                },
            }
        },
    ),
):
    response = update_row("choices", choice_id, payload)
    if not response:
        raise HTTPException(status_code=404, detail="Choice not found")
    return response


@router.delete("/{choice_id}", status_code=204)
def delete_choice(
    choice_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da alternativa",
                "value": "00000000-0000-0000-0000-000000000321",
            }
        },
    )
):
    response = delete_row("choices", choice_id)
    if not response:
        raise HTTPException(status_code=404, detail="Choice not found")
    return None