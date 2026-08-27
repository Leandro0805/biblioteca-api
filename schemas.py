from pydantic import BaseModel


# Define os dados básicos de um livro
class LivroBase(BaseModel):
    titulo: str
    autor: str


# Define os dados necessários para criar um livro
class LivroCreate(LivroBase):
    ano_publicacao: int


# Define os dados retornados pela API
class LivroResponse(LivroBase):
    id: int

    class Config:
        # Permite criar o schema a partir dos atributos do objeto
        from_attributes = True


# Define os dados básicos de um empréstimo
class BaseEmprestimo(BaseModel):
    nome_leitor: str
    devolvido: bool


# Define os dados necessários para criar um empréstimo
class CreateEmprestimo(BaseEmprestimo):
    data_emprestimo: int
    livro_id: int


# Define os dados retornados pela API
class ResponseEmprestimo(BaseEmprestimo):
    livro_id: int

    class Config:
        # Permite criar o schema a partir dos atributos do objeto
        from_attributes = True