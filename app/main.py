from fastapi import FastAPI
from app.routers import courses, grades, students, grades,categories,assessments
from fastapi.middleware.cors import CORSMiddleware

app  = FastAPI(title="Student Grading system")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    )
app.include_router(assessments.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(grades.router)
app.include_router(categories.router)



@app.get("/")
def root():
    return {"message": "Welcome"}