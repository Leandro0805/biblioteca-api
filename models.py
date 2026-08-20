from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import base


# Representa a tabela de livros
class Livro(base):
    __tablename__ = "livros"

    # Identificador único do livro
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Título do livro
    titulo = Column(
        String(50),
        nullable=False
    )

    # Autor do livro
    autor = Column(
        String(50),
        nullable=False
    )

    # Ano em que o livro foi publicado
    ano_publicacao = Column(
        Integer
    )


# Representa a tabela de empréstimos
class Emprestimo(base):
    __tablename__ = "emprestimos"

    # Identificador único do empréstimo
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Identifica o livro que foi emprestado
    livro_id = Column(
        Integer,
        ForeignKey("livros.id")
    )

    # Nome da pessoa que realizou o empréstimo
    nome_leitor = Column(
        String(50),
        nullable=False
    )

    # Data em que o empréstimo foi realizado
    data_emprestimo = Column(
        Integer,
        nullable=False
    )

    # Indica se o livro já foi devolvido
    devolvido = Column(
        Boolean,
        nullable=False
    )