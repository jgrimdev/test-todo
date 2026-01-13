from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Vytvoříme soubor s databází (bude se jmenovat tasks.db)
DATABASE_URL = "sqlite:///./tasks.db"

# 2. Nastartujeme "motor" (engine)
# connect_args={"check_same_thread": False} je specifikum jen pro SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 3. Vytvoříme továrnu na "Sezení" (Session)
# Session je to, přes co posíláme příkazy do databáze
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Základní třída pro naše modely
Base = declarative_base()