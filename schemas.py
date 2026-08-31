
from pydantic import BaseModel
from datetime import date
from typing import Literal


# Campos básicos utilizados na criação e resposta de um livro.
class LivroBase(BaseModel):
    titulo: str
    autor: str


# Schema utilizado para cadastrar um novo livro.
class LivroCreate(LivroBase):
    ano_publicacao: int


# Schema utilizado nas respostas da API.
class LivroResponse(LivroBase):
    id: int
    ano_publicacao: int
    status: str

    class Config:
        # Permite criar o schema a partir de objetos do SQLAlchemy.
        from_attributes = True


# Define os valores permitidos para o status de um livro.
class LivroStatusUpdate(BaseModel):
    status: Literal[
        "disponivel",
        "emprestado",
        "danificado",
        "perdido"
    ]


# Campos básicos utilizados nos empréstimos.
class BaseEmprestimo(BaseModel):
    nome_leitor: str
    devolvido: bool


# Schema utilizado para criar um novo empréstimo.
class CreateEmprestimo(BaseEmprestimo):
    data_emprestimo: date
    livro_id: int


# Schema utilizado nas respostas relacionadas aos empréstimos.
class ResponseEmprestimo(BaseEmprestimo):
    livro_id: int

    class Config:
        # Permite criar o schema a partir de objetos do SQLAlchemy.
        from_attributes = True
