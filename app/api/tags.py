from typing import Any, Dict, List

from fastapi import APIRouter, Body, HTTPException, Path, Query
from psycopg import sql

from app.api.db import delete_row, fetch_all, fetch_one, insert_row, update_row

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get(
    "",
    response_model=List[Dict[str, Any]],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "00000000-0000-0000-0000-000000000456",
                            "label": "historia",
                        }
                    ]
                }
            }
        }
    },
)
def list_tags(
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
        table=sql.Identifier("tags")
    )
    return fetch_all(query, {"limit": limit, "offset": offset})


@router.get(
    "/{tag_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "id": "00000000-0000-0000-0000-000000000456",
                        "label": "historia",
                    }
                }
            }
        }
    },
)
def get_tag(
    tag_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da tag",
                "value": "00000000-0000-0000-0000-000000000456",
            }
        },
    )
):
    query = sql.SQL("SELECT * FROM {table} WHERE id = %(target_id)s").format(
        table=sql.Identifier("tags")
    )
    response = fetch_one(query, {"target_id": tag_id})
    if not response:
        raise HTTPException(status_code=404, detail="Tag not found")
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
                        "id": "00000000-0000-0000-0000-000000000456",
                        "label": "historia",
                    }
                }
            }
        }
    },
)
def create_tag(
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "label": "historia",
        },
        examples={
            "criar": {
                "summary": "Criar tag",
                "value": {
                    "label": "historia",
                },
            }
        },
    )
):
    return insert_row("tags", payload)


@router.patch(
    "/{tag_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "id": "00000000-0000-0000-0000-000000000456",
                        "label": "geografia",
                    }
                }
            }
        }
    },
)
def update_tag(
    tag_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da tag",
                "value": "00000000-0000-0000-0000-000000000456",
            }
        },
    ),
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "label": "geografia",
        },
        examples={
            "atualizar": {
                "summary": "Atualizar tag",
                "value": {
                    "label": "geografia",
                },
            }
        },
    ),
):
    response = update_row("tags", tag_id, payload)
    if not response:
        raise HTTPException(status_code=404, detail="Tag not found")
    return response


@router.delete("/{tag_id}", status_code=204)
def delete_tag(
    tag_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da tag",
                "value": "00000000-0000-0000-0000-000000000456",
            }
        },
    )
):
    response = delete_row("tags", tag_id)
    if not response:
        raise HTTPException(status_code=404, detail="Tag not found")
    return None