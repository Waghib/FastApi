from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

tasks = []

@app.post("/tasks/", response_model=Task)
async def create_tasks(task: Task):
    task.id = uuid4()
    tasks.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: UUID, task: Task):
    for t in tasks:
        if t.id == task_id:
            t.title = task.title
            t.description = task.description
            t.completed = task.completed
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)