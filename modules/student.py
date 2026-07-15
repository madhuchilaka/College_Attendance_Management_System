# student.py

from database.database_manager import (
    load_attendance,
    load_students,
    save_students
)
from utils.helpers import YEARS, DEPARTMENTS, SECTIONS, select_option
from utils.helpers import (
    select_class,
    select_student
)

from utils.id_generator import generate_student_id

from utils.logger import log_activity
from utils.validators import (
    validate_name,
    validate_email,
    validate_phone,
    email_exists,
    phone_exists
)



def add_student():

    students = load_students()

    print("\n========== ADD STUDENT ==========\n")

    student_id = generate_student_id()

    print(f"\nStudent ID : {student_id} (Auto Generated)")

    if student_id in students:
        print("\nStudent already exists.")
        return

    while True:

        name = input("Enter Student Name : ").strip()

        if validate_name(name):
            break

        print("❌ Invalid Name. Only letters and spaces are allowed.")

        # ==========================================
    # Email
    # ==========================================

    while True:

        email = input("Enter Email : ").strip()

        if not validate_email(email):

            print("❌ Invalid Email Format.")
            continue

        if email_exists(email, students):

            print("❌ Email Already Exists.")
            continue

        break


    # ==========================================
    # Phone Number
    # ==========================================

    while True:

        phone = input("Enter Phone Number : ").strip()

        if not validate_phone(phone):

            print("❌ Phone Number must contain exactly 10 digits.")
            continue

        if phone_exists(phone, students):

            print("❌ Phone Number Already Exists.")
            continue

        break

        

    gender = select_option(
        ["Male", "Female", "Other"],
        "Select Gender"
    )

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

    students[student_id] = {

        "name": name,

        "gender": gender,

        "email": email,

        "phone": phone,

        "year": year,

        "department": department,

        "section": section,

        "attendance": {}

    }

    try:
        save_students(students)
        log_activity(f"Student Added : {student_id}")
        print("\n✅ Student Added Successfully.")
    except Exception as e:
        print("\n❌ Failed to Save Student.")
        print(e)

def filter_students(year, department, section):
    """
    Return students belonging to the selected class.
    """

    students = load_students()

    filtered_students = {}

    for student_id, details in students.items():

        if (
            details["year"] == year
            and details["department"] == department
            and details["section"] == section
        ):

            filtered_students[student_id] = details

    return filtered_students


def view_students():

    year, department, section = select_class()

    students = filter_students(year, department, section)

    if not students:
        print("\nNo students found.")
        return

    print("\n" + "=" * 80)
    print(f"{'Roll No':<15}{'Name':<20}{'Gender':<10}{'Department':<20}{'Section'}")
    print("=" * 80)

    for student_id, details in students.items():

        print(
            f"{student_id:<15}"
            f"{details['name']:<20}"
            f"{details['email']:<25}"
            f"{details['phone']:<15}"
            f"{details['year']:<10}"
            f"{details['gender']:<10}"
            f"{details['department']:<20}"
            f"{details['section']}"
        )

    print("=" * 80)


def search_student():

    year, department, section = select_class()

    students = filter_students(
        year,
        department,
        section
    )

    if not students:

        print("\nNo students found.")
        return


    
    student_id, details = select_student(students)


    print("\n")
    print("=" * 40)

    print("Student Details")

    print("=" * 40)

    print(f"Student ID : {student_id}")
    print(f"Name        : {details['name']}")
    print(f"Email       : {details['email']}")
    print(f"Phone       : {details['phone']}")
    print(f"Gender      : {details['gender']}")
    print(f"Year        : {details['year']}")
    print(f"Department  : {details['department']}")
    print(f"Section     : {details['section']}")

    print("=" * 40)


def update_student():

    year, department, section = select_class()

    students = filter_students(year, department, section)

    if not students:
        print("\nNo students found.")
        return

    student_id, details = select_student(students)

    print("\n========== UPDATE STUDENT ==========")

    # Name
    new_name = input(f"Name ({details['name']}): ").strip()

    if new_name:
        details["name"] = new_name.title()

    # Email
    new_email = input(f"Email ({details['email']}): ").strip()

    if new_email:
        details["email"] = new_email

    # Phone
    new_phone = input(f"Phone ({details['phone']}): ").strip()

    if new_phone:
        details["phone"] = new_phone

    # Gender
    gender = select_option(
        ["Male", "Female", "Other"],
        "Select Gender",
        allow_skip=True
    )

    if gender != "Keep Current":
        details["gender"] = gender

    # Academic Year
    year = select_option(
        YEARS,
        "Select Academic Year",
        allow_skip=True
    )

    if year != "Keep Current":
        details["year"] = year

    # Department
    department = select_option(
        DEPARTMENTS,
        "Select Department",
        allow_skip=True
    )

    if department != "Keep Current":
        details["department"] = department

    # Section
    section = select_option(
        SECTIONS,
        "Select Section",
        allow_skip=True
    )

    if section != "Keep Current":
        details["section"] = section

    all_students = load_students()

    all_students[student_id] = details

    try:
        save_students(all_students)
        log_activity(f"Student Updated : {student_id}")
        print("\n✅ Student Updated Successfully.")
    except Exception as e:
        print("\n❌ Failed to Save Student.")
        print(e)
     

def delete_student():

    year, department, section = select_class()

    students = filter_students(year, department, section)

    if not students:
        print("\nNo students found.")
        return

    student_id, details = select_student(students)

    print("\nStudent Details")
    print("-" * 30)
    print(f"Student ID : {student_id}")
    print(f"Name        : {details['name']}")
    print(f"Department  : {details['department']}")
    print(f"Section     : {details['section']}")

    confirm = input("\nAre you sure you want to delete this student? (Y/N): ").strip().upper()

    if confirm == "Y":

        all_students = load_students()

        attendance = load_attendance()

        for record in attendance.values():

            if student_id in record.get("attendance", {}):

                print("\n❌ Cannot Delete Student.")
                print("Attendance records already exist.")

                return

        del all_students[student_id]

        try:
            save_students(all_students)
            log_activity(f"Student Deleted : {student_id}")
            print("\n✅ Student deleted successfully.")
        except Exception as e:
            print("\n❌ Failed to Delete Student.")
            print(e)
         
    else:

        print("\nDeletion cancelled.")


