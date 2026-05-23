from typing import Any, Dict, List

from fastapi import APIRouter, Body, HTTPException, Path, Query
from psycopg import sql

from app.api.db import delete_row, fetch_all, fetch_one, insert_row, update_row

router = APIRouter(prefix="/users", tags=["Usuários"])


@router.get(
    "",
    response_model=List[Dict[str, Any]],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "00000000-0000-0000-0000-000000000123",
                            "username": "aventureiro123",
                            "password": "senha_super_secreta",
                            "high_score": 4200,
                            "active": True,
                        }
                    ]
                }
            }
        }
    },
)
def list_users(
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
        table=sql.Identifier("users")
    )
    return fetch_all(query, {"limit": limit, "offset": offset})


@router.get(
    "/{user_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "id": "00000000-0000-0000-0000-000000000123",
                        "username": "aventureiro123",
                        "password": "senha_super_secreta",
                        "high_score": 4200,
                        "active": True,
                    }
                }
            }
        }
    },
)
def get_user(
    user_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID do usuário",
                "value": "00000000-0000-0000-0000-000000000123",
            }
        },
    )
):
    query = sql.SQL("SELECT * FROM {table} WHERE id = %(target_id)s").format(
        table=sql.Identifier("users")
    )
    response = fetch_one(query, {"target_id": user_id})
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
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
                        "id": "00000000-0000-0000-0000-000000000123",
                        "username": "aventureiro123",
                        "password": "senha_super_secreta",
                        "high_score": 0,
                        "active": True,
                    }
                }
            }
        }
    },
)
def create_user(
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "username": "aventureiro123",
            "password": "senha_super_secreta",
            "high_score": 0,
            "active": True,
        },
        examples={
            "criar": {
                "summary": "Criar usuário",
                "value": {
                    "username": "aventureiro123",
                    "password": "senha_super_secreta",
                    "high_score": 0,
                    "active": True,
                },
            }
        },
    )
):
    return insert_row("users", payload)


@router.patch(
    "/{user_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "id": "00000000-0000-0000-0000-000000000123",
                        "username": "aventureiro123",
                        "password": "senha_super_secreta",
                        "high_score": 4200,
                        "active": True,
                    }
                }
            }
        }
    },
)
def update_user(
    user_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID do usuário",
                "value": "00000000-0000-0000-0000-000000000123",
            }
        },
    ),
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "high_score": 4200,
            "active": True,
        },
        examples={
            "atualizar": {
                "summary": "Atualizar usuário",
                "value": {
                    "high_score": 4200,
                    "active": True,
                },
            }
        },
    ),
):
    response = update_row("users", user_id, payload)
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    return response


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID do usuário",
                "value": "00000000-0000-0000-0000-000000000123",
            }
        },
    )
):
    response = delete_row("users", user_id)
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    return None