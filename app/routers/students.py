# app/routers/students.py
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(prefix="/api/students", tags=["Students"])

_COLUMNS = "id, student_number, first_name, last_name, email, created_at"


class StudentCreate(BaseModel):
    studentNumber: str = Field(min_length=1)
    firstName: str = Field(min_length=1)
    lastName: str = Field(min_length=1)
    email: str = Field(min_length=3)


def _to_json(row) -> dict:
    # camelCase keys to match the shared API contract
    return {
        "id": row[0],
        "studentNumber": row[1],
        "firstName": row[2],
        "lastName": row[3],
        "email": row[4],
        "createdAt": row[5],
    }


@router.get("")
def list_students(db: Session = Depends(get_db)):
    rows = db.execute(
        text(f"SELECT {_COLUMNS} FROM students ORDER BY student_number")
    ).fetchall()
    return [_to_json(r) for r in rows]


@router.get("/{student_id}")
def get_student(student_id: UUID, db: Session = Depends(get_db)):
    row = db.execute(
        text(f"SELECT {_COLUMNS} FROM students WHERE id = :sid"),
        {"sid": str(student_id)},
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} was not found.")
    return _to_json(row)


@router.post("", status_code=201)
def create_student(body: StudentCreate, db: Session = Depends(get_db)):
    new_id = str(uuid4())
    try:
        db.execute(
            text(
                "INSERT INTO students (id, student_number, first_name, last_name, email) "
                "VALUES (:id, :num, :first, :last, :email)"
            ),
            {
                "id": new_id,
                "num": body.studentNumber.strip(),
                "first": body.firstName.strip(),
                "last": body.lastName.strip(),
                "email": body.email.strip(),
            },
        )
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A student with that student number or email already exists.",
        )

    row = db.execute(
        text(f"SELECT {_COLUMNS} FROM students WHERE id = :sid"),
        {"sid": new_id},
    ).fetchone()
    return _to_json(row)