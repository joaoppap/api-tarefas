"""API de Tarefas - FastAPI + SQLite (projeto academico, Azure App Service)."""
import os
import sqlite3
from contextlib import closing
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# No Azure App Service (Linux) apenas /home e persistente.
# WEBSITE_SITE_NAME so existe la; localmente usamos um arquivo na pasta atual.
if os.getenv("WEBSITE_SITE_NAME"):
    DB_PATH = "/home/data/tarefas.db"
else:
    DB_PATH = "tarefas.db"

os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)

app = FastAPI(title="API de Tarefas", version="1.0.0",
              description="API basica (CRUD) com SQLite hospedada no Azure.")


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.on_event("startup")
def criar_tabela():
    with closing(conectar()) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS tarefas (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   titulo TEXT NOT NULL,
                   concluida INTEGER NOT NULL DEFAULT 0,
                   criada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
               )"""
        )
        conn.commit()


class TarefaIn(BaseModel):
    titulo: str
    concluida: Optional[bool] = False


@app.get("/")
def raiz():
    return {"mensagem": "API de Tarefas no ar", "docs": "/docs"}


@app.get("/tarefas")
def listar():
    with closing(conectar()) as conn:
        linhas = conn.execute("SELECT * FROM tarefas ORDER BY id").fetchall()
    return [dict(l) for l in linhas]


@app.get("/tarefas/{tarefa_id}")
def obter(tarefa_id: int):
    with closing(conectar()) as conn:
        l = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
    if not l:
        raise HTTPException(404, "Tarefa nao encontrada")
    return dict(l)


@app.post("/tarefas", status_code=201)
def criar(t: TarefaIn):
    with closing(conectar()) as conn:
        cur = conn.execute("INSERT INTO tarefas (titulo, concluida) VALUES (?, ?)",
                           (t.titulo, int(t.concluida)))
        conn.commit()
        novo = conn.execute("SELECT * FROM tarefas WHERE id = ?", (cur.lastrowid,)).fetchone()
    return dict(novo)


@app.put("/tarefas/{tarefa_id}")
def atualizar(tarefa_id: int, t: TarefaIn):
    with closing(conectar()) as conn:
        cur = conn.execute("UPDATE tarefas SET titulo = ?, concluida = ? WHERE id = ?",
                           (t.titulo, int(t.concluida), tarefa_id))
        conn.commit()
        if cur.rowcount == 0:
            raise HTTPException(404, "Tarefa nao encontrada")
        l = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
    return dict(l)


@app.delete("/tarefas/{tarefa_id}", status_code=204)
def apagar(tarefa_id: int):
    with closing(conectar()) as conn:
        cur = conn.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
        conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(404, "Tarefa nao encontrada")
