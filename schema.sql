PRAGMA foreign_keys = ON;

CREATE TABLE students (
    id TEXT PRIMARY KEY NOT NULL,
    student_number TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE courses (
    id TEXT PRIMARY KEY NOT NULL,
    code TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    term TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE enrollments (
    id TEXT PRIMARY KEY NOT NULL,
    student_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    enrolled_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    CONSTRAINT uq_student_course UNIQUE (student_id, course_id)
);

CREATE TABLE assessment_categories (
    id TEXT PRIMARY KEY NOT NULL,
    course_id TEXT NOT NULL,
    name TEXT NOT NULL,
    weight REAL NOT NULL CHECK (weight > 0.0 AND weight <= 1.0),
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

CREATE TABLE assessments (
    id TEXT PRIMARY KEY NOT NULL,
    category_id TEXT NOT NULL,
    title TEXT NOT NULL,
    max_score REAL NOT NULL CHECK (max_score > 0.0),
    FOREIGN KEY (category_id) REFERENCES assessment_categories(id) ON DELETE CASCADE
);

CREATE TABLE student_scores (
    id TEXT PRIMARY KEY NOT NULL,
    assessment_id TEXT NOT NULL,
    student_id TEXT NOT NULL,
    score_obtained REAL NOT NULL CHECK (score_obtained >= 0.0),
    recorded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    CONSTRAINT uq_assessment_student UNIQUE (assessment_id, student_id)
);

CREATE INDEX idx_enrollments_course ON enrollments(course_id);
CREATE INDEX idx_enrollments_student ON enrollments(student_id);
CREATE INDEX idx_categories_course ON assessment_categories(course_id);
CREATE INDEX idx_assessments_category ON assessments(category_id);
CREATE INDEX idx_scores_student ON student_scores(student_id);
CREATE INDEX idx_scores_assessment ON student_scores(assessment_id);

