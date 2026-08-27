from database import base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date

# Certifique-se de importar os tipos necessários

class Livro(base):
    __tablename__ = "livros"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True  # Significa que dentro da tabela, essa coluna terá um índice
    ) 
    titulo = Column(
        String(50), 
        nullable=False  # O que recebeu isso não pode ser nulo
    )
    autor = Column(String(50), nullable=False) 
    ano_publicacao = Column(Date) 


class Emprestimo(base): 
    __tablename__ = "emprestimos" # Adicionado por boas práticas

    id = Column(Integer, primary_key=True, index=True) 
    livro_id = Column(Integer, ForeignKey('livros.id'),nullable=False) # Geralmente usa-se o nome da tabela em minúsculo ('livros.id')
    nome_leitor = Column(String(50), nullable=False) 
    data_emprestimo = Column(Date, nullable=False) # Nota: Se for data, o ideal costuma ser Date ou DateTime, mas mantive Integer conforme o seu
    devolvido = Column(Boolean, default=False, nullable=False) # Corrigido de Bool=True para Boolean, default=True