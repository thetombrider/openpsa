# src/main.py
import uvicorn
from src.api.api import app  # import relativo
from src.database.database import init_db  # import relativo

def main():
    # Inizializza il database
    init_db()
    
    # Avvia il server
    uvicorn.run(
        app,  # percorso relativo al modulo
        host="0.0.0.0",
        port=8000,
        reload=True  # abilita hot reload in development
    )

if __name__ == "__main__":
    main()