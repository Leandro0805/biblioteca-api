from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas

from database import session_local, engine


# Cria as tabelas no banco de dados
models.base.metadata.create_all(bind=engine)

app = FastAPI()


# Cria uma sessão com o banco de dados
def get_db():
    db = session_local()

    try:
        yield db
    finally:
        # Fecha a sessão após o uso
        db.close()


# Cadastra um novo livro
@app.post(
    "/livros/",
    response_model=schemas.LivroResponse
)
def create_livro(
    book: schemas.LivroCreate,
    db: Session = Depends(get_db)
):
    # Converte os dados recebidos em um objeto Livro
    db_book = models.Livro(**book.model_dump())

    # Adiciona o livro à sessão
    db.add(db_book)

    # Salva o livro no banco de dados
    db.commit()

    # Atualiza o objeto com os dados gerados pelo banco
    db.refresh(db_book)

    return db_book


# Lista todos os livros cadastrados
@app.get(
    "/livros/",
    response_model=List[schemas.LivroResponse]
)
def listar_livros(
    db: Session = Depends(get_db)
):
    # Consulta todos os livros
    books = db.query(models.Livro).all()

    if not books:
        raise HTTPException(
            status_code=404,
            detail="Nenhum livro encontrado"
        )

    return books


# Busca um livro pelo ID
@app.get(
    "/livros/{livro_id}",
    response_model=schemas.LivroResponse
)
def buscar_livro(
    livro_id: int,
    db: Session = Depends(get_db)
):
    # Busca o livro pelo ID informado
    book = db.query(models.Livro).filter(
        models.Livro.id == livro_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado"
        )

    return book


# Registra um novo empréstimo
@app.post(
    "/emprestimo",
    response_model=schemas.ResponseEmprestimo
)
def emprestar_livro(
    book: schemas.CreateEmprestimo,
    db: Session = Depends(get_db)
):
    # Converte os dados recebidos em um objeto Emprestimo
    db_loan = models.Emprestimo(**book.model_dump())

    # Adiciona o empréstimo à sessão
    db.add(db_loan)

    # Salva o empréstimo no banco de dados
    db.commit()

    # Atualiza o objeto com os dados gerados pelo banco
    db.refresh(db_loan)

    return db_loan


# Lista todos os empréstimos cadastrados
@app.get(
    "/emprestimo",
    response_model=List[schemas.ResponseEmprestimo]
)
def listar_emprestimos(
    db: Session = Depends(get_db)
):
    # Consulta todos os empréstimos
    loans = db.query(models.Emprestimo).all()

    if not loans:
        raise HTTPException(
            status_code=404,
            detail="Nenhum empréstimo encontrado"
        )

    return loans