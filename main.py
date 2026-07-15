# ==========================================
# College Attendance Management System
# main.py
# ==========================================

from utils.splash import splash_screen

from modules.auth import (
    login_menu,
    admin_login,
    faculty_login,
    get_role
)

from panels.admin_panel import admin_panel
from panels.faculty_panel import faculty_panel


# ==========================================
# Main Function
# ==========================================

def main():

    splash_screen()

    while True:

        current_user = None

        role = None

        # ===============================
        # Login
        # ===============================

        while current_user is None:

            choice = login_menu()

            if choice == "1":

                current_user = admin_login()

            elif choice == "2":

                current_user = faculty_login()

            elif choice == "3":

                print("\nThank You For Using The System.")
                return

            else:

                print("\n❌ Invalid Choice.")

        role = get_role(current_user)

        # ===============================
        # Admin
        # ===============================

        if role == "admin":

            result = admin_panel(current_user, role)

        # ===============================
        # Faculty
        # ===============================

        elif role == "faculty":

            result = faculty_panel(current_user)

        else:

            print("\n❌ Invalid Role.")

            continue

        # ===============================
        # Logout
        # ===============================

        if result == "logout":

            continue

        # ===============================
        # Exit
        # ===============================

        elif result == "exit":

            print("\nThank You For Using The System.")

            break


# ==========================================
# Start Program
# ==========================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\n\nProgram Interrupted.")

    except Exception as e:

        print("\nUnexpected Error")

        print(e)