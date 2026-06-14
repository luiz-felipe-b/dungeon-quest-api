from typing import Any, Dict, List

from fastapi import APIRouter, Body, HTTPException, Path, Query
from psycopg import sql

from app.api.db import delete_row, fetch_all, fetch_one, insert_row, update_row

router = APIRouter(prefix="/questions", tags=["Perguntas"])


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
                                "id": "00000000-0000-0000-0000-000000000789",
                                "prompt": "Qual e a capital do Brasil?",
                                "answer_id": "00000000-0000-0000-0000-000000000000",
                                "answer_explanation": "Brasilia e a capital do Brasil.",
                                "tag_ids": [
                                    "00000000-0000-0000-0000-000000000001",
                                    "00000000-0000-0000-0000-000000000002",
                                ],
                                "choices": [
                                    {
                                        "id": "00000000-0000-0000-0000-000000000321",
                                        "label": "Brasilia",
                                        "question_id": "00000000-0000-0000-0000-000000000789",
                                    }
                                ],
                            }
                        ]
                    }
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
    questions = fetch_all(query, {"limit": limit, "offset": offset})
    if not questions:
        return questions

    question_ids = [question["id"] for question in questions]
    choices_query = sql.SQL("SELECT * FROM {table} WHERE question = ANY(%(question_ids)s)").format(
        table=sql.Identifier("choices")
    )
    choices = fetch_all(choices_query, {"question_ids": question_ids})
    choices_by_question: Dict[str, List[Dict[str, Any]]] = {}
    for choice in choices:
        choices_by_question.setdefault(choice["question"], []).append(choice)

    for question in questions:
        question["choices"] = choices_by_question.get(question["id"], [])

    return {"response": questions}


@router.get(
    "/{question_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "response": {
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
    return {"response": response}


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
                            "id": "00000000-0000-0000-0000-000000000789",
                            "prompt": "Qual e a capital do Brasil?",
                            "answer_id": "00000000-0000-0000-0000-000000000321",
                            "answer_explanation": "Brasilia e a capital do Brasil.",
                            "tag_ids": [
                                "00000000-0000-0000-0000-000000000001",
                                "00000000-0000-0000-0000-000000000002",
                            ],
                            "choices": [
                                {
                                    "id": "00000000-0000-0000-0000-000000000321",
                                    "label": "Brasilia",
                                    "question": "00000000-0000-0000-0000-000000000789",
                                },
                                {
                                    "id": "00000000-0000-0000-0000-000000000322",
                                    "label": "Rio de Janeiro",
                                    "question": "00000000-0000-0000-0000-000000000789",
                                },
                                {
                                    "id": "00000000-0000-0000-0000-000000000323",
                                    "label": "São Paulo",
                                    "question": "00000000-0000-0000-0000-000000000789",
                                },
                                {
                                    "id": "00000000-0000-0000-0000-000000000324",
                                    "label": "Salvador",
                                    "question": "00000000-0000-0000-0000-000000000789",
                                },
                            ],
                        }
                    }
                }
            }
        }
    },
)
def create_question(
    payload: Dict[str, Any] = Body(
        ...,
        description="Crie uma pergunta com alternativas ou sem. Se as alternativas forem fornecidas no atributo 'choices', o 'answer_id' não é necessário - ele será definido automaticamente pela alternativa marcada como correta. Se nenhuma alternativa for fornecida, 'answer_id' é obrigatório.",
        example={
            "prompt": "Qual e a capital do Brasil?",
            "created_by": "00000000-0000-0000-0000-000000000123",
            "answer_id": "00000000-0000-0000-0000-000000000000",
            "answer_explanation": "Brasilia e a capital do Brasil.",
            "tags": [
                "00000000-0000-0000-0000-000000000001",
                "00000000-0000-0000-0000-000000000002",
            ],
            "choices": [
                {"label": "Brasilia", "correct": True},
                {"label": "Rio de Janeiro"},
                {"label": "São Paulo"},
                {"label": "Salvador"},
            ],
        },
        examples={
            "criar_com_alternativas": {
                "summary": "Criar pergunta com 4 alternativas (uma marcada como correta)",
                "value": {
                    "prompt": "Qual é a capital do Brasil?",
                    "answer_explanation": "Brasília é a capital do Brasil.",
                    "created_by": "00000000-0000-0000-0000-000000000123",
                    "tags": [
                        "00000000-0000-0000-0000-000000000001",
                        "00000000-0000-0000-0000-000000000002"
                    ],
                    "choices": [
                        {"label": "Brasília", "correct": True},
                        {"label": "Rio de Janeiro"},
                        {"label": "São Paulo"},
                        {"label": "Salvador"},
                    ],
                },
            },
            "criar_sem_alternativas": {
                "summary": "Criar pergunta sem alternativas",
                "value": {
                    "prompt": "Qual é a capital da Argentina?",
                    "answer_id": "00000000-0000-0000-0000-000000000999",
                    "created_by": "00000000-0000-0000-0000-000000000123",
                    "answer_explanation": "Buenos Aires é a capital da Argentina.",
                    "tags": [
                        "00000000-0000-0000-0000-000000000003"
                    ],
                },
            }
        },
    )
):

    # Validate created_by
    created_by = payload.get("created_by")
    if not created_by:
        raise HTTPException(
            status_code=400,
            detail="created_by is required"
        )
    
    choices = payload.pop("choices", [])

    # If no choices, just create the question with answer_id
    if not choices:
        return {"response": insert_row("questions", payload)}

    # Validate exactly 4 choices
    if len(choices) != 4:
        raise HTTPException(
            status_code=400,
            detail="Exactly 4 choices are required",
        )

    # Validate at most 1 choice has correct=true
    correct_choices = [c for c in choices if c.get("correct", False)]
    if len(correct_choices) > 1:
        raise HTTPException(
            status_code=400,
            detail="Only one choice can be marked as correct",
        )

    # Create the question
    question = insert_row("questions", payload)

    # Create the 4 choices
    created_choices = []
    correct_choice_id = None
    for choice in choices:
        choice_payload = {
            "label": choice.get("label"),
            "question": question["id"],
            "created_by": created_by,
        }
        created_choice = insert_row("choices", choice_payload)
        created_choices.append(created_choice)

        # Track the correct choice ID
        if choice.get("correct", False):
            correct_choice_id = created_choice["id"]

    # If one choice was marked as correct, update the question's answer_id
    if correct_choice_id:
        update_payload = {"answer": correct_choice_id}
        question = update_row("questions", question["id"], update_payload)

    question["choices"] = created_choices
    return {"response": question}


@router.patch(
    "/{question_id}",
    response_model=Dict[str, Any],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "response": {
                            "id": "00000000-0000-0000-0000-000000000789",
                            "prompt": "Qual e a capital da Argentina?",
                            "answer_id": "00000000-0000-0000-0000-000000000000",
                            "answer_explanation": "Buenos Aires e a capital da Argentina.",
                            "tag_ids": ["00000000-0000-0000-0000-000000000003"],
                        }
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
    return {"response": response}


@router.delete("/{question_id}", status_code=200)
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
    return {"response": None}