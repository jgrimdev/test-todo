from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import TaskDB  # Importujeme naši definici tabulky

# Tímto příkazem reálně vytvoříme soubor tasks.db a tabulky v něm
# (Pokud už existují, nic se nestane)
Base.metadata.create_all(bind=engine)


class TaskManager:
    def __init__(self):
        # Při startu si otevřeme spojení do databáze
        self.db: Session = SessionLocal()

    def add_task(self, title: str) -> None:
        # 1. Vytvoříme objekt (jako dřív)
        new_task = TaskDB(title=title, completed=False)

        # 2. Přidáme ho do "předsíně" databáze
        self.db.add(new_task)

        # 3. Potvrdíme změnu (Commit) -> Teprve teď se zapíše do souboru
        self.db.commit()

        # 4. Občerstvíme objekt (aby dostal přidělené ID)
        self.db.refresh(new_task)
        print(f"✅ Úkol '{title}' přidán s ID {new_task.id}.")

    def get_tasks(self):
        # SQL: SELECT * FROM tasks;
        return self.db.query(TaskDB).all()

    def mark_task_as_done(self, task_id: int) -> bool:
        # SQL: SELECT * FROM tasks WHERE id = task_id;
        task = self.db.query(TaskDB).filter(TaskDB.id == task_id).first()

        if task:
            task.completed = True
            self.db.commit()  # Uložení změny
            return True
        return False

    # Důležité: Když končíme, zavřeme spojení
    def __del__(self):
        self.db.close()