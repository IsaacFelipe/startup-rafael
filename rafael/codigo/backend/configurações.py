# configurações.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Carrega .env automaticamente
basedir = Path(__file__).resolve().parent
env_path = basedir.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-dev-fallback'
    # Garante que use o MySQL definido no .env ou fallback para SQLite local
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + str(basedir / 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False