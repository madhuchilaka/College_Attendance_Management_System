
import json
import os

BASE_DIR = os.path.dirname(__file__)

STUDENTS_FILE = os.path.join(BASE_DIR, "students.json")
FACULTY_FILE = os.path.join(BASE_DIR, "faculty.json")
SUBJECTS_FILE = os.path.join(BASE_DIR, "subjects.json")
ATTENDANCE_FILE = os.path.join(BASE_DIR, "attendance.json")
ASSIGNMENTS_FILE = os.path.join(BASE_DIR, "assignments.json")




def load_json(file_path):
    """
    Load data from a JSON file.
    """

    if not os.path.exists(file_path):
        return {}

    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def save_json(file_path, data):

    try:

        with open(file_path, "w") as file:

            json.dump(data, file, indent=4)

    except Exception as e:

        print(f"\n❌ Error Saving {file_path}")

        print(e)


def load_students():
    return load_json(STUDENTS_FILE)


def save_students(data):
    save_json(STUDENTS_FILE, data)



def load_faculty():
    return load_json(FACULTY_FILE)

def save_faculty(data):
    save_json(FACULTY_FILE, data)



def load_subjects():
    return load_json(SUBJECTS_FILE)


def save_subjects(data):
    save_json(SUBJECTS_FILE, data)  



def load_attendance():
    return load_json(ATTENDANCE_FILE)


def save_attendance(data):
    save_json(ATTENDANCE_FILE, data)



# ==========================================
# Authentication Database
# ==========================================

AUTH_FILE = os.path.join(BASE_DIR, "auth.json")


def load_auth():
    return load_json(AUTH_FILE)


def save_auth(data):
    save_json(AUTH_FILE, data)


# ==========================================
# Assignment Database
# ==========================================

def load_assignments():

    return load_json(ASSIGNMENTS_FILE)


def save_assignments(data):

    save_json(ASSIGNMENTS_FILE, data)