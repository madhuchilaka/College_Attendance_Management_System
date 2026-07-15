# ==========================================
# modules/attendance.py
# Attendance Module Version 2.0
# ==========================================

from datetime import datetime

from database.database_manager import (
    load_students,
    load_subjects,
    load_faculty,
    load_attendance,
    save_attendance
)

from modules.assignment import (
    select_assigned_class
)

from utils.helpers import (
    YEARS,
    DEPARTMENTS,
    SECTIONS,
    select_option,
    select_subject,
    select_student
)


from utils.id_generator import generate_attendance_id
from utils.logger import log_activity


# ==========================================
# Filter Students
# ==========================================

def filter_students(year, department, section):

    students = load_students()

    filtered = {}

    for student_id, details in students.items():

        if (
            details["year"] == year
            and details["department"] == department
            and details["section"] == section
        ):

            filtered[student_id] = details

    return filtered



# ==========================================
# Generate Attendance ID
# ==========================================

def generate_attendance_id():

    attendance = load_attendance()

    return f"ATT{len(attendance)+1:04}"



# ==========================================
# Check Duplicate Attendance
# ==========================================

def attendance_exists(
    attendance,
    faculty_id,
    subject_code,
    year,
    department,
    section,
    date
):

    for record in attendance.values():

        if (

            record.get("faculty_id") == faculty_id

            and

            record.get("subject_code") == subject_code

            and

            record.get("year") == year

            and

            record.get("department") == department

            and

            record.get("section") == section

            and

            record.get("date") == date

        ):

            return True

    return False



# ==========================================
# Save Attendance Record
# ==========================================

def save_attendance_record(

    faculty_id,
    faculty_name,

    subject_code,
    subject_name,

    year,
    department,
    section,

    attendance_data

):

    attendance = load_attendance()

    record_id = generate_attendance_id()

    attendance[record_id] = {

        "date": datetime.now().strftime("%d-%m-%Y"),

        "faculty_id": faculty_id,

        "faculty_name": faculty_name,

        "subject_code": subject_code,

        "subject_name": subject_name,

        "year": year,

        "department": department,

        "section": section,

        "attendance": attendance_data

    }

    try:
        save_attendance(attendance)
        log_activity(f"Attendance Recorded : {record_id}")
    except Exception as e:
        print("❌ Error Saving Attendance")
        print(e)


# ==========================================
# Attendance Summary
# ==========================================

def attendance_summary(attendance_data):

    total = len(attendance_data)

    present = sum(

        1

        for status in attendance_data.values()

        if status == "P"

    )

    absent = total - present

    percentage = 0

    if total != 0:

        percentage = (present / total) * 100

    print("\n" + "=" * 50)

    print("ATTENDANCE SUMMARY")

    print("=" * 50)

    print(f"Total Students : {total}")

    print(f"Present        : {present}")

    print(f"Absent         : {absent}")

    print(f"Percentage     : {percentage:.2f}%")

    print("=" * 50)




# ==========================================
# Admin Mark Attendance
# ==========================================


def mark_attendance():

    print("\n" + "=" * 50)
    print("          MARK ATTENDANCE")
    print("=" * 50)

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

    students = filter_students(
        year,
        department,
        section
    )

    if not students:

        print("\n❌ No Students Found.")

        return

    subjects = load_subjects()

    if not subjects:

        print("\n❌ No Subjects Found.")

        return

    print("\nSelect Subject")

    subject_code, subject = select_subject(subjects)

    faculty = load_faculty()

    faculty_id = subject["faculty_id"]

    faculty_name = faculty.get(
        faculty_id,
        {}
    ).get(
        "name",
        "Unknown"
    )

    attendance = {}

    print()

    for student_id, details in students.items():

        while True:

            status = input(
                f"{student_id} - {details['name']} (P/A): "
            ).strip().upper()

            if status in ["P", "A"]:

                attendance[student_id] = status

                break

            print("❌ Enter only P or A.")

    attendance_db = load_attendance()

    today = datetime.now().strftime("%d-%m-%Y")

    if attendance_exists(

        attendance_db,

        faculty_id,

        subject_code,

        year,

        department,

        section,

        today

    ):

        print("\n❌ Attendance Already Marked Today.")

        return

    try:
        save_attendance_record(

            faculty_id,

            faculty_name,

            subject_code,

            subject["subject_name"],

            year,

            department,

            section,

            attendance

        )
        log_activity(f"Attendance Recorded : {subject_code} - {today}")
        print("\n✅ Attendance Recorded Successfully.")
    except Exception as e:
        print("❌ Error Saving Attendance")
        print(e)
        return

    attendance_summary(attendance)


# ==========================================
# Faculty Attendance
# ==========================================


