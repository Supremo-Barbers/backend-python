from fastapi import FastAPI
from app.routers import courses, grades, students, grades 

app  = FastAPI(title="Student Grading system")

#app.include_router(courses.router)
app.include_router(grades.router)
#app.include_router(students.router)

@app.get("/")
def root():
    return {"message": "Welcome"}