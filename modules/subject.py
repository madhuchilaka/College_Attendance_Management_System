# modules/subject.py

from database.database_manager import (
    load_subjects,
    save_subjects,
    load_faculty
)

from database.database_manager import (
    load_assignments,
    load_attendance
)

from utils.helpers import (
    YEARS,
    SEMESTERS,
    DEPARTMENTS,
    select_option,
    select_subject,
    select_faculty
)

from utils.id_generator import generate_subject_id

from utils.logger import log_activity
from utils.validators import (
    validate_name,
    validate_subject_code,
    validate_credits,
    subject_code_exists

)

# ===================================
# Add Subject
# ===================================

def add_subject():

    subjects = load_subjects()
    faculty = load_faculty()

    print("\n========== ADD SUBJECT ==========\n")

    subject_id = generate_subject_id()

    print(f"\nSubject ID : {subject_id} (Auto Generated)")

    if subject_id in subjects:
        print("\nSubject ID already exists.")
        return

    while True:

        subject_code = input("Enter Subject Code : ").strip().upper()

        if not validate_subject_code(subject_code):

            print("❌ Invalid Subject Code.")
            continue

        if subject_code_exists(subject_code, subjects):

            print("❌ Subject Code Already Exists.")
            continue

        break
    while True:

        subject_name = input("Enter Subject Name : ").strip()

        if validate_name(subject_name):

            break

        print("❌ Invalid Subject Name.")

    year = select_option(YEARS, "Select Academic Year")
    semester = select_option(SEMESTERS, "Select Semester")
    department = select_option(DEPARTMENTS, "Select Department")

    if faculty:

        print("\nAssign Faculty")
        faculty_id, faculty_details = select_faculty(faculty)

    else:

        faculty_id = ""
        print("\nNo Faculty Available. Subject saved without faculty.")

    while True:

        credits = input("Enter Credits : ").strip()

        if validate_credits(credits):

            credits = int(credits)

            break

        print("❌ Credits must be between 1 and 6.")

    subjects[subject_id] = {

        "subject_code": subject_code,
        "subject_name": subject_name,
        "year": year,
        "semester": semester,
        "department": department,
        "faculty_id": faculty_id,
        "credits": credits

    }

    try:
        save_subjects(subjects)
        log_activity(f"Subject Added : {subject_code}")
        print("\n✅ Subject Added Successfully.")
    except Exception as e:
        print("❌ Error Saving Subject")
        print(e)
        return

    
    


# ===================================
# View Subjects
# ===================================

def view_subjects():

    subjects = load_subjects()

    if not subjects:

        print("\nNo Subjects Found.")
        return

    print("\n" + "=" * 120)

    print(
        f"{'ID':<10}"
        f"{'Code':<10}"
        f"{'Subject':<30}"
        f"{'Year':<8}"
        f"{'Sem':<8}"
        f"{'Dept':<15}"
        f"{'Faculty':<12}"
        f"{'Credits'}"
    )

    print("=" * 120)

    for subject_id, details in subjects.items():

        print(
            f"{subject_id:<10}"
            f"{details['subject_code']:<10}"
            f"{details['subject_name']:<30}"
            f"{details['year']:<8}"
            f"{details['semester']:<8}"
            f"{details['department']:<15}"
            f"{details['faculty_id']:<12}"
            f"{details['credits']}"
        )

    print("=" * 120)


# ===================================
# Search Subject
# ===================================

def search_subject():

    subjects = load_subjects()

    if not subjects:

        print("\nNo Subjects Found.")
        return

    subject_id, details = select_subject(subjects)

    print("\n========== SUBJECT DETAILS ==========")

    print(f"Subject ID    : {subject_id}")
    print(f"Subject Code  : {details['subject_code']}")
    print(f"Subject Name  : {details['subject_name']}")
    print(f"Year          : {details['year']}")
    print(f"Semester      : {details['semester']}")
    print(f"Department    : {details['department']}")
    print(f"Faculty ID    : {details['faculty_id']}")
    print(f"Credits       : {details['credits']}")


# ===================================
# Update Subject
# ===================================

def update_subject():

    subjects = load_subjects()

    if not subjects:

        print("\nNo Subjects Found.")
        return

    faculty = load_faculty()

    subject_id, details = select_subject(subjects)

    print("\n========== UPDATE SUBJECT ==========")

    code = input(f"Subject Code ({details['subject_code']}) : ").strip().upper()

    if code:
        details["subject_code"] = code

    name = input(f"Subject Name ({details['subject_name']}) : ").strip().title()

    if name:
        details["subject_name"] = name


    
    year = select_option(
        YEARS,
        "Academic Year",
        allow_skip=True
    )

    if year != "Keep Current":
        details["year"] = year

    semester = select_option(
        SEMESTERS,
        "Semester",
        allow_skip=True
    )

    if semester != "Keep Current":
        details["semester"] = semester

    department = select_option(
        DEPARTMENTS,
        "Department",
        allow_skip=True
    )

    if department != "Keep Current":
        details["department"] = department

    if faculty:

        print("\nAssign Faculty")

        faculty_id, faculty_details = select_faculty(faculty)

        details["faculty_id"] = faculty_id

    credits = input(f"Credits ({details['credits']}) : ")

    if credits:
        details["credits"] = int(credits)

    subjects[subject_id] = details

    try:
        save_subjects(subjects)
        log_activity(f"Subject Updated : {subject_id}")
        print("\n✅ Subject Updated Successfully.")
        
    except Exception as e:
        print("❌ Error Saving Subject")
        print(e)
        return

    

# ===================================
# Delete Subject
# ===================================

def delete_subject():

    subjects = load_subjects()

    if not subjects:

        print("\nNo Subjects Found.")
        return

    subject_id, details = select_subject(subjects)

    confirm = input(
        f"\nDelete {details['subject_name']} ? (Y/N): "
    ).upper()

    if confirm == "Y":

        assignments = load_assignments()

        for assignment in assignments.values():

            if assignment.get("subject_code") == subject["subject_code"]:

                print("\n❌ Cannot Delete Subject.")
                print("Subject is assigned to a faculty.")

                return

        attendance = load_attendance()

        for record in attendance.values():

            if record.get("subject_code") == subject["subject_code"]:

                print("\n❌ Cannot Delete Subject.")
                print("Attendance records exist for this subject.")

                return

        del subjects[subject_id]

        try:
            save_subjects(subjects)
            log_activity(f"Subject Deleted : {subject_id}")
            print("\n✅ Subject Deleted Successfully.")
        except Exception as e:
            print("❌ Error Saving Subject")
            print(e)
            return

        

    else:

        print("\nDeletion Cancelled.")