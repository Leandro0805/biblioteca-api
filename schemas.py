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
        # Permite criar o schema a partir dos atributos de um objeto
        from_attributes = True


# Define os dados básicos de um empréstimo
class BaseEmprestimo(BaseModel):
    nome_leitor: str
    data_emprestimo: int
    devolvido: bool


# Define os dados necessários para criar um empréstimo
class CreateEmprestimo(BaseEmprestimo):
    pass


# Define os dados retornados pela API
class ResponseEmprestimo(BaseEmprestimo):
    livro_id: int

    class Config:
        # Permite criar o schema a partir dos atributos de um objeto
        from_attributes = True