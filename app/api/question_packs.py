from typing import Any, Dict, List

from fastapi import APIRouter, Body, HTTPException, Path, Query
from psycopg import sql

from app.api.db import delete_row, fetch_all, fetch_one, insert_row, update_row

router = APIRouter(prefix="/question-packs", tags=["Pacotes de Perguntas"])


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
                                "name": "Perguntas de História",
                                "created_at": "2026-06-14T10:00:00Z",
                                "created_by": "00000000-0000-0000-0000-000000000100",
                                "tags": ["historia", "medieval"]
                                # "questions": [
                                #     {
                                #         "id": "00000000-0000-0000-0000-000000000789",
                                #         "prompt": "Qual e a capital do Brasil?",
                                #     }
                                # ],
                            }
                        ]
                    }
                }
            }
        }
    },
)
def list_question_packs(
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
        table=sql.Identifier("question_packs")
    )
    packs = fetch_all(query, {"limit": limit, "offset": offset})
    if not packs:
        return {"response": packs}

    # pack_ids = [pack["id"] for pack in packs]
    # questions_query = sql.SQL(
    #     "SELECT q.id, q.prompt, qqp.question_pack_id FROM {questions} q "
    #     "INNER JOIN {qqp} qqp ON q.id = qqp.question_id "
    #     "WHERE qqp.question_pack_id = ANY(%(pack_ids)s) "
    #     "ORDER BY qqp.created_at"
    # ).format(
    #     questions=sql.Identifier("questions"),
    #     qqp=sql.Identifier("question_question_packs"),
    # )
    # questions = fetch_all(questions_query, {"pack_ids": pack_ids})
    # questions_by_pack: Dict[str, List[Dict[str, Any]]] = {}
    # for question in questions:
    #     pack_id = question.pop("question_pack_id")
    #     questions_by_pack.setdefault(pack_id, []).append(question)

    # for pack in packs:
    #     pack["questions"] = questions_by_pack.get(pack["id"], [])

    return {"response": packs}


@router.get(
    "/{pack_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "response": {
                            "id": "00000000-0000-0000-0000-000000000001",
                            "name": "Perguntas de História",
                            "created_at": "2026-06-14T10:00:00Z",
                            "created_by": "00000000-0000-0000-0000-000000000100",
                            "tags": ["historia", "medieval"],
                            "questions": [
                                {
                                    "id": "00000000-0000-0000-0000-000000000789",
                                    "prompt": "Qual e a capital do Brasil?",
                                }
                            ],
                        }
                    }
                }
            }
        }
    },
)
def get_question_pack(
    pack_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID do pacote de perguntas",
                "value": "00000000-0000-0000-0000-000000000001",
            }
        },
    )
):
    query = sql.SQL("SELECT * FROM {table} WHERE id = %(target_id)s").format(
        table=sql.Identifier("question_packs")
    )
    pack = fetch_one(query, {"target_id": pack_id})
    if not pack:
        raise HTTPException(status_code=404, detail="Question pack not found")

    # questions_query = sql.SQL(
    #     "SELECT q.id, q.prompt FROM {questions} q "
    #     "INNER JOIN {qqp} qqp ON q.id = qqp.question_id "
    #     "WHERE qqp.question_pack_id = %(pack_id)s "
    #     "ORDER BY qqp.created_at"
    # ).format(
    #     questions=sql.Identifier("questions"),
    #     qqp=sql.Identifier("question_question_packs"),
    # )
    # questions = fetch_all(questions_query, {"pack_id": pack_id})
    # pack["questions"] = questions

    return {"response": pack}


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
                            "name": "Perguntas de História",
                            "created_at": "2026-06-14T10:00:00Z",
                            "created_by": "00000000-0000-0000-0000-000000000100",
                            "tags": ["historia", "medieval"],
                        }
                    }
                }
            }
        }
    },
)
def create_question_pack(
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "name": "Perguntas de História",
            "created_by": "00000000-0000-0000-0000-000000000100",
            "tags": ["historia", "medieval"],
        },
        examples={
            "criar": {
                "summary": "Criar pacote de perguntas",
                "value": {
                    "name": "Perguntas de História",
                    "created_by": "00000000-0000-0000-0000-000000000100",
                    "tags": ["historia", "medieval"],
                },
            }
        },
    )
):
    return {"response": insert_row("question_packs", payload)}