def faculty_attendance(faculty_id):

    assignment = select_assigned_class(faculty_id)

    if assignment is None:

        return

    year = assignment["year"]

    department = assignment["department"]

    section = assignment["section"]

    students = filter_students(

        year,

        department,

        section

    )

    if not students:

        print("\n❌ No Students Found.")

        return

    attendance = {}

    print("\n" + "=" * 50)

    print("MARK ATTENDANCE")

    print("=" * 50)

    print(f"Subject : {assignment['subject_name']}")

    print(f"Year    : {year}")

    print(f"Dept    : {department}")

    print(f"Section : {section}")

    print()

    for student_id, details in students.items():

        while True:

            status = input(

                f"{student_id} - {details['name']} (P/A): "

            ).strip().upper()

            if status in ["P", "A"]:

                attendance[student_id] = status

                break

            print("❌ Enter only P or A.")

    attendance_db = load_attendance()

    today = datetime.now().strftime("%d-%m-%Y")

    if attendance_exists(

        attendance_db,

        faculty_id,

        assignment["subject_code"],

        year,

        department,

        section,

        today

    ):

        print("\n❌ Attendance Already Marked Today.")

        return

    faculty = load_faculty()

    faculty_name = faculty.get(

        faculty_id,

        {}

    ).get(

        "name",

        "Unknown"

    )

    try:
        save_attendance_record(

            faculty_id,

            faculty_name,

            assignment["subject_code"],

            assignment["subject_name"],

            year,

            department,

            section,

            attendance

        )
        log_activity(f"Attendance Recorded : {assignment['subject_code']} - {today}")
        print("\n✅ Attendance Recorded Successfully.")
    except Exception as e:
        print("❌ Error Saving Attendance")
        print(e)
        return
    


    attendance_summary(attendance)



# ==========================================
# View Attendance
# ==========================================

def view_attendance():

    attendance = load_attendance()

    if not attendance:

        print("\n❌ No Attendance Records Found.")

        return

    students = load_students()

    print("\n" + "=" * 80)
    print("               ATTENDANCE RECORDS")
    print("=" * 80)

    attendance_list = list(attendance.items())

    for index, (record_id, record) in enumerate(attendance_list, start=1):

        print(

            f"{index}. "

            f"{record['date']} | "

            f"{record['subject_name']} | "

            f"{record['year']} Year | "

            f"{record['department']} | "

            f"Section {record['section']}"

        )

    while True:

        try:

            choice = int(input("\nSelect Record : "))

            if 1 <= choice <= len(attendance_list):

                break

            print("❌ Invalid Choice.")

        except ValueError:

            print("❌ Enter a valid number.")

    record_id, record = attendance_list[choice - 1]

    print("\n" + "=" * 80)

    faculty = load_faculty()

    faculty_name = "Unknown"

    for faculty_id, details in faculty.items():

        if faculty_id == record["faculty_id"]:

            faculty_name = details["name"]

            break


    print(f"Attendance ID : {record_id}")
    print(f"Date          : {record.get('date', '-')}")
    print(f"Faculty       : {faculty_name}")
    print(f"Subject       : {record.get('subject_name', '-')}")
    print(f"Year          : {record.get('year', '-')}")
    print(f"Department    : {record.get('department', '-')}")
    print(f"Section       : {record.get('section', '-')}")

    print("=" * 80)

    print(f"{'Roll No':<15}{'Name':<25}{'Status'}")

    print("-" * 80)

    for student_id, status in record["attendance"].items():

        name = students.get(

            student_id,

            {}

        ).get(

            "name",

            "Unknown"

        )

        status_text = "Present" if status == "P" else "Absent"

        print(

            f"{student_id:<15}"

            f"{name:<25}"

            f"{status_text}"

        )

    print("=" * 80)



# ==========================================
# Attendance History
# ==========================================



def attendance_history():

    attendance = load_attendance()

    if not attendance:

        print("\n❌ No Attendance History Found.")

        return

    print("\n" + "=" * 80)

    print("             ATTENDANCE HISTORY")

    print("=" * 80)

    for record in attendance.values():

        total = len(record["attendance"])

        present = sum(

            1

            for status in record["attendance"].values()

            if status == "P"

        )

        absent = total - present

        print(

            f"{record['date']} | "

            f"{record['subject_name']} | "

            f"{record['year']} Year | "

            f"{record['department']} | "

            f"{record['section']} | "

            f"P:{present} "

            f"A:{absent}"

        )

    print("=" * 80)


# ==========================================
# Attendance Percentage
# ==========================================


