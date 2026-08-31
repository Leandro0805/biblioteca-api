# API de Gerenciamento de Biblioteca

API REST desenvolvida em **Python** para gerenciamento de livros e empréstimos de uma biblioteca.

O projeto utiliza **FastAPI** para construção da API, **SQLAlchemy** para comunicação com o banco de dados e **PostgreSQL** para persistência das informações.

O principal objetivo do projeto foi praticar conceitos de desenvolvimento **Back-End**, incluindo criação de APIs REST, integração com banco de dados relacional, validação de dados, gerenciamento de sessões e tratamento de erros HTTP.

---

## Tecnologias utilizadas

* **Python**
* **FastAPI** — desenvolvimento da API REST
* **SQLAlchemy** — ORM para interação com o banco de dados
* **PostgreSQL** — banco de dados relacional
* **Pydantic** — validação e serialização dos dados
* **python-dotenv** — gerenciamento de variáveis de ambiente
* **Uvicorn** — servidor ASGI para execução da aplicação

---

## Estrutura do projeto

```text
biblioteca-api/
│
├── main.py          # Rotas e lógica principal da API
├── database.py      # Configuração da conexão com o PostgreSQL
├── models.py        # Modelos das tabelas do banco
├── schemas.py       # Schemas Pydantic para validação dos dados
├── .env             # Variáveis de ambiente
├── .gitignore       # Arquivos ignorados pelo Git
└── README.md        # Documentação do projeto
```

---

## Funcionalidades

### Gerenciamento de livros

A API permite:

* Cadastrar livros
* Listar todos os livros
* Buscar um livro pelo ID
* Alterar o status de um livro

Os livros podem possuir os seguintes status:

```text
disponivel
emprestado
danificado
perdido
```

### Gerenciamento de empréstimos

A API também permite:

* Registrar empréstimos
* Listar empréstimos
* Registrar a devolução de um livro
* Impedir que um livro indisponível seja emprestado
* Impedir múltiplos empréstimos ativos para o mesmo livro
* Impedir que um empréstimo já devolvido seja devolvido novamente

---

## Modelagem do banco de dados

O projeto possui duas entidades principais:

### `livros`

| Campo            | Tipo    | Descrição               |
| ---------------- | ------- | ----------------------- |
| `id`             | Integer | Identificador do livro  |
| `titulo`         | String  | Título do livro         |
| `autor`          | String  | Autor                   |
| `ano_publicacao` | Integer | Ano de publicação       |
| `status`         | String  | Situação atual do livro |

### `emprestimos`

| Campo             | Tipo    | Descrição                       |
| ----------------- | ------- | ------------------------------- |
| `id`              | Integer | Identificador do empréstimo     |
| `livro_id`        | Integer | ID do livro emprestado          |
| `nome_leitor`     | String  | Nome do leitor                  |
| `data_emprestimo` | Date    | Data do empréstimo              |
| `devolvido`       | Boolean | Indica se o livro foi devolvido |

A tabela `emprestimos` possui uma **chave estrangeira (`ForeignKey`)** que relaciona cada empréstimo a um livro.

---

## Endpoints

### Livros

| Método  | Endpoint                    | Descrição                   |
| ------- | --------------------------- | --------------------------- |
| `POST`  | `/livros/`                  | Cadastra um novo livro      |
| `GET`   | `/livros/`                  | Lista todos os livros       |
| `GET`   | `/livros/{livro_id}`        | Busca um livro pelo ID      |
| `PATCH` | `/livros/{livro_id}/status` | Altera o status de um livro |

### Empréstimos

| Método  | Endpoint                                | Descrição                  |
| ------- | --------------------------------------- | -------------------------- |
| `POST`  | `/emprestimos/`                         | Registra um empréstimo     |
| `GET`   | `/emprestimos/`                         | Lista todos os empréstimos |
| `PATCH` | `/emprestimos/{emprestimo_id}/devolver` | Registra a devolução       |

---

## Regras de negócio

O projeto possui algumas regras para garantir a consistência dos dados.

### Empréstimos

Um livro só pode ser emprestado quando estiver com status:

```text
disponivel
```

Caso contrário, a API retorna:

```http
409 Conflict
```

Também é verificado se já existe um empréstimo ativo para o livro.

