# app/core/functional_pipeline.py
from functools import reduce
from typing import Callable, Iterable
from uuid import UUID
from app.core.immutable_types import (
    CategoryBreakdown,
    CategoryRecord,
    ScoreRecord,
    StudentGradeReport,
    StudentRecord,
)
from app.core.nu_scale import to_nu_grade

def calculate_category_breakdown(
    category: CategoryRecord, 
    scores: Iterable[ScoreRecord]
) -> CategoryBreakdown:
    """Pure transformation computing percentage and weighted contribution using reduce."""
    # Filter scores matching this specific category
    cat_scores = tuple(filter(lambda s: s.category_id == category.id, scores))
    
    total_earned = reduce(lambda acc, s: acc + s.score_obtained, cat_scores, 0.0)
    total_possible = reduce(lambda acc, s: acc + s.max_score, cat_scores, 0.0)
    
    percentage = (total_earned / total_possible * 100.0) if total_possible > 0.0 else 0.0
    weighted = percentage * category.weight
    
    return CategoryBreakdown(
        category_id=category.id,
        category_name=category.name,
        weight=category.weight,
        points_earned=round(total_earned, 2),
        total_possible=round(total_possible, 2),
        category_percentage=round(percentage, 2),
        weighted_score=round(weighted, 2),
    )

def evaluate_student(
    student: StudentRecord,
    categories: tuple[CategoryRecord, ...],
    all_scores: tuple[ScoreRecord, ...]
) -> StudentGradeReport:
    """Higher-order transformation evaluating a single student record without shared state."""
    # Filter scores belonging strictly to this student
    student_scores = tuple(filter(lambda s: s.student_id == student.id, all_scores))
    
    # Map each category to its breakdown using a pure curried partial
    breakdowns: tuple[CategoryBreakdown, ...] = tuple(
        map(lambda cat: calculate_category_breakdown(cat, student_scores), categories)
    )
    
    # Aggregate weighted totals using reduce
    raw_final = reduce(lambda acc, b: acc + b.weighted_score, breakdowns, 0.0)
    final_rounded = round(raw_final, 2)
    nu_result = to_nu_grade(final_rounded)
    
    return StudentGradeReport(
        student_id=student.id,
        student_number=student.student_number,
        full_name=f"{student.first_name} {student.last_name}",
        category_breakdown=breakdowns,
        final_raw_percentage=final_rounded,
        grade_point=nu_result.grade_point,
        academic_remark=nu_result.remark,
    )

def run_grading_pipeline(
    students: tuple[StudentRecord, ...],
    categories: tuple[CategoryRecord, ...],
    scores: tuple[ScoreRecord, ...]
) -> tuple[StudentGradeReport, ...]:
    """Entry point for the functional pipeline: maps students to complete reports."""
    return tuple(map(lambda s: evaluate_student(s, categories, scores), students))

