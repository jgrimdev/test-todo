from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from todo import TaskManager  # Importujeme tvou logiku!

# Inicializace aplikace
app = FastAPI()

# Inicializace manažera (načte si data z jsonu)
manager = TaskManager()

# --- DATOVÉ MODELY (Pydantic) ---
# Zatímco v appce jsme měli Dataclass, pro API používáme Pydantic.
# Definuje, co nám má uživatel poslat, když chce vytvořit úkol.
class TaskInput(BaseModel):
    title: str

# --- ENDPOINTY (Cesty) ---

# 1. GET /tasks -> Vrátí seznam úkolů
@app.get("/tasks")
def get_all_tasks():
    return manager.task_list

# 2. POST /tasks -> Přidá nový úkol
@app.post("/tasks")
def create_new_task(new_task: TaskInput):
    # FastAPI automaticky zkontrolovalo, že nám přišel JSON s "title"
    manager.add_task(new_task.title)
    return {"message": "Úkol byl úspěšně přidán", "task": new_task.title}

# 3. GET / -> Jen pro kontrolu, že server běží
@app.get("/")
def home():
    return {"status": "System is running", "version": "2026.1"}


# {task_index} je proměnná část URL
@app.put("/tasks/{task_index}/complete")
def complete_task_endpoint(task_index: int):
    # Zavoláme naši novou čistou metodu
    success = manager.mark_task_as_done(task_index)

    if not success:
        # V API nevracíme print("Chyba"), ale HTTP Status kód 404 (Not Found)
        raise HTTPException(status_code=404, detail="Úkol s tímto indexem neexistuje")

    return {"message": "Úkol byl úspěšně označen jako hotový", "index": task_index}