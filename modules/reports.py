# ==========================================
# modules/reports.py
# ==========================================

from database.database_manager import (
    load_students,
    load_subjects,
    load_faculty,
    load_attendance
)

from utils.helpers import (
    select_student,
    select_subject,
    select_faculty
)


# ==========================================
# Helper Function
# ==========================================

def calculate_student_attendance(student_id):

    attendance = load_attendance()

    present = 0
    absent = 0
    late = 0

    for record in attendance.values():

        if student_id in record["attendance"]:

            status = record["attendance"][student_id]

            if status == "P":
                present += 1

            elif status == "A":
                absent += 1

            elif status == "L":
                late += 1

    total = present + absent + late

    percentage = 0

    if total != 0:

        percentage = (present / total) * 100

    return {

        "present": present,

        "absent": absent,

        "late": late,

        "total": total,

        "percentage": percentage

    }


# ==========================================
# Student Report
# ==========================================

def student_report():

    students = load_students()

    if not students:

        print("\nNo Students Found.")

        return

    student_id, student = select_student(students)

    report = calculate_student_attendance(student_id)

    print("\n")

    print("=" * 50)

    print("      STUDENT ATTENDANCE REPORT")

    print("=" * 50)

    print(f"Student ID  : {student_id}")

    print(f"Name        : {student['name']}")

    print(f"Department  : {student['department']}")

    print(f"Section     : {student['section']}")

    print("-" * 50)

    print(f"Total Classes : {report['total']}")

    print(f"Present      : {report['present']}")

    print(f"Absent       : {report['absent']}")

    print(f"Late         : {report['late']}")

    print(f"Attendance % : {report['percentage']:.2f}")

    print("-" * 50)

    if report["percentage"] >= 75:

        print("Status : ELIGIBLE")

    else:

        print("Status : NOT ELIGIBLE")

    print("=" * 50)


# ==========================================
# Subject Report
# ==========================================

def subject_report():

    subjects = load_subjects()

    if not subjects:

        print("\nNo Subjects Found.")

        return

    subject_id, subject = select_subject(subjects)

    attendance = load_attendance()

    classes = 0

    total_present = 0

    total_students = 0

    for record in attendance.values():

        if record.get("subject_code") == subject.get("subject_code"):

            classes += 1

            for status in record["attendance"].values():

                total_students += 1

                if status == "P":

                    total_present += 1

    average = 0

    if total_students != 0:

        average = (total_present / total_students) * 100

    print("\n")

    print("=" * 50)

    print("        SUBJECT REPORT")

    print("=" * 50)

    print(f"Subject Code : {subject['subject_code']}")

    print(f"Subject Name : {subject['subject_name']}")

    print(f"Department   : {subject['department']}")

    print(f"Semester     : {subject['semester']}")

    print("-" * 50)

    print(f"Classes Conducted : {classes}")

    print(f"Average Attendance : {average:.2f}%")

    print("=" * 50)


# ==========================================
# Faculty Report
# ==========================================

def faculty_report():

    faculty = load_faculty()

    if not faculty:

        print("\nNo Faculty Found.")
        return

    faculty_id, faculty_details = select_faculty(faculty)

    subjects = load_subjects()
    attendance = load_attendance()

    subject_list = []

    total_classes = 0
    total_present = 0
    total_students = 0

    for _, subject in subjects.items():

        if subject["faculty_id"] == faculty_id:

            subject_list.append(subject["subject_name"])

            for record in attendance.values():

                if record.get("subject_code") == subject.get("subject_code"):

                    total_classes += 1

                    for status in record["attendance"].values():

                        total_students += 1

                        if status == "P":
                            total_present += 1

    average = 0

    if total_students != 0:

        average = (total_present / total_students) * 100

    print("\n" + "=" * 60)
    print("               FACULTY REPORT")
    print("=" * 60)

    print(f"Faculty ID   : {faculty_id}")
    print(f"Name         : {faculty_details['name']}")
    print(f"Department   : {faculty_details['department']}")
    print(f"Designation  : {faculty_details['designation']}")

    print("\nSubjects Handled")

    if subject_list:

        for subject in subject_list:
            print(f"• {subject}")

    else:
        print("No Subjects Assigned")

    print("\nTotal Classes Taken :", total_classes)
    print(f"Average Attendance : {average:.2f}%")

    print("=" * 60)


# ==========================================
# Students Below 75%
# ==========================================

def students_below_75():

    students = load_students()

    if not students:

        print("\nNo Students Found.")
        return

    print("\n" + "=" * 75)
    print("              STUDENTS BELOW 75%")
    print("=" * 75)

    print(
        f"{'Student ID':<15}"
        f"{'Name':<25}"
        f"{'Attendance %'}"
    )

    print("-" * 75)

    found = False

    for student_id, student in students.items():

        report = calculate_student_attendance(student_id)

        if report["percentage"] < 75:

            found = True

            print(
                f"{student_id:<15}"
                f"{student['name']:<25}"
                f"{report['percentage']:.2f}"
            )

    if not found:

        print("All students have attendance above 75%.")

    print("=" * 75)


# ==========================================
# Overall Summary
# ==========================================

def overall_summary():

    students = load_students()
    faculty = load_faculty()
    subjects = load_subjects()
    attendance = load_attendance()

    total_present = 0
    total_absent = 0
    total_late = 0

    for record in attendance.values():

        for status in record["attendance"].values():

            if status == "P":
                total_present += 1

            elif status == "A":
                total_absent += 1

            elif status == "L":
                total_late += 1

    total = total_present + total_absent + total_late

    average = 0

    if total != 0:

        average = (total_present / total) * 100

    print("\n" + "=" * 60)
    print("             OVERALL SUMMARY")
    print("=" * 60)

    print(f"Total Students          : {len(students)}")
    print(f"Total Faculty           : {len(faculty)}")
    print(f"Total Subjects          : {len(subjects)}")
    print(f"Attendance Records      : {len(attendance)}")

    print()

    print(f"Present Entries         : {total_present}")
    print(f"Absent Entries          : {total_absent}")
    print(f"Late Entries            : {total_late}")

    print()

    print(f"Overall Attendance      : {average:.2f}%")

    print("=" * 60)