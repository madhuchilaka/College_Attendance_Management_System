# ==========================================
# utils/validator.py
# ==========================================

import re


# ==========================================
# Name Validation
# ==========================================

def validate_name(name):

    name = name.strip()

    if len(name) < 2:
        return False

    return all(char.isalpha() or char.isspace() for char in name)


# ==========================================
# Email Validation
# ==========================================

def validate_email(email):

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    return bool(re.match(pattern, email))


# ==========================================
# Phone Number Validation
# ==========================================

def validate_phone(phone):

    return phone.isdigit() and len(phone) == 10


# ==========================================
# Subject Code Validation
# ==========================================

def validate_subject_code(subject_code):

    subject_code = subject_code.strip().upper()

    pattern = r"^[A-Z0-9]{2,10}$"

    return bool(re.match(pattern, subject_code))


# ==========================================
# Credits Validation
# ==========================================

def validate_credits(credits):

    try:

        credits = int(credits)

        return 1 <= credits <= 6

    except ValueError:

        return False


# ==========================================
# Password Validation
# ==========================================

def validate_password(password):

    return len(password) >= 6


# ==========================================
# Duplicate Email Check
# ==========================================

def email_exists(email, data):

    email = email.lower()

    for details in data.values():

        if details.get("email", "").lower() == email:

            return True

    return False


# ==========================================
# Duplicate Phone Check
# ==========================================

def phone_exists(phone, data):

    for details in data.values():

        if details.get("phone") == phone:

            return True

    return False


# ==========================================
# Duplicate Subject Code Check
# ==========================================

def subject_code_exists(subject_code, subjects):

    subject_code = subject_code.upper()

    for subject in subjects.values():

        if subject.get("subject_code", "").upper() == subject_code:

            return True

    return False


# ==========================================
# Duplicate Assignment Check
# ==========================================

def assignment_exists(assignments,
                      faculty_id,
                      subject_code,
                      year,
                      department,
                      section):

    for assignment in assignments.values():

        if (

            assignment.get("faculty_id") == faculty_id

            and

            assignment.get("subject_code") == subject_code

            and

            str(assignment.get("year")) == str(year)

            and

            assignment.get("department") == department

            and

            assignment.get("section") == section

        ):

            return True

    return False