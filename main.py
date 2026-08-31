
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas

from database import session_local, engine

# Cria as tabelas do banco de dados caso elas ainda não existam.
models.base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    # Cria uma sessão do banco para cada requisição.
    db = session_local()

    try:
        yield db
    finally:
        # Garante o fechamento da sessão após a requisição.
        db.close()


@app.post(
    "/livros/",
    response_model=schemas.LivroResponse
)
def create_livro(
    book: schemas.LivroCreate,
    db: Session = Depends(get_db)
):
    # Cria uma instância do modelo Livro com os dados recebidos.
    db_book = models.Livro(**book.model_dump())

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


@app.get(
    "/livros/",
    response_model=List[schemas.LivroResponse]
)
def listar_livros(
    db: Session = Depends(get_db)
):
    # Busca todos os livros cadastrados no banco.
    books = db.query(models.Livro).all()

    return books


@app.get(
    "/livros/{livro_id}",
    response_model=schemas.LivroResponse
)
def buscar_livro(
    livro_id: int,
    db: Session = Depends(get_db)
):
    # Busca um livro pelo seu ID.
    book = db.query(models.Livro).filter(
        models.Livro.id == livro_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado"
        )

    return book


@app.patch(
    "/livros/{livro_id}/status",
    response_model=schemas.LivroResponse
)
def alterar_status_livro(
    livro_id: int,
    status_data: schemas.LivroStatusUpdate,
    db: Session = Depends(get_db)
):
    # Busca o livro que terá o status alterado.
    book = db.query(models.Livro).filter(
        models.Livro.id == livro_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado"
        )

    # Verifica se existe um empréstimo ativo para o livro.
    active_loan = db.query(models.Emprestimo).filter(
        models.Emprestimo.livro_id == livro_id,
        models.Emprestimo.devolvido == False
    ).first()

    # Impede que um livro emprestado seja marcado como disponível.
    if status_data.status == "disponivel" and active_loan is not None:
        raise HTTPException(
            status_code=409,
            detail="O livro possui um empréstimo ativo"
        )

    # Atualiza o status do livro.
    book.status = status_data.status

    db.commit()
    db.refresh(book)

    return book


@app.post(
    "/emprestimos/",
    response_model=schemas.ResponseEmprestimo
)
def emprestar_livro(
    loan_data: schemas.CreateEmprestimo,
    db: Session = Depends(get_db)
):
    # Verifica se o livro informado existe.
    book = db.query(models.Livro).filter(
        models.Livro.id == loan_data.livro_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado"
        )

    # Impede empréstimos de livros que não estão disponíveis.
    if book.status != "disponivel":
        raise HTTPException(
            status_code=409,
            detail=f"Livro não está disponível. Status atual: {book.status}"
        )

    # Verifica se já existe um empréstimo ativo para o livro.
    existing_loan = db.query(models.Emprestimo).filter(
        models.Emprestimo.livro_id == loan_data.livro_id,
        models.Emprestimo.devolvido == False
    ).first()

    if existing_loan is not None:
        raise HTTPException(
            status_code=409,
            detail="Livro já está emprestado"
        )

    # Cria o registro do empréstimo.
    db_loan = models.Emprestimo(**loan_data.model_dump())

    # Atualiza o status do livro após o empréstimo.
    book.status = "emprestado"

    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)

    return db_loan


@app.patch(
    "/emprestimos/{emprestimo_id}/devolver",
    response_model=schemas.ResponseEmprestimo
)
def devolver_livro(
    emprestimo_id: int,
    db: Session = Depends(get_db)
):
    # Busca o empréstimo pelo ID.
    loan = db.query(models.Emprestimo).filter(
        models.Emprestimo.id == emprestimo_id
    ).first()

    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Empréstimo não encontrado"
        )

    # Impede que um empréstimo já devolvido seja devolvido novamente.
    if loan.devolvido:
        raise HTTPException(
            status_code=409,
            detail="O livro já foi devolvido"
        )

    # Busca o livro relacionado ao empréstimo.
    book = db.query(models.Livro).filter(
        models.Livro.id == loan.livro_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado"
        )

    # Marca o empréstimo como devolvido e libera o livro.
    loan.devolvido = True
    book.status = "disponivel"

    db.commit()
    db.refresh(loan)

    return loan


@app.get(
    "/emprestimos/",
    response_model=List[schemas.ResponseEmprestimo]
)
def listar_emprestimos(
    db: Session = Depends(get_db)
):
    # Busca todos os empréstimos cadastrados.
    loans = db.query(models.Emprestimo).all()

    return loans
