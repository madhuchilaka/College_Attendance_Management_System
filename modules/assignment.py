# ==========================================
# modules/assignment.py
# ==========================================

from database.database_manager import (
    load_assignments,
    save_assignments,
    load_faculty,
    load_subjects
)

from database.database_manager import load_attendance

from modules import faculty
from utils.helpers import (
    YEARS,
    DEPARTMENTS,
    SECTIONS,
    select_option
)


from utils.id_generator import generate_assignment_id

from utils.logger import log_activity
from utils.validators import assignment_exists

# ==========================================
# Assign Subject
# ==========================================

def assign_subject():

    assignments = load_assignments()

    faculty = load_faculty()

    subjects = load_subjects()

    print("\n========================================")
    print("         ASSIGN SUBJECT")
    print("========================================")

    # -----------------------------
    # Select Faculty
    # -----------------------------

    if not faculty:

        print("\n❌ No Faculty Found.")
        return

    faculty_ids = list(faculty.keys())

    print("\nSelect Faculty")
    print("-" * 30)

    for i, faculty_id in enumerate(faculty_ids, start=1):

        print(f"{i}. {faculty_id} - {faculty[faculty_id]['name']}")

    while True:

        try:

            choice = int(input("\nEnter Choice : "))

            if 1 <= choice <= len(faculty_ids):

                faculty_id = faculty_ids[choice - 1]
                break

        except ValueError:
            pass

        print("❌ Invalid Choice.")

    # -----------------------------
    # Select Subject
    # -----------------------------

    if not subjects:

        print("\n❌ No Subjects Found.")
        return

    subject_codes = list(subjects.keys())

    print("\nSelect Subject")
    print("-" * 30)

    for i, code in enumerate(subject_codes, start=1):

        print(f"{i}. {code} - {subjects[code]['subject_name']}")

    while True:

        try:

            choice = int(input("\nEnter Choice : "))

            if 1 <= choice <= len(subject_codes):

                subject_code = subject_codes[choice - 1]
                break

        except ValueError:
            pass

        print("❌ Invalid Choice.")

    # -----------------------------
    # Academic Details
    # -----------------------------

    year = select_option(
        YEARS,
        "Select Academic Year"
    )

    department = select_option(
        DEPARTMENTS,
        "Select Department"
    )

    section = select_option(
        SECTIONS,
        "Select Section"
    )

    # -----------------------------
    # Assignment ID
    # -----------------------------

    assignment_id = generate_assignment_id()

    if assignment_exists(
        assignments,
        faculty_id,
        subject_code,
        year,
        department,
        section
    ):

        print("\n❌ Assignment Already Exists.")

        return
    

    assignments[assignment_id] = {

        "faculty_id": faculty_id,

        "faculty_name": faculty[faculty_id]["name"],

        "subject_code": subject_code,

        "subject_name": subjects[subject_code]["subject_name"],

        "year": year,

        "department": department,

        "section": section

    }

    try:
        save_assignments(assignments)
        log_activity(f"Assignment Added : {assignment_id}")
        print("\n✅ Assignment Added Successfully.")
    except Exception as e:
        print("❌ Error Saving Assignment")
        print(e)
        return

    
    print(f"\nAssignment ID : {assignment_id}")




# ==========================================
# View Assignments
# ==========================================

def view_assignments():

    assignments = load_assignments()

    if not assignments:

        print("\n❌ No Assignments Found.")
        return

    print("\n" + "=" * 110)

    print(
        f"{'ID':<10}"
        f"{'Faculty':<20}"
        f"{'Subject':<25}"
        f"{'Year':<8}"
        f"{'Department':<20}"
        f"{'Section'}"
    )

    print("=" * 110)

    for assignment_id, details in assignments.items():

        faculty = load_faculty()

        faculty_name = faculty.get(
            details["faculty_id"],
            {}
        ).get(
            "name",
            "Unknown"
        )

        print(
            f"{assignment_id:<10}"
            f"{faculty_name:<20}"
            f"{details.get('subject_name', '-'): <25}"
            f"{details.get('year', '-'): <8}"
            f"{details.get('department', '-'): <20}"
            f"{details.get('section', '-')}"
        )

    print("=" * 110)


# ==========================================
# Search Assignment
# ==========================================

def search_assignment():

    assignments = load_assignments()

    if not assignments:

        print("\n❌ No Assignments Found.")
        return

    assignment_id = input("\nEnter Assignment ID : ").strip().upper()

    if assignment_id not in assignments:

        print("\n❌ Assignment Not Found.")
        return

    details = assignments[assignment_id]

    print("\n" + "=" * 50)
    print("        ASSIGNMENT DETAILS")
    print("=" * 50)

    faculty = load_faculty()

    faculty_name = faculty.get(
        details["faculty_id"],
        {}
    ).get(
        "name",
        "Unknown"
    )

    print(f"Assignment ID : {assignment_id}")
    print(f"Faculty       : {faculty_name}")
    print(f"Faculty ID    : {details['faculty_id']}")
    print(f"Subject       : {details['subject_name']}")
    print(f"Subject Code  : {details['subject_code']}")
    print(f"Year          : {details['year']}")
    print(f"Department    : {details['department']}")
    print(f"Section       : {details['section']}")

    print("=" * 50)


