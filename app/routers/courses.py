# app/routers/courses.py
from uuid import UUID, uuid4
 
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
 
from app.db.database import get_db
 
router = APIRouter(prefix="/api/courses", tags=["Courses"])
 
 
class CourseCreate(BaseModel):
    code: str = Field(min_length=1)
    title: str = Field(min_length=1)
    term: str = Field(min_length=1)
 
 
def _to_json(row) -> dict:
    # camelCase keys to match the shared API contract
    return {
        "id": row[0],
        "code": row[1],
        "title": row[2],
        "term": row[3],
        "createdAt": row[4],
    }
 
 
@router.get("")
def list_courses(db: Session = Depends(get_db)):
    rows = db.execute(
        text("SELECT id, code, title, term, created_at FROM courses ORDER BY code")
    ).fetchall()
    return [_to_json(r) for r in rows]
 
 
@router.get("/{course_id}")
def get_course(course_id: UUID, db: Session = Depends(get_db)):
    row = db.execute(
        text("SELECT id, code, title, term, created_at FROM courses WHERE id = :cid"),
        {"cid": str(course_id)},
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} was not found.")
    return _to_json(row)
 
 
@router.post("", status_code=201)
def create_course(body: CourseCreate, db: Session = Depends(get_db)):
    new_id = str(uuid4())
    try:
        db.execute(
            text("INSERT INTO courses (id, code, title, term) VALUES (:id, :code, :title, :term)"),
            {"id": new_id, "code": body.code.strip(), "title": body.title.strip(), "term": body.term.strip()},
        )
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Course code {body.code} already exists.")
 
    row = db.execute(
        text("SELECT id, code, title, term, created_at FROM courses WHERE id = :cid"),
        {"cid": new_id},
    ).fetchone()
    return _to_json(row)
 