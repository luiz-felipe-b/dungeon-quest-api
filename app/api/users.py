from typing import Any, Dict, List
import hashlib
import os

from fastapi import APIRouter, Body, HTTPException, Path, Query
from psycopg import sql

from app.api.db import delete_row, fetch_all, fetch_one, insert_row, update_row

router = APIRouter(prefix="/users", tags=["Usuários"])


def hash_password(password: str) -> str:
    if not isinstance(password, str) or not password:
        raise HTTPException(status_code=400, detail="password must be a non-empty string")
    salt = os.getenv("PASSWORD_SALT", "")
    digest = hashlib.sha256(f"{salt}{password}".encode("utf-8")).hexdigest()
    return digest


def strip_encrypted_password(user: Dict[str, Any]) -> Dict[str, Any]:
    sanitized = dict(user)
    sanitized.pop("encrypted_password", None)
    return sanitized


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
                            "user_name": "aventureiro123",
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
    query = sql.SQL(
        "SELECT id, user_name, high_score, active FROM {table} LIMIT %(limit)s OFFSET %(offset)s"
    ).format(table=sql.Identifier("users"))
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
                        "user_name": "aventureiro123",
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
    query = sql.SQL(
        "SELECT id, user_name, high_score, active FROM {table} WHERE id = %(target_id)s"
    ).format(table=sql.Identifier("users"))
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
                        "user_name": "aventureiro123",
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
            "user_name": "aventureiro123",
            "password": "senha_super_secreta",
            "high_score": 0,
            "active": True,
        },
        examples={
            "criar": {
                "summary": "Criar usuário",
                "value": {
                    "user_name": "aventureiro123",
                    "password": "senha_super_secreta",
                    "high_score": 0,
                    "active": True,
                },
            }
        },
    )
):
    if "password" not in payload:
        raise HTTPException(status_code=400, detail="password is required")
    to_insert = dict(payload)
    to_insert["encrypted_password"] = hash_password(str(to_insert.pop("password")))
    created = insert_row("users", to_insert)
    return strip_encrypted_password(created)


@router.patch(
    "/{user_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "id": "00000000-0000-0000-0000-000000000123",
                        "user_name": "aventureiro123",
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
    to_update = dict(payload)
    if "password" in to_update:
        to_update["encrypted_password"] = hash_password(str(to_update.pop("password")))
    response = update_row("users", user_id, to_update)
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    return strip_encrypted_password(response)


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


@router.post(
    "/login",
    response_model=Dict[str, bool],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {"valid": True}
                }
            }
        }
    },
)
def login_user(
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "user_name": "aventureiro123",
            "password": "senha_super_secreta",
        },
        examples={
            "login": {
                "summary": "Login de usuário",
                "value": {
                    "user_name": "aventureiro123",
                    "password": "senha_super_secreta",
                },
            }
        },
    )
):
    user_name = payload.get("user_name")
    password = payload.get("password")
    if not user_name or not password:
        raise HTTPException(status_code=400, detail="user_name and password are required")
    query = sql.SQL(
        "SELECT encrypted_password FROM {table} WHERE user_name = %(user_name)s"
    ).format(table=sql.Identifier("users"))
    record = fetch_one(query, {"user_name": user_name})
    if not record:
        return {"valid": False}
    return {"valid": record.get("encrypted_password") == hash_password(str(password))}