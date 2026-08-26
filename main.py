from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas

from database import session_local, engine


# Cria as tabelas no banco de dados
models.base.metadata.create_all(bind=engine)

app = FastAPI()


# Cria e encerra a sessão com o banco de dados
def get_db():
    db = session_local()

    try:
        yield db
    finally:
        db.close()


@app.post(
    "/livros/",
    response_model=schemas.LivroResponse
)
def create_livro(
    book: schemas.LivroCreate,
    db: Session = Depends(get_db)
):
    # Converte os dados recebidos em um objeto do modelo Livro
    db_book = models.Livro(**book.model_dump())

    # Adiciona o livro à sessão
    db.add(db_book)

    # Salva as alterações no banco
    db.commit()

    # Atualiza o objeto com os dados gerados pelo banco
    db.refresh(db_book)

    return db_book


@app.get(
    "/livros/",
    response_model=List[schemas.LivroResponse]
)
def listar_livros(
    db: Session = Depends(get_db)
):
    # Consulta todos os livros cadastrados
    books = db.query(models.Livro).all()

    return books