### Devolução

Ao devolver um livro:

1. O empréstimo é marcado como `devolvido = True`;
2. O status do livro é alterado para `disponivel`.

A API também impede que um empréstimo já devolvido seja devolvido novamente.

### Alteração de status

Um livro que possui um empréstimo ativo não pode ser alterado para:

```text
disponivel
```

Isso evita inconsistências entre o status do livro e os registros de empréstimos.

---

## Variáveis de ambiente

As informações de conexão com o banco de dados são armazenadas em variáveis de ambiente utilizando o arquivo `.env`.

Exemplo:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/biblioteca
```

> O arquivo `.env` não deve ser enviado para o GitHub. Adicione-o ao `.gitignore` para evitar a exposição de credenciais.

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

Entre na pasta:

```bash
cd seu-repositorio
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

No Windows:

```powershell
venv\Scripts\activate
```

### 4. Instale as dependências

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```

### 5. Configure o PostgreSQL

Crie um banco de dados chamado:

```text
biblioteca
```

Depois, configure a variável `DATABASE_URL` no arquivo `.env`:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/biblioteca
```

Substitua `usuario` e `senha` pelas suas credenciais do PostgreSQL.

---

## Executando a aplicação

Com o ambiente virtual ativado, execute:

```bash
python -m uvicorn main:app --reload
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

---

## Documentação da API

O FastAPI gera automaticamente uma documentação interativa.

### Swagger UI

Acesse:

```text
http://127.0.0.1:8000/docs
```

### ReDoc

Também é possível acessar:

```text
http://127.0.0.1:8000/redoc
```

Através do Swagger UI, é possível visualizar os endpoints e realizar requisições diretamente pelo navegador.

---

## Exemplos de utilização

### Cadastrar um livro

`POST /livros/`

```json
{
    "titulo": "Dom Casmurro",
    "autor": "Machado de Assis",
    "ano_publicacao": 1899
}
```

### Registrar um empréstimo

`POST /emprestimos/`

```json
{
    "nome_leitor": "João",
    "devolvido": false,
    "data_emprestimo": "2026-08-31",
    "livro_id": 1
}
```

### Alterar o status de um livro

`PATCH /livros/1/status`

```json
{
    "status": "danificado"
}
```

### Registrar uma devolução

`PATCH /emprestimos/1/devolver`

Não é necessário enviar um corpo na requisição.

---

## Objetivos de aprendizado

Este projeto foi desenvolvido com o objetivo de praticar conceitos importantes de desenvolvimento Back-End, como:

* Criação de APIs REST;
* Desenvolvimento de endpoints com FastAPI;
* Utilização de métodos HTTP (`GET`, `POST` e `PATCH`);
* Integração entre Python e PostgreSQL;
* Utilização de ORM com SQLAlchemy;
* Modelagem de dados relacionais;
* Utilização de chaves estrangeiras;
* Validação de dados com Pydantic;
* Gerenciamento de sessões do banco de dados;
* Utilização de variáveis de ambiente;
* Tratamento de exceções com `HTTPException`;
* Implementação de regras de negócio;
* Documentação automática de APIs.

---

## Possíveis melhorias futuras

Algumas funcionalidades que podem ser adicionadas em versões futuras:

* [ ] Autenticação e autorização de usuários;
* [ ] Sistema de usuários e leitores;
* [ ] Endpoint para atualizar informações dos livros;
* [ ] Exclusão de livros;
* [ ] Histórico completo de empréstimos;
* [ ] Paginação na listagem de livros;
* [ ] Filtros por título, autor e status;
* [ ] Relacionamentos ORM entre `Livro` e `Emprestimo`;
* [ ] Testes automatizados com `pytest`;
* [ ] Migrações de banco de dados utilizando Alembic;
* [ ] Dockerização da aplicação;
* [ ] Deploy da API em um ambiente de produção.

---

## Sobre o projeto

Projeto desenvolvido como parte do meu processo de aprendizado em **desenvolvimento Back-End com Python**, com foco na construção de APIs e integração com bancos de dados relacionais.

O projeto representa uma aplicação prática dos conhecimentos adquiridos em **Python, SQL, PostgreSQL, FastAPI e SQLAlchemy**.
