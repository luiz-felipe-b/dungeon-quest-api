from typing import Any, Dict, List
import random
import string

from fastapi import APIRouter, Body, HTTPException, Path, Query
from psycopg import sql

from app.api.db import delete_row, fetch_all, fetch_one, insert_row, update_row

router = APIRouter(prefix="/rooms", tags=["Salas"])


def generate_room_code() -> str:
    """Generate a random 6-character code with uppercase letters and numbers."""
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(6))


@router.get(
    "",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "response": [
                            {
                                "id": "00000000-0000-0000-0000-000000000001",
                                "title": "Quiz Night",
                                "code": "QUIZ123",
                                "created_at": "2026-06-14T10:00:00Z",
                                "owner": "00000000-0000-0000-0000-000000000100",
                                "question_pack_id": "00000000-0000-0000-0000-000000000050",
                                "level_quantity": 10,
                                "tag_target": "variado"
                            }
                        ]
                    }
                }
            }
        }
    },
)
def list_rooms(
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
        table=sql.Identifier("rooms")
    )
    return {"response": fetch_all(query, {"limit": limit, "offset": offset})}


@router.get(
    "/code/{code}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "response": {
                            "id": "00000000-0000-0000-0000-000000000001",
                            "title": "Quiz Night",
                            "code": "QUIZ12",
                            "created_at": "2026-06-14T10:00:00Z",
                            "owner": "00000000-0000-0000-0000-000000000100",
                            "question_pack_id": "00000000-0000-0000-0000-000000000050",
                            "level_quantity": 10,
                            "tag_target": "variado"
                        }
                    }
                }
            }
        }
    },
)
def get_room_by_code(
    code: str = Path(
        ...,
        examples={
            "code": {
                "summary": "Código da sala",
                "value": "QUIZ12",
            }
        },
    )
):
    query = sql.SQL("SELECT * FROM {table} WHERE code = %(target_code)s").format(
        table=sql.Identifier("rooms")
    )
    room = fetch_one(query, {"target_code": code})
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"response": room}


@router.get(
    "/{room_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "response": {
                            "id": "00000000-0000-0000-0000-000000000001",
                            "title": "Quiz Night",
                            "code": "QUIZ123",
                            "created_at": "2026-06-14T10:00:00Z",
                            "owner": "00000000-0000-0000-0000-000000000100",
                            "question_pack_id": "00000000-0000-0000-0000-000000000050",
                            "level_quantity": 10,
                            "tag_target": "variado"
                        }
                    }
                }
            }
        }
    },
)
def get_room(
    room_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da sala",
                "value": "00000000-0000-0000-0000-000000000001",
            }
        },
    )
):
    query = sql.SQL("SELECT * FROM {table} WHERE id = %(target_id)s").format(
        table=sql.Identifier("rooms")
    )
    room = fetch_one(query, {"target_id": room_id})
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"response": room}


@router.post(
    "",
    response_model=Dict[str, Any],
    status_code=201,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "response": {
                            "id": "00000000-0000-0000-0000-000000000001",
                            "title": "Quiz Night",
                            "code": "QUIZ123",
                            "created_at": "2026-06-14T10:00:00Z",
                            "owner": "00000000-0000-0000-0000-000000000100",
                            "question_pack_id": "00000000-0000-0000-0000-000000000050",
                        }
                    }
                }
            }
        }
    },
)
def create_room(
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "title": "Quiz Night",
            "owner": "00000000-0000-0000-0000-000000000100",
            "question_pack_id": "00000000-0000-0000-0000-000000000050",
        },
        examples={
            "criar": {
                "summary": "Criar sala",
                "value": {
                    "title": "Quiz Night",
                    "owner": "00000000-0000-0000-0000-000000000100",
                    "question_pack_id": "00000000-0000-0000-0000-000000000050",
                },
            }
        },
    )
):
    if "title" not in payload or not payload.get("title"):
        raise HTTPException(status_code=400, detail="title is required")
    
    payload["code"] = generate_room_code()
    return {"response": insert_row("rooms", payload)}


@router.patch(
    "/{room_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "response": {
                            "id": "00000000-0000-0000-0000-000000000001",
                            "title": "Quiz Night 2",
                            "code": "QUIZ123",
                            "created_at": "2026-06-14T10:00:00Z",
                            "owner": "00000000-0000-0000-0000-000000000100",
                            "question_pack_id": "00000000-0000-0000-0000-000000000050",
                        }
                    }
                }
            }
        }
    },
)
def update_room(
    room_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da sala",
                "value": "00000000-0000-0000-0000-000000000001",
            }
        },
    ),
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "title": "Quiz Night 2",
            "question_pack_id": "00000000-0000-0000-0000-000000000051",
        },
        examples={
            "atualizar": {
                "summary": "Atualizar sala",
                "value": {
                    "title": "Quiz Night 2",
                    "question_pack_id": "00000000-0000-0000-0000-000000000051",
                },
            }
        },
    ),
):
    response = update_row("rooms", room_id, payload)
    if not response:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"response": response}


@router.delete("/{room_id}", status_code=200)
def delete_room(
    room_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da sala",
                "value": "00000000-0000-0000-0000-000000000001",
            }
        },
    )
):
    response = delete_row("rooms", room_id)
    if not response:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"response": None}


