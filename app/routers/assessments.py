# app/routers/assessments.py
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(prefix="/api/categories/{category_id}/assessments", tags=["Assessments"])


class AssessmentCreate(BaseModel):
    title: str = Field(min_length=1)
    maxScore: float = Field(gt=0.0)


@router.post("", status_code=201)
def create_assessment(category_id: UUID, body: AssessmentCreate, db: Session = Depends(get_db)):
    exists = db.execute(
        text("SELECT 1 FROM assessment_categories WHERE id = :cid"),
        {"cid": str(category_id)},
    ).fetchone()
    if not exists:
        raise HTTPException(status_code=404, detail=f"Category with id {category_id} was not found.")

    new_id = str(uuid4())
    db.execute(
        text("INSERT INTO assessments (id, category_id, title, max_score) VALUES (:id, :cid, :title, :max)"),
        {"id": new_id, "cid": str(category_id), "title": body.title.strip(), "max": body.maxScore},
    )
    db.commit()

    return {
        "id": new_id,
        "categoryId": str(category_id),
        "title": body.title.strip(),
        "maxScore": body.maxScore,
    }