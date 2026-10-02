# app/routers/categories.py
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(prefix="/api/courses/{course_id}/categories", tags=["Categories"])

_COLUMNS = "id, course_id, name, weight"


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1)
    # Fraction of the final grade, e.g. 0.30 for 30%
    weight: float = Field(gt=0.0, le=1.0)


def _to_json(row) -> dict:
    # camelCase keys to match the shared API contract
    return {
        "id": row[0],
        "courseId": row[1],
        "name": row[2],
        "weight": float(row[3]),
    }


def _require_course(db: Session, course_id: UUID) -> None:
    exists = db.execute(
        text("SELECT 1 FROM courses WHERE id = :cid"), {"cid": str(course_id)}
    ).fetchone()
    if not exists:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} was not found.")


@router.get("")
def list_categories(course_id: UUID, db: Session = Depends(get_db)):
    _require_course(db, course_id)
    rows = db.execute(
        text(f"SELECT {_COLUMNS} FROM assessment_categories WHERE course_id = :cid ORDER BY name"),
        {"cid": str(course_id)},
    ).fetchall()
    return [_to_json(r) for r in rows]


@router.post("", status_code=201)
def create_category(course_id: UUID, body: CategoryCreate, db: Session = Depends(get_db)):
    _require_course(db, course_id)

    current_total = db.execute(
        text("SELECT COALESCE(SUM(weight), 0.0) FROM assessment_categories WHERE course_id = :cid"),
        {"cid": str(course_id)},
    ).scalar()

    # Weights across a course may never exceed 1.0 (100%)
    if round(float(current_total) + body.weight, 6) > 1.0:
        raise HTTPException(
            status_code=400,
            detail=f"Category weights would exceed 100%. Remaining weight: {round(1.0 - float(current_total), 4)}.",
        )

    new_id = str(uuid4())
    db.execute(
        text("INSERT INTO assessment_categories (id, course_id, name, weight) VALUES (:id, :cid, :name, :weight)"),
        {"id": new_id, "cid": str(course_id), "name": body.name.strip(), "weight": body.weight},
    )
    db.commit()

    row = db.execute(
        text(f"SELECT {_COLUMNS} FROM assessment_categories WHERE id = :id"),
        {"id": new_id},
    ).fetchone()
    return _to_json(row)