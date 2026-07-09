"""
Conexão com o MongoDB (Atlas ou instância própria).
Configure a variável MONGO_URI no arquivo .env desta pasta.
Exemplo de URI do Atlas:
  mongodb+srv://usuario:senha@cluster.xxxxx.mongodb.net/
Exemplo de URI de instância própria (EC2/local):
  mongodb://usuario:senha@SEU_HOST:27017/
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB_NAME", "bancoufs_nosql")


def get_db():
    """Abre a conexão e retorna o objeto do banco de dados."""
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]
