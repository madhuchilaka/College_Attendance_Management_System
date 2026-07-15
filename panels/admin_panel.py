# ==========================================
# panels/admin_panel.py
# ==========================================

from utils.menu import (
    student_menu,
    faculty_menu,
    subject_menu,
    attendance_menu,
    reports_menu
)

from modules.student import (
    add_student,
    view_students,
    search_student,
    update_student,
    delete_student
)

from modules.faculty import (
    add_faculty,
    view_faculty,
    search_faculty,
    update_faculty,
    delete_faculty
)

from modules.subject import (
    add_subject,
    view_subjects,
    search_subject,
    update_subject,
    delete_subject
)

from modules.attendance import (
    mark_attendance,
    view_attendance,
    attendance_percentage,
    daily_report,
    attendance_history
)

from modules.reports import (
    student_report,
    subject_report,
    faculty_report,
    students_below_75,
    overall_summary
)

from modules.dashboard import dashboard
from modules.auth import logout


from modules.assignment import (
    assign_subject,
    view_assignments,
    search_assignment,
    update_assignment,
    delete_assignment 

)

from utils.menu import assignment_menu

from modules.settings import (
    settings_menu,
    change_admin_password,
    reset_faculty_password,
    unlock_faculty_account,
    backup_database,
    restore_database
)



def admin_panel(current_user, role):

    while True:

        dashboard(current_user, role)

        choice = input("\nEnter Choice : ").strip()

        # ---------------- Student ----------------

        if choice == "1":

            while True:

                student_menu()

                student_choice = input("\nEnter Choice : ").strip()

                if student_choice == "1":
                    add_student()

                elif student_choice == "2":
                    view_students()

                elif student_choice == "3":
                    search_student()

                elif student_choice == "4":
                    update_student()

                elif student_choice == "5":
                    delete_student()

                elif student_choice == "6":
                    break

                else:
                    print("\n❌ Invalid Choice.")

        # ---------------- Faculty ----------------

        elif choice == "2":

            while True:

                faculty_menu()

                faculty_choice = input("\nEnter Choice : ").strip()

                if faculty_choice == "1":
                    add_faculty()

                elif faculty_choice == "2":
                    view_faculty()

                elif faculty_choice == "3":
                    search_faculty()

                elif faculty_choice == "4":
                    update_faculty()

                elif faculty_choice == "5":
                    delete_faculty()

                elif faculty_choice == "6":
                    break

                else:
                    print("\n❌ Invalid Choice.")

        # ---------------- Subject ----------------

        elif choice == "3":

            while True:

                subject_menu()

                subject_choice = input("\nEnter Choice : ").strip()

                if subject_choice == "1":
                    add_subject()

                elif subject_choice == "2":
                    view_subjects()

                elif subject_choice == "3":
                    search_subject()

                elif subject_choice == "4":
                    update_subject()

                elif subject_choice == "5":
                    delete_subject()

                elif subject_choice == "6":
                    break

                else:
                    print("\n❌ Invalid Choice.")

        # ---------------- Attendance ----------------

        elif choice == "4":

            while True:

                attendance_menu()

                attendance_choice = input("\nEnter Choice : ").strip()

                if attendance_choice == "1":
                    mark_attendance()

                elif attendance_choice == "2":
                    view_attendance()

                elif attendance_choice == "3":
                    attendance_percentage()

                elif attendance_choice == "4":
                    daily_report()

                elif attendance_choice == "5":
                    attendance_history()

                elif attendance_choice == "6":
                    break

                else:
                    print("\n❌ Invalid Choice.")


        # ==========================================
        # Assignment Management
        # ==========================================

        elif choice == "5":

            while True:

                assignment_menu()

                assignment_choice = input("\nEnter Choice : ").strip()

                if assignment_choice == "1":

                    assign_subject()

                elif assignment_choice == "2":

                    view_assignments()

                elif assignment_choice == "3":
                    search_assignment()

                elif assignment_choice == "4":

                    update_assignment()

                elif assignment_choice == "5":

                    delete_assignment()

                elif assignment_choice == "6":

                    break

                else:

                    print("\n❌ Invalid Choice.")

        # ---------------- Reports ----------------

        elif choice == "6":

            while True:

                reports_menu()

                report_choice = input("\nEnter Choice : ").strip()

                if report_choice == "1":
                    student_report()

                elif report_choice == "2":
                    subject_report()

                elif report_choice == "3":
                    faculty_report()

                elif report_choice == "4":
                    students_below_75()

                elif report_choice == "5":
                    overall_summary()

                elif report_choice == "6":
                    break

                else:
                    print("\n❌ Invalid Choice.")

        elif choice == "7":

            while True:

                settings_menu()

                setting_choice = input("\nEnter Choice : ").strip()

                if setting_choice == "1":

                    change_admin_password()

                elif setting_choice == "2":

                    reset_faculty_password()

                elif setting_choice == "3":

                    unlock_faculty_account()

                elif setting_choice == "4":

                    backup_database()

                elif setting_choice == "5":

                    restore_database()

                elif setting_choice == "6":

                    break

                else:

                    print("\n❌ Invalid Choice.")

        elif choice == "8":

            logout(current_user)
            return "logout"

        elif choice == "9":

            return "exit"

        else:

            print("\n❌ Invalid Choice.")