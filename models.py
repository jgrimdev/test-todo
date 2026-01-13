from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# Třída Task dědí od Base -> tím říkáme, že toto je tabulka v DB
class TaskDB(Base):
    __tablename__ = "tasks"  # Název tabulky v SQL

    # Definice sloupců
    id = Column(Integer, primary_key=True, index=True) # Každý úkol má unikátní ID
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)