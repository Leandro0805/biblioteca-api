
from database import base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date


# Modelo responsável por representar os livros no banco de dados.
class Livro(base):
    __tablename__ = "livros"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    titulo = Column(
        String(50),
        nullable=False
    )

    autor = Column(
        String(50),
        nullable=False
    )

    ano_publicacao = Column(Integer)

    # Armazena o estado atual do livro.
    status = Column(
        String(20),
        nullable=False,
        default="disponivel"
    )


# Modelo responsável por representar os empréstimos no banco de dados.
class Emprestimo(base):
    __tablename__ = "emprestimos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Relaciona o empréstimo ao livro correspondente.
    livro_id = Column(
        Integer,
        ForeignKey('livros.id'),
        nullable=False
    )

    nome_leitor = Column(
        String(50),
        nullable=False
    )

    data_emprestimo = Column(
        Date,
        nullable=False
    )

    # Indica se o livro já foi devolvido.
    devolvido = Column(
        Boolean,
        default=False,
        nullable=False
    )
