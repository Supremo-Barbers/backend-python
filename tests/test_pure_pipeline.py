# tests/test_pure_pipeline.py
from uuid import uuid4
from app.core.immutable_types import CategoryRecord, ScoreRecord, StudentRecord
from app.core.functional_pipeline import run_grading_pipeline

def test_nu_failing_grade_pipeline():
    student_id = uuid4()
    cat_id = uuid4()
    
    students = (StudentRecord(student_id, "2023-0001", "Maria", "Santos"),)
    categories = (CategoryRecord(cat_id, "Exams", 1.0),)
    # 52 out of 100 -> 52.00% -> Should yield "R" and "Repeat"
    scores = (ScoreRecord(uuid4(), student_id, 52.0, 100.0, cat_id),)

    results = run_grading_pipeline(students, categories, scores)
    
    assert len(results) == 1
    assert results[0].final_raw_percentage == 52.00
    assert results[0].grade_point == "R"
    assert results[0].academic_remark == "Repeat"