@router.patch(
    "/{pack_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "response": {
                            "id": "00000000-0000-0000-0000-000000000001",
                            "name": "Perguntas de Geografia",
                            "created_at": "2026-06-14T10:00:00Z",
                            "created_by": "00000000-0000-0000-0000-000000000100",
                            "tags": ["geografia"],
                        }
                    }
                }
            }
        }
    },
)
def update_question_pack(
    pack_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID do pacote de perguntas",
                "value": "00000000-0000-0000-0000-000000000001",
            }
        },
    ),
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "name": "Perguntas de Geografia",
            "tags": ["geografia"],
        },
        examples={
            "atualizar": {
                "summary": "Atualizar pacote de perguntas",
                "value": {
                    "name": "Perguntas de Geografia",
                    "tags": ["geografia"],
                },
            }
        },
    ),
):
    response = update_row("question_packs", pack_id, payload)
    if not response:
        raise HTTPException(status_code=404, detail="Question pack not found")
    return {"response": response}


@router.delete("/{pack_id}", status_code=200)
def delete_question_pack(
    pack_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID do pacote de perguntas",
                "value": "00000000-0000-0000-0000-000000000001",
            }
        },
    )
):
    response = delete_row("question_packs", pack_id)
    if not response:
        raise HTTPException(status_code=404, detail="Question pack not found")
    return {"response": None}


@router.post(
    "/{pack_id}/questions",
    response_model=Dict[str, Any],
    status_code=201,
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "response": {
                            "id": 1,
                            "question_pack_id": "00000000-0000-0000-0000-000000000001",
                            "question_id": "00000000-0000-0000-0000-000000000789",
                            "created_at": "2026-06-14T10:00:00Z",
                        }
                    }
                }
            }
        }
    },
)
def add_question_to_pack(
    pack_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID do pacote de perguntas",
                "value": "00000000-0000-0000-0000-000000000001",
            }
        },
    ),
    payload: Dict[str, Any] = Body(
        ...,
        example={
            "question_id": "00000000-0000-0000-0000-000000000789",
        },
        examples={
            "adicionar": {
                "summary": "Adicionar pergunta ao pacote",
                "value": {
                    "question_id": "00000000-0000-0000-0000-000000000789",
                },
            }
        },
    ),
):
    question_id = payload.get("question_id")
    if not question_id:
        raise HTTPException(status_code=400, detail="question_id is required")

    query = sql.SQL("SELECT id FROM {table} WHERE id = %(target_id)s").format(
        table=sql.Identifier("question_packs")
    )
    pack = fetch_one(query, {"target_id": pack_id})
    if not pack:
        raise HTTPException(status_code=404, detail="Question pack not found")

    query = sql.SQL("SELECT id FROM {table} WHERE id = %(target_id)s").format(
        table=sql.Identifier("questions")
    )
    question = fetch_one(query, {"target_id": question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    insertion_payload = {
        "question_pack_id": pack_id,
        "question_id": question_id,
    }
    return {"response": insert_row("question_question_packs", insertion_payload)}


@router.delete(
    "/{pack_id}/questions/{question_id}",
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
def remove_question_from_pack(
    pack_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID do pacote de perguntas",
                "value": "00000000-0000-0000-0000-000000000001",
            }
        },
    ),
    question_id: str = Path(
        ...,
        examples={
            "id": {
                "summary": "ID da pergunta",
                "value": "00000000-0000-0000-0000-000000000789",
            }
        },
    ),
):
    query = sql.SQL(
        "DELETE FROM {table} WHERE question_pack_id = %(pack_id)s AND question_id = %(question_id)s RETURNING *"
    ).format(table=sql.Identifier("question_question_packs"))
    response = fetch_one(
        query, {"pack_id": pack_id, "question_id": question_id}
    )
    if not response:
        raise HTTPException(
            status_code=404,
            detail="Question not found in this pack or pack not found",
        )
    return {"response": None}
