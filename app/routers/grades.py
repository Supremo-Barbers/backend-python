# app/routers/grades.py
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.immutable_types import CategoryRecord, ScoreRecord, StudentRecord
from app.core.functional_pipeline import run_grading_pipeline
from app.schemas.response_contracts import CourseGradeSummaryResponse

router = APIRouter(prefix="/api/courses", tags=["Grades"])

@router.get("/{course_id}/grades", response_model=CourseGradeSummaryResponse)
def get_course_grades(course_id: UUID, db: Session = Depends(get_db)):
    # 1. Fetch raw relational rows (I/O Boundary)
    course_row = db.execute(
        "SELECT id, code, title FROM courses WHERE id = :cid", {"cid": str(course_id)}
    ).fetchone()
    
    if not course_row:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} was not found.")

    student_rows = db.execute(
        """
        SELECT s.id, s.student_number, s.first_name, s.last_name 
        FROM students s
        JOIN enrollments e ON s.id = e.student_id
        WHERE e.course_id = :cid
        """,
        {"cid": str(course_id)}
    ).fetchall()

    category_rows = db.execute(
        "SELECT id, name, weight FROM assessment_categories WHERE course_id = :cid",
        {"cid": str(course_id)}
    ).fetchall()

    score_rows = db.execute(
        """
        SELECT sc.assessment_id, sc.student_id, sc.score_obtained, a.max_score, a.category_id
        FROM student_scores sc
        JOIN assessments a ON sc.assessment_id = a.id
        WHERE a.category_id IN (
            SELECT id FROM assessment_categories WHERE course_id = :cid
        )
        """,
        {"cid": str(course_id)}
    ).fetchall()

    # 2. Map database rows into immutable domain records
    students = tuple(
        StudentRecord(
            id=UUID(r[0]), student_number=r[1], first_name=r[2], last_name=r[3]
        ) for r in student_rows
    )
    categories = tuple(
        CategoryRecord(id=UUID(r[0]), name=r[1], weight=float(r[2])) 
        for r in category_rows
    )
    scores = tuple(
        ScoreRecord(
            assessment_id=UUID(r[0]),
            student_id=UUID(r[1]),
            score_obtained=float(r[2]),
            max_score=float(r[3]),
            category_id=UUID(r[4])
        ) for r in score_rows
    )

    # 3. Execute the Pure Functional Pipeline
    reports = run_grading_pipeline(students, categories, scores)

    # 4. Serialize to match the unified API contract
    return {
        "courseId": course_row[0],
        "courseCode": course_row[1],
        "engine": "Python FastAPI (Functional)",
        "gradingSystem": "National University (AY 2019-2020 Scale)",
        "students": [
            {
                "studentId": rep.student_id,
                "studentNumber": rep.student_number,
                "fullName": rep.full_name,
                "categoryBreakdown": [
                    {
                        "categoryId": cb.category_id,
                        "categoryName": cb.category_name,
                        "weight": cb.weight,
                        "pointsEarned": cb.points_earned,
                        "totalPossible": cb.total_possible,
                        "categoryPercentage": cb.category_percentage,
                        "weightedScore": cb.weighted_score,
                    }
                    for cb in rep.category_breakdown
                ],
                "finalRawPercentage": rep.final_raw_percentage,
                "gradePoint": rep.grade_point,
                "academicRemark": rep.academic_remark,
            }
            for rep in reports
        ],
    }

