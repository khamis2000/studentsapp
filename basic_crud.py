from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

security = HTTPBasic()

class User(BaseModel):
    username: str
    password: str
    role: str

users_db = {
    "admin": User(username="admin", password="admin", role="admin"),
    "guest": User(username="guest", password="guest", role="guest")
}

def get_user(username: str):
    return users_db.get(username)

# Authenticate user
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user(credentials.username)
    if not user or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user

class Student(BaseModel):
    name: str
    id: int
    age: float
    classes: List[str] = []

# Mock database for students
students = {}

# Add a new student (accessible only for admins)
@app.post('/students', dependencies=[Depends(authenticate_user)])
def add_student(student: Student, user: User = Depends(authenticate_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="User does not have permission to add student")
    if student.id in students:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    students[student.id] = student
    return student

# Get student by class (accessible only for admins)
@app.get('/students/class/{class_name}', dependencies=[Depends(authenticate_user)])
def get_students_by_class(class_name: str, user: User = Depends(authenticate_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="User does not have permission to get students by class")
    class_students = [student for student in students.values() if class_name in student.classes]
    return class_students

# Get all students (accessible for all authenticated users)
@app.get('/students', dependencies=[Depends(authenticate_user)])
def get_all_students(user: User = Depends(authenticate_user)):
    return students.values()

# Get student by ID (accessible for all authenticated users)
@app.get('/students/{student_id}', dependencies=[Depends(authenticate_user)])
def get_student_by_id(student_id: int, user: User = Depends(authenticate_user)):
    student = students.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
