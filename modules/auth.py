# ==========================================
# modules/auth.py
# ==========================================

from database.database_manager import (
    load_auth,
    save_auth
)
from utils.logger import log_activity


# ==========================================
# Login Menu
# ==========================================

def login_menu():

    print("\n" + "=" * 45)
    print("           COLLEGE LOGIN")
    print("=" * 45)

    print("1. Admin Login")
    print("2. Faculty Login")
    print("3. Exit")

    return input("\nEnter Choice : ").strip()


# ==========================================
# Verify Login
# ==========================================

def verify_login(username, password):

    auth = load_auth()

    if username not in auth:

        print("\n❌ Invalid Username")
        return None

    user = auth[username]

    if user.get("locked", False):

        print("\n❌ Account Locked.")
        return None

    if password != user["password"]:

        user["attempts"] = user.get("attempts", 0) + 1

        if user["attempts"] >= 3:

            user["locked"] = True

            print("\n❌ Account Locked after 3 failed attempts.")

        else:

            remaining = 3 - user["attempts"]

            print(f"\n❌ Wrong Password. {remaining} attempt(s) left.")

        auth[username] = user

        save_auth(auth)

        return None

    user["attempts"] = 0

    auth[username] = user

    save_auth(auth)

    return username


# ==========================================
# Admin Login
# ==========================================


def admin_login():

    auth = load_auth()

    admin = auth.get("admin")

    if admin is None:

        print("\n❌ Admin account not found.")
        return None

    print("\n" + "=" * 45)
    print("           ADMIN LOGIN")
    print("=" * 45)

    username = input("Username : ").strip()
    password = input("Password : ").strip()

    if username != admin["username"]:

        print("\n❌ Invalid Username.")
        return None

    if password != admin["password"]:

        print("\n❌ Invalid Password.")
        return None

    log_activity("Admin Logged In")
    print("\n✅ Welcome Administrator.")
    

    return "admin"


# ==========================================
# Faculty Login
# ==========================================

def faculty_login():

    print("\n" + "=" * 45)
    print("          FACULTY LOGIN")
    print("=" * 45)

    username = input("Faculty ID : ").strip().upper()
    password = input("Password   : ").strip()

    user = verify_login(username, password)

    if user is None:
        return None

    if get_role(user) != "faculty":

        print("\n❌ Not a Faculty Account.")
        return None
    log_activity(f"Faculty Logged In : {username}")
    print(f"\n✅ Welcome {username}")
    

    if first_login(username):

        first_login_process(username)

    return user


# ==========================================
# Get Role
# ==========================================

def get_role(username):

    auth = load_auth()

    if username in auth:

        return auth[username]["role"]

    return None


# ==========================================
# First Login
# ==========================================

def first_login(username):

    auth = load_auth()

    return auth[username]["first_login"]


# ==========================================
# Change Password
# ==========================================

def change_password(username):

    auth = load_auth()

    print("\n" + "=" * 45)
    print("        CHANGE PASSWORD")
    print("=" * 45)

    while True:

        new_password = input("New Password : ").strip()

        confirm_password = input("Confirm Password : ").strip()

        if new_password != confirm_password:

            print("\n❌ Passwords do not match.")
            continue

        if len(new_password) < 6:

            print("\n❌ Password must be at least 6 characters.")
            continue

        break

    auth[username]["password"] = new_password
    auth[username]["first_login"] = False

    save_auth(auth)
    log_activity(f"Password Changed : {username}")
    print("\n✅ Password Changed Successfully.")


# ==========================================
# First Login Process
# ==========================================

def first_login_process(username):

    auth = load_auth()

    if auth[username]["first_login"]:

        print("\n========================================")
        print("            FIRST LOGIN")
        print("========================================")
        print("Temporary password detected.")
        print("Please change your password.\n")

        change_password(username)


# ==========================================
# Logout
# ==========================================

def logout(current_user):

    print("\n" + "=" * 45)
    log_activity(f"Faculty Logged Out : {current_user}")
    print("\n✅ Logged Out Successfully.")


# ==========================================
# Unlock Account
# ==========================================

def unlock_account(username):

    auth = load_auth()

    if username not in auth:

        print("\n❌ User Not Found.")
        return

    auth[username]["locked"] = False
    auth[username]["attempts"] = 0

    save_auth(auth)

    print("\n✅ Account Unlocked Successfully.")


# ==========================================
# Reset Password
# ==========================================

def reset_password(username):

    auth = load_auth()

    if username not in auth:

        print("\n❌ User Not Found.")
        return

    auth[username]["password"] = f"{username}@123"
    auth[username]["first_login"] = True
    auth[username]["locked"] = False
    auth[username]["attempts"] = 0

    save_auth(auth)

    print("\n✅ Password Reset Successfully.")
    print(f"Temporary Password : {username}@123")