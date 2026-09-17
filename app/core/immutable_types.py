# app/core/immutable_types.py
from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ScoreRecord:
    assessment_id: UUID
    student_id: UUID
    score_obtained: float
    max_score: float
    category_id: UUID

@dataclass(frozen=True)
class CategoryRecord:
    id: UUID
    name: str
    weight: float

@dataclass(frozen=True)
class StudentRecord:
    id: UUID
    student_number: str
    first_name: str
    last_name: str

@dataclass(frozen=True)
class CategoryBreakdown:
    category_id: UUID
    category_name: str
    weight: float
    points_earned: float
    total_possible: float
    category_percentage: float
    weighted_score: float

@dataclass(frozen=True)
class StudentGradeReport:
    student_id: UUID
    student_number: str
    full_name: str
    category_breakdown: tuple[CategoryBreakdown, ...]
    final_raw_percentage: float
    grade_point: str
    academic_remark: str

