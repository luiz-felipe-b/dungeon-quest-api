# Dungeon Quest 2 Backend

Backend simples em FastAPI com conexão direta ao PostgreSQL.

## Requisitos

- Python 3.10+
- `DATABASE_URL`

## Configuração rápida

```powershell
python -m venv .venv
\.venv\Scripts\python -m pip install --upgrade pip
\.venv\Scripts\pip install -r requirements.txt
```

Edite o arquivo `.env` com a sua `DATABASE_URL` do PostgreSQL.

## Rodando

```powershell
\.venv\Scripts\python -m uvicorn app.main:app --reload
```

## Exemplos de requisições

Base URL usada nos exemplos: `http://localhost:8000`.

### Health check

```powershell
curl http://localhost:8000/health
```

### Usuários

```powershell
curl "http://localhost:8000/api/users?limit=20&offset=0"

curl http://localhost:8000/api/users/00000000-0000-0000-0000-000000000123

curl -X POST http://localhost:8000/api/users ^
	-H "Content-Type: application/json" ^
	-d '{"username":"aventureiro123","password":"senha_super_secreta","high_score":0,"active":true}'

curl -X PATCH http://localhost:8000/api/users/00000000-0000-0000-0000-000000000123 ^
	-H "Content-Type: application/json" ^
	-d '{"high_score":4200,"active":true}'

curl -X DELETE http://localhost:8000/api/users/00000000-0000-0000-0000-000000000123
```

### Tags

```powershell
curl "http://localhost:8000/api/tags?limit=20&offset=0"

curl http://localhost:8000/api/tags/00000000-0000-0000-0000-000000000456

curl -X POST http://localhost:8000/api/tags ^
	-H "Content-Type: application/json" ^
	-d '{"label":"historia"}'

curl -X PATCH http://localhost:8000/api/tags/00000000-0000-0000-0000-000000000456 ^
	-H "Content-Type: application/json" ^
	-d '{"label":"geografia"}'

curl -X DELETE http://localhost:8000/api/tags/00000000-0000-0000-0000-000000000456
```

### Perguntas

```powershell
curl "http://localhost:8000/api/questions?limit=20&offset=0"

curl http://localhost:8000/api/questions/00000000-0000-0000-0000-000000000789

curl -X POST http://localhost:8000/api/questions ^
	-H "Content-Type: application/json" ^
	-d '{"prompt":"Qual e a capital do Brasil?","answer_id":"00000000-0000-0000-0000-000000000000","answer_explanation":"Brasilia e a capital do Brasil.","tag_ids":["00000000-0000-0000-0000-000000000001","00000000-0000-0000-0000-000000000002"]}'

curl -X PATCH http://localhost:8000/api/questions/00000000-0000-0000-0000-000000000789 ^
	-H "Content-Type: application/json" ^
	-d '{"prompt":"Qual e a capital da Argentina?","answer_explanation":"Buenos Aires e a capital da Argentina.","tag_ids":["00000000-0000-0000-0000-000000000003"]}'

curl -X DELETE http://localhost:8000/api/questions/00000000-0000-0000-0000-000000000789
```

### Alternativas

```powershell
curl "http://localhost:8000/api/choices?limit=20&offset=0"

curl http://localhost:8000/api/choices/00000000-0000-0000-0000-000000000321

curl -X POST http://localhost:8000/api/choices ^
	-H "Content-Type: application/json" ^
	-d '{"label":"Brasilia","question_id":"00000000-0000-0000-0000-000000000010"}'

curl -X PATCH http://localhost:8000/api/choices/00000000-0000-0000-0000-000000000321 ^
	-H "Content-Type: application/json" ^
	-d '{"label":"Rio de Janeiro"}'

curl -X DELETE http://localhost:8000/api/choices/00000000-0000-0000-0000-000000000321
```

## Testes

```powershell
\.venv\Scripts\python -m pytest
```
