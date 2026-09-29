# app/schemas/response_contracts.py
from pydantic import BaseModel
from uuid import UUID


class CategoryBreakdownResponse(BaseModel):
    categoryId: UUID
    categoryName: str
    weight: float
    pointsEarned: float
    totalPossible: float
    categoryPercentage: float
    weightedScore: float


class StudentGradeResponse(BaseModel):
    studentId: UUID
    studentNumber: str
    fullName: str
    categoryBreakdown: list[CategoryBreakdownResponse]
    finalRawPercentage: float
    gradePoint: str
    academicRemark: str


class CourseGradeSummaryResponse(BaseModel):
    courseId: UUID
    courseCode: str
    engine: str
    gradingSystem: str
    students: list[StudentGradeResponse]