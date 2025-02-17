from sqlalchemy import create_engine, text
from alembic.config import Config
from alembic import command
from dotenv import load_dotenv
import os
import getpass

def init_database():
    load_dotenv()
    
    # Configurazione del database
    DB_USER = os.getenv("DB_USER", "openpsa_user")
    DB_PASS = os.getenv("DB_PASSWORD", "123456")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "openpsa")
    
    # Su macOS, usa l'utente corrente come superuser
    current_user = getpass.getuser()
    
    # Connessione come superuser
    admin_engine = create_engine(f"postgresql://{current_user}@localhost/postgres")
    
    with admin_engine.connect() as conn:
        conn.execute(text("COMMIT"))
        
        # Crea l'utente dell'applicazione se non esiste usando parametri bind
        conn.execute(text("""
            DO $$
            DECLARE
                db_user text := :user;
                db_pass text := :pass;
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = db_user) THEN
                    EXECUTE format('CREATE USER %I WITH PASSWORD %L', db_user, db_pass);
                END IF;
            END
            $$;
        """), {"user": DB_USER, "pass": DB_PASS})
        
        # Termina le connessioni esistenti
        conn.execute(text("""
            SELECT pg_terminate_backend(pid) 
            FROM pg_stat_activity 
            WHERE datname = :db_name AND pid != pg_backend_pid()
        """), {"db_name": DB_NAME})
        
        # Ricrea il database
        conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
        conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
        
        # Gestione dei privilegi
        conn.execute(
            text(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER}")
        )
        conn.commit()
    
    # Connessione al nuovo database per le operazioni successive
    app_engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
    
    with app_engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
        conn.commit()
    
    # Applica le migrazioni
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    init_database()