# ==========================================
# Update Assignment
# ==========================================

def update_assignment():

    assignments = load_assignments()

    if not assignments:

        print("\n❌ No Assignments Found.")
        return

    assignment_id = input("\nEnter Assignment ID : ").strip().upper()

    if assignment_id not in assignments:

        print("\n❌ Assignment Not Found.")
        return

    assignment = assignments[assignment_id]

    print("\nCurrent Assignment Details")
    print("-" * 40)

    faculty = load_faculty()

    faculty_name = faculty.get(
        assignment["faculty_id"],
        {}
    ).get(
        "name",
        "Unknown"
    )

    print(f"Faculty      : {faculty_name}")
    print(f"Subject      : {assignment['subject_name']}")
    print(f"Year         : {assignment['year']}")
    print(f"Department   : {assignment['department']}")
    print(f"Section      : {assignment['section']}")

    print("\nLeave blank to keep current value.\n")

    year = input(f"Academic Year ({assignment['year']}) : ").strip()

    department = input(f"Department ({assignment['department']}) : ").strip()

    section = input(f"Section ({assignment['section']}) : ").strip()

    if year:

        assignment["year"] = year

    if department:

        assignment["department"] = department

    if section:

        assignment["section"] = section

    assignments[assignment_id] = assignment

    try:
        save_assignments(assignments)
        log_activity(f"Assignment Updated : {assignment_id}")
        print("\n✅ Assignment Updated Successfully.")
    except Exception as e:
        print("❌ Error Saving Assignment")
        print(e)
        return

    



# ==========================================
# Delete Assignment
# ==========================================

def delete_assignment():

    assignments = load_assignments()

    if not assignments:

        print("\n❌ No Assignments Found.")
        return

    assignment_id = input("\nEnter Assignment ID : ").strip().upper()

    if assignment_id not in assignments:

        print("\n❌ Assignment Not Found.")
        return

    assignment = assignments[assignment_id]

    print("\nAssignment Details")
    print("-" * 40)

    faculty = load_faculty()

    faculty_name = faculty.get(
        assignment["faculty_id"],
        {}
    ).get(
        "name",
        "Unknown"
    )

    print(f"Faculty    : {faculty_name}")
    print(f"Subject    : {assignment['subject_name']}")
    print(f"Year       : {assignment['year']}")
    print(f"Department : {assignment['department']}")
    print(f"Section    : {assignment['section']}")

    confirm = input("\nDelete this assignment? (Y/N): ").strip().upper()

    if confirm == "Y":

        attendance = load_attendance()

        for record in attendance.values():

            if (

                record.get("faculty_id") == assignment["faculty_id"]

                and

                record.get("subject_code") == assignment["subject_code"]

                and

                str(record.get("year")) == str(assignment["year"])

                and

                record.get("department") == assignment["department"]

                and

                record.get("section") == assignment["section"]

            ):

                print("\n❌ Cannot Delete Assignment.")
                print("Attendance records already exist.")

                return

        del assignments[assignment_id]

        try:
            save_assignments(assignments)
            log_activity(f"Assignment Deleted : {assignment_id}")
            print("\n✅ Assignment Deleted Successfully.")
        except Exception as e:
            print("❌ Error Saving Assignment")
            print(e)
            return

         
    else:

        print("\nDeletion Cancelled.")


# ==========================================
# Get Assignments By Faculty
# ==========================================

def get_faculty_assignments(faculty_id):

    assignments = load_assignments()

    faculty_assignments = {}

    for assignment_id, details in assignments.items():

        if details["faculty_id"] == faculty_id:

            faculty_assignments[assignment_id] = details

    return faculty_assignments


# ==========================================
# Select Assigned Class
# ==========================================

def select_assigned_class(faculty_id):

    assignments = get_faculty_assignments(faculty_id)

    if not assignments:

        print("\n❌ No Classes Assigned.")
        return None

    assignment_ids = list(assignments.keys())

    print("\n========================================")
    print("         MY ASSIGNED CLASSES")
    print("========================================")

    for index, assignment_id in enumerate(assignment_ids, start=1):

        details = assignments[assignment_id]

        print(
            f"{index}. "
            f"{details['subject_name']} | "
            f"{details['year']} Year | "
            f"{details['department']} | "
            f"Section {details['section']}"
        )

    while True:

        try:

            choice = int(input("\nEnter Choice : "))

            if 1 <= choice <= len(assignment_ids):

                return assignments[assignment_ids[choice - 1]]

        except ValueError:
            pass

        print("❌ Invalid Choice.")



# ==========================================
# View Faculty Subjects
# ==========================================

def view_faculty_subjects(faculty_id):

    assignments = get_faculty_assignments(faculty_id)

    if not assignments:

        print("\n❌ No Subjects Assigned.")
        return

    print("\n" + "=" * 70)
    print("                 MY SUBJECTS")
    print("=" * 70)

    print(
        f"{'Subject':<25}"
        f"{'Year':<8}"
        f"{'Department':<18}"
        f"{'Section'}"
    )

    print("-" * 70)

    for details in assignments.values():

        print(
            f"{details['subject_name']:<25}"
            f"{details['year']:<8}"
            f"{details['department']:<18}"
            f"{details['section']}"
        )

    print("=" * 70)