@router.get(
    "/{room_id}/users",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "response": [
                            {
                                "id": "00000000-0000-0000-0000-000000000200",
                                "user_id": "00000000-0000-0000-0000-000000000100",
                                "room_id": "00000000-0000-0000-0000-000000000001",
                                "score": 1500,
                                "created_at": "2026-06-14T10:00:00Z",
                            }
                        ]
                    }
                }
            }
        }
    },
)
def list_room_users(
    room_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da sala",
                "value": "00000000-0000-0000-0000-000000000001",
            }
        },
    ),
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
    query = sql.SQL("SELECT * FROM {table} WHERE room_id = %(room_id)s LIMIT %(limit)s OFFSET %(offset)s").format(
        table=sql.Identifier("users_rooms")
    )
    return {"response": fetch_all(query, {"room_id": room_id, "limit": limit, "offset": offset})}


@router.post(
    "/{room_id}/users",
    response_model=Dict[str, Any],
    status_code=201,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "response": {
                            "id": "00000000-0000-0000-0000-000000000200",
                            "user_id": "00000000-0000-0000-0000-000000000100",
                            "room_id": "00000000-0000-0000-0000-000000000001",
                            "score": 0,
                            "created_at": "2026-06-14T10:00:00Z",
                        }
                    }
                }
            }
        }
    },
)
def add_user_to_room(
    room_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da sala",
                "value": "00000000-0000-0000-0000-000000000001",
            }
        },
    ),
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "user_id": "00000000-0000-0000-0000-000000000100",
            "score": 0,
        },
        examples={
            "adicionar": {
                "summary": "Adicionar usuário à sala",
                "value": {
                    "user_id": "00000000-0000-0000-0000-000000000100",
                    "score": 0,
                },
            }
        },
    ),
):
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    query = sql.SQL("SELECT id FROM {table} WHERE id = %(target_id)s").format(
        table=sql.Identifier("rooms")
    )
    room = fetch_one(query, {"target_id": room_id})
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    query = sql.SQL("SELECT id FROM {table} WHERE id = %(target_id)s").format(
        table=sql.Identifier("users")
    )
    user = fetch_one(query, {"target_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    insertion_payload = {
        "user_id": user_id,
        "room_id": room_id,
        "score": payload.get("score", 0),
    }
    return {"response": insert_row("users_rooms", insertion_payload)}


@router.patch(
    "/{room_id}/users/{user_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "response": {
                            "id": "00000000-0000-0000-0000-000000000200",
                            "user_id": "00000000-0000-0000-0000-000000000100",
                            "room_id": "00000000-0000-0000-0000-000000000001",
                            "score": 2000,
                            "created_at": "2026-06-14T10:00:00Z",
                        }
                    }
                }
            }
        }
    },
)
def update_user_in_room(
    room_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da sala",
                "value": "00000000-0000-0000-0000-000000000001",
            }
        },
    ),
    user_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID do usuário",
                "value": "00000000-0000-0000-0000-000000000100",
            }
        },
    ),
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "score": 2000,
        },
        examples={
            "atualizar": {
                "summary": "Atualizar usuário na sala",
                "value": {
                    "score": 2000,
                },
            }
        },
    ),
):
    query = sql.SQL(
        "SELECT id FROM {table} WHERE user_id = %(user_id)s AND room_id = %(room_id)s"
    ).format(table=sql.Identifier("users_rooms"))
    relation = fetch_one(query, {"user_id": user_id, "room_id": room_id})
    if not relation:
        raise HTTPException(
            status_code=404, detail="User not found in this room"
        )

    update_query = sql.SQL(
        "UPDATE {table} SET {assignments} WHERE user_id = %(user_id)s AND room_id = %(room_id)s RETURNING *"
    ).format(
        table=sql.Identifier("users_rooms"),
        assignments=sql.SQL(", ").join(
            sql.SQL("{field} = {value}").format(
                field=sql.Identifier(key),
                value=sql.Placeholder(key),
            )
            for key in payload.keys()
        ),
    )
    params = {**payload, "user_id": user_id, "room_id": room_id}
    response = fetch_one(update_query, params)
    if not response:
        raise HTTPException(status_code=500, detail="Failed to update user in room")
    return {"response": response}


@router.delete(
    "/{room_id}/users/{user_id}",
    status_code=200,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "response": None,
                    }
                }
            }
        }
    },
)
def remove_user_from_room(
    room_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da sala",
                "value": "00000000-0000-0000-0000-000000000001",
            }
        },
    ),
    user_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID do usuário",
                "value": "00000000-0000-0000-0000-000000000100",
            }
        },
    ),
):
    query = sql.SQL(
        "DELETE FROM {table} WHERE user_id = %(user_id)s AND room_id = %(room_id)s RETURNING *"
    ).format(table=sql.Identifier("users_rooms"))
    response = fetch_one(
        query, {"user_id": user_id, "room_id": room_id}
    )
    if not response:
        raise HTTPException(
            status_code=404,
            detail="User not found in this room or room not found",
        )
    return {"response": None}
