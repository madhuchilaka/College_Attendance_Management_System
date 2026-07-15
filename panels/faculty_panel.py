# ==========================================
# panels/faculty_panel.py
# ==========================================

from utils.menu import faculty_dashboard_menu

from modules.attendance import (
    faculty_attendance,
    faculty_attendance_reports  
)

from modules.auth import (
    change_password,
    logout
)

from modules.assignment import view_faculty_subjects


def faculty_panel(current_user):

    while True:

        faculty_dashboard_menu()

        choice = input("\nEnter Choice : ").strip()

        # ==========================================
        # My Subjects
        # ==========================================

        if choice == "1":

            view_faculty_subjects(current_user)

        # ==========================================
        # Mark Attendance
        # ==========================================

        elif choice == "2":

            faculty_attendance(current_user)

        # ==========================================
        # My Reports
        # ==========================================

        elif choice == "3":

            faculty_attendance_reports(current_user)

        # ==========================================
        # Change Password
        # ==========================================

        elif choice == "4":

            change_password(current_user)

        # ==========================================
        # Logout
        # ==========================================

        elif choice == "5":

            logout(current_user)

            return "logout"

        else:

            print("\n❌ Invalid Choice.")