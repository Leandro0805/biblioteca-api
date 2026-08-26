# Importa as ferramentas necessárias para criar a conexão com o banco
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Importa ferramentas para acessar as variáveis do arquivo .env
import os
from dotenv import load_dotenv


# Carrega as variáveis do arquivo .env 
load_dotenv()

# Define a URL de conexão recuperando do ambiente (ou definindo um fallback se quiser)
DATABASE_URL = os.getenv("DATABASE_URL")

# Cria a conexão com o banco de dados passando a variável
engine = create_engine(DATABASE_URL)

# Cria uma fábrica de sessões para realizar operações no banco
session_local = sessionmaker(bind=engine)

# Cria a classe base usada pelos modelos
base = declarative_base()