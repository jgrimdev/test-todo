from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from todo import TaskManager

app = FastAPI()
manager = TaskManager()


class TaskInput(BaseModel):
    title: str


@app.get("/tasks")
def get_all_tasks():
    # Voláme novou metodu get_tasks
    return manager.get_tasks()


@app.post("/tasks")
def create_new_task(new_task: TaskInput):
    manager.add_task(new_task.title)
    return {"message": "Úkol přidán"}


# Změna: už ne task_index, ale task_id
@app.put("/tasks/{task_id}/complete")
def complete_task_endpoint(task_id: int):
    success = manager.mark_task_as_done(task_id)

    if not success:
        raise HTTPException(status_code=404, detail="Úkol s tímto ID neexistuje")

    return {"message": "Hotovo", "id": task_id}