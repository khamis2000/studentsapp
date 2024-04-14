from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel


app = FastAPI()
class Student(BaseModel):
    name: str
    id: int
    age: float
    classes: list[str]=[]

students = {}

@app.get('/students/{student_id}')
def get_student_by_id(student_id: int):
    student = students.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
@app.get('/students')
def get_all_students():
    return students.values()
@app.post('/students')
def add_student(student: Student):
    if student.id in students:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    students[student.id] = student
    return student
@app.put('/students/{student_id}')
def update_student(student_id: int, student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    students[student_id] = student
    return student