def attendance_percentage():

    students = load_students()

    if not students:

        print("\n❌ No Students Found.")

        return

    student_id, student = select_student(students)

    attendance = load_attendance()

    total = 0

    present = 0

    for record in attendance.values():

        if student_id in record["attendance"]:

            total += 1

            if record["attendance"][student_id] == "P":

                present += 1

    percentage = 0

    if total != 0:

        percentage = (present / total) * 100

    print("\n" + "=" * 50)

    print("ATTENDANCE PERCENTAGE")

    print("=" * 50)

    print(f"Student : {student['name']}")

    print(f"Student ID : {student_id}")

    print(f"Total Classes : {total}")

    print(f"Present       : {present}")

    print(f"Absent        : {total-present}")

    print(f"Percentage    : {percentage:.2f}%")

    print("=" * 50)


# ==========================================
# Daily Report
# ==========================================


def daily_report():

    attendance = load_attendance()

    today = datetime.now().strftime("%d-%m-%Y")

    present = 0

    absent = 0

    for record in attendance.values():

        if record["date"] == today:

            present += sum(

                1

                for status in record["attendance"].values()

                if status == "P"

            )

            absent += sum(

                1

                for status in record["attendance"].values()

                if status == "A"

            )

    print("\n" + "=" * 50)

    print("TODAY'S REPORT")

    print("=" * 50)

    print(f"Date    : {today}")

    print(f"Present : {present}")

    print(f"Absent  : {absent}")

    print("=" * 50)



# ==========================================
# Faculty Attendance Reports
# ==========================================


def faculty_attendance_reports(faculty_id):

    attendance = load_attendance()

    if not attendance:

        print("\n❌ No Attendance Records Found.")

        return

    print("\n" + "=" * 100)

    print("                 MY ATTENDANCE REPORTS")

    print("=" * 100)

    print(

        f"{'Date':<15}"

        f"{'Subject':<25}"

        f"{'Class':<20}"

        f"{'Present':<10}"

        f"{'Absent'}"

    )

    print("-" * 100)

    found = False

    for record in attendance.values():

        if record["faculty_id"] == faculty_id:

            found = True

            total = len(record["attendance"])

            present = sum(

                1

                for status in record["attendance"].values()

                if status == "P"

            )

            absent = total - present

            classroom = (

                f"{record['year']} "

                f"{record['department']} "

                f"{record['section']}"

            )

            print(

                f"{record['date']:<15}"

                f"{record['subject_name']:<25}"

                f"{classroom:<20}"

                f"{present:<10}"

                f"{absent}"

            )

    if not found:

        print("\nNo Attendance Records Found.")

    print("=" * 100)


# ==========================================
# Search Attendance
# ==========================================


def search_attendance():

    attendance = load_attendance()

    if not attendance:

        print("\n❌ No Attendance Records.")

        return

    record_id = input("\nEnter Attendance ID : ").strip().upper()

    if record_id not in attendance:

        print("\n❌ Attendance Record Not Found.")

        return

    record = attendance[record_id]

    print("\n" + "=" * 60)

    print("ATTENDANCE DETAILS")

    print("=" * 60)

    print(f"Date        : {record['date']}")

    print(f"Faculty     : {record['faculty_name']}")

    print(f"Subject     : {record['subject_name']}")

    print(f"Year        : {record['year']}")

    print(f"Department  : {record['department']}")

    print(f"Section     : {record['section']}")

    print("=" * 60)


# ==========================================
# Delete Attendance
# ==========================================


def delete_attendance():

    attendance = load_attendance()

    if not attendance:

        print("\n❌ No Attendance Records.")

        return

    record_id = input("\nEnter Attendance ID : ").strip().upper()

    if record_id not in attendance:

        print("\n❌ Attendance Record Not Found.")

        return

    confirm = input("\nDelete this record? (Y/N): ").strip().upper()

    if confirm == "Y":

        del attendance[record_id]

        save_attendance(attendance)

        print("\n✅ Attendance Deleted Successfully.")

    else:

        print("\nDeletion Cancelled.")


# ==========================================
# Edit Attendance
# ==========================================


def edit_attendance():

    attendance = load_attendance()

    students = load_students()

    if not attendance:

        print("\n❌ No Attendance Records.")

        return

    record_id = input("\nEnter Attendance ID : ").strip().upper()

    if record_id not in attendance:

        print("\n❌ Attendance Record Not Found.")

        return

    record = attendance[record_id]

    print("\nEditing Attendance\n")

    for student_id in record["attendance"]:

        name = students.get(

            student_id,

            {}

        ).get(

            "name",

            "Unknown"

        )

        current = record["attendance"][student_id]

        new_status = input(

            f"{student_id} - {name} ({current}) P/A : "

        ).strip().upper()

        if new_status in ["P", "A"]:

            record["attendance"][student_id] = new_status

    attendance[record_id] = record

    try:
        save_attendance(attendance)
        log_activity(f"Attendance Updated : {record_id}")
    except Exception as e:
        print("❌ Error Saving Attendance")
        print(e)
        return


    print("\n✅ Attendance Updated Successfully.")








