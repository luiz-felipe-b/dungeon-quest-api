import os
from typing import Any, Dict, List

from dotenv import load_dotenv
import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from fastapi import HTTPException

load_dotenv()


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        raise RuntimeError("DATABASE_URL must be set.")
    return database_url


def get_db_timeouts() -> tuple[int, int]:
    connect_timeout = int(os.getenv("DB_CONNECT_TIMEOUT", "5"))
    statement_timeout_ms = int(os.getenv("DB_STATEMENT_TIMEOUT_MS", "5000"))
    return connect_timeout, statement_timeout_ms


def fetch_all(query: sql.SQL, params: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    try:
        connect_timeout, statement_timeout_ms = get_db_timeouts()
        with psycopg.connect(
            get_database_url(),
            row_factory=dict_row,
            connect_timeout=connect_timeout,
            options=f"-c statement_timeout={statement_timeout_ms}",
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or {})
                return cur.fetchall()
    except psycopg.OperationalError as exc:
        raise HTTPException(status_code=503, detail=f"Database connection error: {exc}")
    except psycopg.Error as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}")


def fetch_one(query: sql.SQL, params: Dict[str, Any] | None = None) -> Dict[str, Any] | None:
    try:
        connect_timeout, statement_timeout_ms = get_db_timeouts()
        with psycopg.connect(
            get_database_url(),
            row_factory=dict_row,
            connect_timeout=connect_timeout,
            options=f"-c statement_timeout={statement_timeout_ms}",
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or {})
                return cur.fetchone()
    except psycopg.OperationalError as exc:
        raise HTTPException(status_code=503, detail=f"Database connection error: {exc}")
    except psycopg.Error as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}")


def insert_row(table: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if not payload:
        raise HTTPException(status_code=400, detail="Payload cannot be empty")
    query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({values}) RETURNING *").format(
        table=sql.Identifier(table),
        fields=sql.SQL(", ").join(sql.Identifier(key) for key in payload.keys()),
        values=sql.SQL(", ").join(sql.Placeholder(key) for key in payload.keys()),
    )
    result = fetch_one(query, payload)
    if not result:
        raise HTTPException(status_code=500, detail="Insert failed")
    return result


def update_row(table: str, row_id: str, payload: Dict[str, Any]) -> Dict[str, Any] | None:
    if not payload:
        raise HTTPException(status_code=400, detail="No fields to update")
    assignments = [
        sql.SQL("{field} = {value}").format(
            field=sql.Identifier(key),
            value=sql.Placeholder(key),
        )
        for key in payload.keys()
    ]
    query = sql.SQL("UPDATE {table} SET {assignments} WHERE id = %(target_id)s RETURNING *").format(
        table=sql.Identifier(table),
        assignments=sql.SQL(", ").join(assignments),
    )
    params = {**payload, "target_id": row_id}
    return fetch_one(query, params)


def delete_row(table: str, row_id: str) -> Dict[str, Any] | None:
    query = sql.SQL("DELETE FROM {table} WHERE id = %(target_id)s RETURNING *").format(
        table=sql.Identifier(table),
    )
    return fetch_one(query, {"target_id": row_id})