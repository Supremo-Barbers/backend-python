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


# 1. Standalone lambda
square = lambda x: x ** 2
print(square(5))  
 # 25

# 2. Lambda as a sort key
students = [("Ana", 88), ("Ben", 95), ("Cid", 72)]
print(sorted(students, key=lambda s: s[1], reverse=True))
# [('Ben', 95), ('Ana', 88), ('Cid', 72)]

# 3. Lambda with map() and filter()
numbers = [1, 2, 3, 4, 5, 6]
print(list(map(lambda n: n ** 2, numbers)))        
# [1, 4, 9, 16, 25, 36]
print(list(filter(lambda n: n % 2 == 0, numbers)))  
# [2, 4, 6]
