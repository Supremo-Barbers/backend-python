# app/core/nu_scale.py
from typing import NamedTuple

class GradeConversion(NamedTuple):
    grade_point: str
    remark: str

def to_nu_grade(raw_percentage: float) -> GradeConversion:
    """Pure mathematical conversion mapping raw percentage to the NU grading scale."""
    rounded_score = round(raw_percentage, 2)
    
    # Declarative pattern matching via threshold tuples
    thresholds: tuple[tuple[float, str, str], ...] = (
        (96.00, "4.0", "Passed"),
        (90.00, "3.5", "Passed"),
        (84.00, "3.0", "Passed"),
        (78.00, "2.5", "Passed"),
        (72.00, "2.0", "Passed"),
        (66.00, "1.5", "Passed"),
        (60.00, "1.0", "Passed"),
    )
    
    for threshold, mark, remark in thresholds:
        if rounded_score >= threshold:
            return GradeConversion(grade_point=mark, remark=remark)
            
    return GradeConversion(grade_point="R", remark="Repeat")

