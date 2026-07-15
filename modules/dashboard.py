# ==========================================
# modules/dashboard.py
# ==========================================

from datetime import datetime

from database.database_manager import (
    load_students,
    load_faculty,
    load_subjects,
    load_attendance,
    load_assignments
)


# ==========================================
# Total Students
# ==========================================

def total_students():

    return len(load_students())


# ==========================================
# Total Faculty
# ==========================================

def total_faculty():

    return len(load_faculty())


# ==========================================
# Total Subjects
# ==========================================

def total_subjects():

    return len(load_subjects())


# ==========================================
# Attendance Records
# ==========================================

def attendance_records():

    return len(load_attendance())


# ==========================================
# Total Assignments
# ==========================================

def total_assignments():

    return len(load_assignments())


# ==========================================
# Today's Attendance
# ==========================================

def today_attendance():

    attendance = load_attendance()

    today = datetime.now().strftime("%d-%m-%Y")

    count = 0

    for record in attendance.values():

        if record.get("date") == today:

            count += 1

    return count


# ==========================================
# Students Below 75%
# ==========================================

def students_below_75():

    students = load_students()

    attendance = load_attendance()

    count = 0

    for student_id in students:

        total = 0
        present = 0

        for record in attendance.values():

            if student_id in record.get("attendance", {}):

                total += 1

                if record["attendance"][student_id] == "P":

                    present += 1

        percentage = 0

        if total != 0:

            percentage = (present / total) * 100

        if percentage < 75:

            count += 1

    return count


# ==========================================
# Greeting
# ==========================================

def greeting():

    hour = datetime.now().hour

    if hour < 12:

        return "🌅 Good Morning"

    elif hour < 17:

        return "☀ Good Afternoon"

    elif hour < 21:

        return "🌇 Good Evening"

    else:

        return "🌙 Good Night"


# ==========================================
# System Status
# ==========================================

def system_status():

    databases = {

        "Students Database": load_students(),

        "Faculty Database": load_faculty(),

        "Subjects Database": load_subjects(),

        "Attendance Database": load_attendance(),

        "Assignments Database": load_assignments()

    }

    print()

    print("╔══════════════════════════════════════════════╗")
    print("║               SYSTEM STATUS                 ║")
    print("╚══════════════════════════════════════════════╝")

    for name, data in databases.items():

        if isinstance(data, dict):

            print(f"🟢 {name:<25} Ready")

        else:

            print(f"🔴 {name:<25} Error")


# ==========================================
# Dashboard
# ==========================================

def dashboard(current_user, role):

    now = datetime.now()

    role_name = "Administrator" if role.lower() == "admin" else "Faculty"

    print()

    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║                 🎓 COLLEGE ATTENDANCE MANAGEMENT SYSTEM             ║")
    print("║                    Version 1.0 | Python Console ERP                 ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    print()

    print(f"{greeting()}, {role_name}")

    print()

    print("┌────────────────────────────────────────────────────────────────────┐")

    print(f"│ 👤 Logged in User : {current_user:<46}│")

    print(f"│ 🛡️ Role          : {role_name:<46}│")

    print(f"│ 📅 Date          : {now.strftime('%d-%m-%Y'):<46}│")

    print(f"│ 🕒 Time          : {now.strftime('%I:%M:%S %p'):<46}│")

    print(f"│ 🎓 Academic Year : 2026-2027{'':<38}│")

    print("└────────────────────────────────────────────────────────────────────┘")

    print()

    print("┌────────────────────── SYSTEM OVERVIEW ──────────────────────────────┐")

    print("│                                                                    │")

    print(
        f"│ 👨‍🎓 Students            : {total_students():<5}"
        f"📚 Subjects         : {total_subjects():<5}│"
    )

    print(
        f"│ 👨‍🏫 Faculty             : {total_faculty():<5}"
        f"📝 Assignments     : {total_assignments():<5}│"
    )

    print(
        f"│ 📖 Attendance          : {attendance_records():<5}"
        f"📅 Today's Classes : {today_attendance():<5}│"
    )

    print(
        f"│ ⚠ Below 75%           : {students_below_75():<5}"
        f"💾 Backup Status   : Ready│"
    )

    print("│                                                                    │")

    print("└────────────────────────────────────────────────────────────────────┘")

    print()

    print("┌──────────────────────────── MAIN MENU ──────────────────────────────┐")

    print()

    print("   1️  Student Management")

    print()

    print("   2️  Faculty Management")

    print()

    print("   3️  Subject Management")

    print()

    print("   4️  Attendance Management")

    print()

    print("   5️  Assignment Management")

    print()

    print("   6️  Reports")

    print()

    print("   7️  Settings")

    print()

    print("   8️  Logout")

    print()

    print("   9️  Exit")

    print()

    print("└────────────────────────────────────────────────────────────────────┘")

    print()

    print("══════════════════════════════════════════════════════════════════════")

    print("        © 2026 College Attendance Management System")

    print("              Developed by CHILAKA MADHU BABU")

    print("══════════════════════════════════════════════════════════════════════")