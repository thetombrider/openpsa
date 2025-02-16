from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
import os
from typing import Generator

# Configurazione del database da variabili d'ambiente
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "openpsa")

# Creazione URL di connessione
DATABASE_URL = URL.create(
    drivername="postgresql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

# Creazione engine con pool di connessioni
engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # numero massimo di connessioni nel pool
    max_overflow=10,  # connessioni extra temporanee
    pool_timeout=30,  # timeout in secondi per ottenere una connessione
    echo=False  # impostare a True per il debug SQL
)

# Creazione SessionLocal class per gestire le sessioni
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Base class per i modelli
Base = declarative_base()

def get_db() -> Generator:
    """
    Generator di sessioni database.
    Usa questo come dependency injection nei router FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    """
    Inizializza il database creando tutte le tabelle.
    Chiamare questa funzione all'avvio dell'applicazione.
    """
    Base.metadata.create_all(bind=engine)