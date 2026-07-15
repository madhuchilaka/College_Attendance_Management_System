# modules/faculty.py

from database.database_manager import (
    load_faculty,
    save_faculty,
    load_auth,
    save_auth
)

from database.database_manager import (
    load_subjects,
    load_assignments
)

from utils.helpers import (
    DEPARTMENTS,
    DESIGNATIONS,
    select_option,
    select_faculty
)


from utils.id_generator import generate_faculty_id


from utils.logger import log_activity
from utils.validators import (
    validate_name,
    validate_email,
    validate_phone,
    email_exists,
    phone_exists
)


# ==========================
# Add Faculty
# ==========================

def add_faculty():

    faculty = load_faculty()

    print("\n========== ADD FACULTY ==========\n")

    faculty_id = generate_faculty_id()

    print(f"\nFaculty ID : {faculty_id} (Auto Generated)")

    if faculty_id in faculty:
        print("\nFaculty already exists.")
        return

    while True:

        name = input("Enter Faculty Name : ").strip()

        if validate_name(name):
            break

        print("❌ Invalid Name. Only letters and spaces are allowed.")


    while True:

        email = input("Enter Email : ").strip()

        if not validate_email(email):

            print("❌ Invalid Email Format.")
            continue

        if email_exists(email, faculty):

            print("❌ Email Already Exists.")
            continue

        break

    while True:

        phone = input("Enter Phone Number : ").strip()

        if not validate_phone(phone):

            print("❌ Phone Number must contain exactly 10 digits.")
            continue

        if phone_exists(phone, faculty):

            print("❌ Phone Number Already Exists.")
            continue

        break
        

    gender = select_option(
        ["Male", "Female", "Other"],
        "Select Gender"
    )

    designation = select_option(
        DESIGNATIONS,
        "Select Designation"
    )

    department = select_option(
        DEPARTMENTS,
        "Select Department"
    )



    faculty[faculty_id] = {

        "name": name,
        "gender": gender,
        "designation": designation,
        "department": department,
        "email": email,
        "phone": phone,
        "subjects": []

    }

    # Save Faculty
    try:
        save_faculty(faculty)
        log_activity(f"Faculty Added : {faculty_id}")
    except Exception as e:
        print("❌ Error Saving Faculty")
        print(e)
        
    # -----------------------------
    # Create Login Credentials
    # -----------------------------

    auth = load_auth()

    auth[faculty_id] = {

        "username": faculty_id,

        "password": f"{faculty_id}@123",

        "role": "faculty",

        "first_login": True,

        "locked": False,

        "attempts": 0

    }

    save_auth(auth)

    print("\n✅ Faculty Added Successfully.")

    print("\nFaculty Login Credentials")

    print("-" * 35)

    print(f"Username : {faculty_id}")

    print(f"Password : {faculty_id}@123")

    print("\n⚠ Faculty must change the password after first login.")


# ==========================
# View Faculty
# ==========================

def view_faculty():

    faculty = load_faculty()

    if not faculty:
        print("\nNo Faculty Found.")
        return

    print("\n" + "=" * 110)

    print(
        f"{'Faculty ID':<12}"
        f"{'Name':<25}"
        f"{'Gender':<10}"
        f"{'Email':<25}"
        f"{'Phone':<15}"
        f"{'Designation':<25}"
        f"{'Department':<15}"
    )

    print("=" * 110)

    for faculty_id, details in faculty.items():

        print(
            f"{faculty_id:<12}"
            f"{details['name']:<25}"
            f"{details['gender']:<10}"
            f"{details['email']:<25}"
            f"{details['phone']:<15}"
            f"{details['designation']:<25}"
            f"{details['department']:<15}"
        )

    print("=" * 110)


# ==========================
# Search Faculty
# ==========================

def search_faculty():

    faculty = load_faculty()

    if not faculty:
        print("\nNo Faculty Found.")
        return

    faculty_id, details = select_faculty(faculty)

    print("\n" + "=" * 40)
    print("Faculty Details")
    print("=" * 40)

    print(f"Faculty ID  : {faculty_id}")
    print(f"Name        : {details['name']}")
    print(f"Gender      : {details['gender']}")
    print(f"Designation : {details['designation']}")
    print(f"Department  : {details['department']}")
    print(f"Email       : {details['email']}")
    print(f"Phone       : {details['phone']}")

    print("=" * 40)


# ==========================
# Update Faculty
# ==========================

def update_faculty():

    faculty = load_faculty()

    if not faculty:

        print("\nNo Faculty Found.")
        return

    faculty_id, details = select_faculty(faculty)

    print("\n========== UPDATE FACULTY ==========\n")

    name = input(f"Faculty Name ({details['name']}): ").strip()

    if name:
        details["name"] = name.title()

    gender = select_option(
        ["Male", "Female", "Other"],
        "Select Gender",
        allow_skip=True
    )

    if gender != "Keep Current":
        details["gender"] = gender

    designation = select_option(
        DESIGNATIONS,
        "Select Designation",
        allow_skip=True
    )

    if designation != "Keep Current":
        details["designation"] = designation

    department = select_option(
        DEPARTMENTS,
        "Select Department",
        allow_skip=True
    )

    if department != "Keep Current":
        details["department"] = department

    email = input(f"Email ({details['email']}): ").strip()

    if email:
        details["email"] = email

    phone = input(f"Phone ({details['phone']}): ").strip()

    if phone:
        details["phone"] = phone

    faculty[faculty_id] = details

    try:
        save_faculty(faculty)
        log_activity(f"Faculty Updated : {faculty_id}")
    except Exception as e:
        print("❌ Error Saving Faculty")
        print(e)
        
    print("\n✅ Faculty Updated Successfully.")


# ==========================
# Delete Faculty
# ==========================

def delete_faculty():

    faculty = load_faculty()

    if not faculty:

        print("\nNo Faculty Found.")
        return

    faculty_id, details = select_faculty(faculty)

    print("\n========== DELETE FACULTY ==========\n")

    print(f"Faculty ID   : {faculty_id}")
    print(f"Name         : {details['name']}")
    print(f"Department   : {details['department']}")
    print(f"Email        : {details['email']}")
    print(f"Phone        : {details['phone']}")
    print(f"Designation  : {details['designation']}")

    confirm = input(
        "\nAre you sure? (Y/N): "
    ).upper()

    if confirm == "Y":

        subjects = load_subjects()

        for subject in subjects.values():

            if subject.get("faculty_id") == faculty_id:

                print("\n❌ Cannot Delete Faculty.")
                print("Faculty is assigned to one or more subjects.")

                return

        assignments = load_assignments()

        for assignment in assignments.values():

            if assignment.get("faculty_id") == faculty_id:

                print("\n❌ Cannot Delete Faculty.")
                print("Faculty has active class assignments.")

                return

        del faculty[faculty_id]

        try:
            save_faculty(faculty)
            log_activity(f"Faculty Deleted : {faculty_id}")
        except Exception as e:
            print("❌ Error Saving Faculty")
            print(e)
            
        # Delete Login Credentials

        auth = load_auth()

        if faculty_id in auth:

            del auth[faculty_id]

            save_auth(auth)
            
        print("\n✅ Faculty Deleted Successfully.")

    else:

        print("\nDeletion Cancelled.")