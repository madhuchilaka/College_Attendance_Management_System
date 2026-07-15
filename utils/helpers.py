
# ==========================
# Constants
# ==========================

YEARS = [1, 2, 3, 4]

SEMESTERS = [1, 2]

DEPARTMENTS = [
    "CSE",
    "CSE-AIML",
    "IT",
    "ECE",
    "EEE"
]

SECTIONS = [
    "A",
    "B",
    "C"
]

DESIGNATIONS = [
    "Assistant Professor",
    "Associate Professor",
    "Professor",
    "Head of Department"
]

# ==========================
# Generic Menu Selection
# ==========================

def select_option(options, title, allow_skip=False):

    print(f"\n{title}")
    print("-" * len(title))

    display_options = options.copy()

    if allow_skip:
        display_options.append("Keep Current")

    for index, option in enumerate(display_options, start=1):
        print(f"{index}. {option}")

    while True:

        try:

            choice = int(input("\nEnter Choice : "))

            if 1 <= choice <= len(display_options):
                return display_options[choice - 1]

            print("Invalid Choice!")

        except ValueError:

            print("Please enter a valid number.")

# ==========================
# Select Class
# ==========================

def select_class():

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

    return year, department, section

# ==========================
# Generic Dictionary Selector
# ==========================

def select_from_dictionary(data, display_key):

    """
    Generic selector.

    Example:

    roll_no, student =
        select_from_dictionary(students,"name")

    faculty_id, faculty =
        select_from_dictionary(faculty,"name")

    subject_id, subject =
        select_from_dictionary(subjects,"subject_name")
    """

    items = list(data.items())

    print()

    for index, (key, value) in enumerate(items, start=1):

        print(f"{index}. {key} - {value[display_key]}")

    while True:

        try:

            choice = int(input("\nEnter Choice : "))

            if 1 <= choice <= len(items):

                return items[choice - 1]

            print("Invalid Choice.")

        except ValueError:

            print("Enter a valid number.")

# ==========================
# Student Selector
# ==========================

def select_student(students):

    return select_from_dictionary(
        students,
        "name"
    )

# ==========================
# Faculty Selector
# ==========================

def select_faculty(faculty):

    return select_from_dictionary(
        faculty,
        "name"
    )

# ==========================
# Subject Selector
# ==========================

def select_subject(subjects):

    return select_from_dictionary(
        subjects,
        "subject_name"
    )