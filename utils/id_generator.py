# ==========================================
# utils/id_generator.py
# ==========================================

from database.database_manager import (
    load_students,
    load_faculty,
    load_subjects,
    load_assignments,
    load_attendance
)


# ==========================================
# Student ID
# ==========================================

def generate_student_id():

    students = load_students()

    return f"STU{len(students)+1:03}"


# ==========================================
# Faculty ID
# ==========================================

def generate_faculty_id():

    faculty = load_faculty()

    return f"FAC{len(faculty)+1:03}"


# ==========================================
# Subject ID
# ==========================================

def generate_subject_id():

    subjects = load_subjects()

    return f"SUB{len(subjects)+1:03}"


# ==========================================
# Assignment ID
# ==========================================

def generate_assignment_id():

    assignments = load_assignments()

    return f"ASN{len(assignments)+1:03}"


# ==========================================
# Attendance ID
# ==========================================

def generate_attendance_id():

    attendance = load_attendance()

    return f"ATT{len(attendance)+1:04}"