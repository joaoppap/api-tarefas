# API de Tarefas (FastAPI + SQLite + Azure App Service)

API CRUD simples para o trabalho de Cloud Azure.

## Rodar localmente
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```
Abra http://127.0.0.1:8000/docs

## Endpoints
| Metodo | Rota | Descricao |
|---|---|---|
| GET | /tarefas | Lista tarefas |
| GET | /tarefas/{id} | Busca uma tarefa |
| POST | /tarefas | Cria tarefa |
| PUT | /tarefas/{id} | Atualiza tarefa |
| DELETE | /tarefas/{id} | Remove tarefa |

## Deploy no Azure (App Service Free F1)
Veja os comandos no documento de entrega ou em `deploy.sh`.
