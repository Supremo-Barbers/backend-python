# app/db/models.py
# Declarative mirror of the DDL in Section 5 of the schema documentation.
# schema.sql stays the source of truth; the routers use raw SQL, so these
# models are for reference and for any future ORM use.
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


# UUIDv4 values are stored as 36-character TEXT strings (application generated)
_NOW = text("CURRENT_TIMESTAMP")


class Student(Base):
    __tablename__ = "students"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    student_number: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=_NOW)


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    code: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    term: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=_NOW)


class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="uq_student_course"),
        Index("idx_enrollments_course", "course_id"),
        Index("idx_enrollments_student", "student_id"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    student_id: Mapped[str] = mapped_column(
        String, ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    course_id: Mapped[str] = mapped_column(
        String, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    enrolled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=_NOW)


class AssessmentCategory(Base):
    __tablename__ = "assessment_categories"
    __table_args__ = (
        CheckConstraint("weight > 0.0 AND weight <= 1.0"),
        Index("idx_categories_course", "course_id"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    course_id: Mapped[str] = mapped_column(
        String, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    # Fraction of the final grade, e.g. 0.30 for 30%
    weight: Mapped[float] = mapped_column(nullable=False)


class Assessment(Base):
    __tablename__ = "assessments"
    __table_args__ = (
        CheckConstraint("max_score > 0.0"),
        Index("idx_assessments_category", "category_id"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    category_id: Mapped[str] = mapped_column(
        String, ForeignKey("assessment_categories.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    max_score: Mapped[float] = mapped_column(nullable=False)


class StudentScore(Base):
    __tablename__ = "student_scores"
    __table_args__ = (
        CheckConstraint("score_obtained >= 0.0"),
        UniqueConstraint("assessment_id", "student_id", name="uq_assessment_student"),
        Index("idx_scores_student", "student_id"),
        Index("idx_scores_assessment", "assessment_id"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    assessment_id: Mapped[str] = mapped_column(
        String, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[str] = mapped_column(
        String, ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    score_obtained: Mapped[float] = mapped_column(nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=_NOW)