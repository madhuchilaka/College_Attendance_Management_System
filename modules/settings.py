from database.database_manager import (
    load_auth,
    save_auth
)

from utils.logger import log_activity
from utils.validators import validate_password

import os
import shutil
from datetime import datetime

import zipfile


# ==========================================
# modules/settings.py
# ==========================================

def settings_menu():

    print("\n")

    print("=" * 45)
    print("            SETTINGS")
    print("=" * 45)

    print("1. Change Admin Password")
    print("2. Reset Faculty Password")
    print("3. Unlock Faculty Account")
    print("4. Backup Database")
    print("5. Restore Database")
    print("6. Back")





# ==========================================
# Change Admin Password
# ==========================================

def change_admin_password():

    auth = load_auth()

    print("\n" + "=" * 45)
    print("      CHANGE ADMIN PASSWORD")
    print("=" * 45)

    username = input("Enter Admin Username : ").strip()

    if username not in auth:

        print("\n❌ Admin Not Found.")
        return

    if auth[username]["role"] != "admin":

        print("\n❌ This user is not an Admin.")
        return

    current_password = input("Current Password : ").strip()

    if current_password != auth[username]["password"]:

        print("\n❌ Incorrect Password.")
        return

    while True:

        new_password = input("New Password : ").strip()

        if not validate_password(new_password):

            print("\n❌ Password must contain at least 6 characters.")
            continue

        confirm_password = input("Confirm Password : ").strip()

        if new_password != confirm_password:

            print("\n❌ Passwords do not match.")
            continue

        break

    auth[username]["password"] = new_password

    try:
        save_auth(auth)
        log_activity(f"Admin Password Changed : {username}")
        print("\n✅ Admin Password Changed Successfully.")
    except Exception as e:
        print("❌ Error Saving Auth Data")
        print(e)

# ==========================================
# Reset Faculty Password
# ==========================================

def reset_faculty_password():

    auth = load_auth()

    print("\n" + "=" * 45)
    print("      RESET FACULTY PASSWORD")
    print("=" * 45)

    username = input("Enter Faculty Username : ").strip()

    if username not in auth:

        print("\n❌ Faculty Account Not Found.")
        return

    if auth[username]["role"] != "faculty":

        print("\n❌ This account is not a Faculty account.")
        return

    temp_password = f"{username}@123"

    auth[username]["password"] = temp_password
    auth[username]["first_login"] = True
    auth[username]["locked"] = False
    auth[username]["attempts"] = 0

    try:
        save_auth(auth)
        print("\n✅ Password Reset Successfully.")
        log_activity(f"Faculty Password Reset : {username}")
        print(f"Temporary Password : {temp_password}")
    except Exception as e:
        print("❌ Error Saving Auth Data")
        print(e)

    log_activity(f"Faculty Password Reset : {username}")
    print("Faculty must change the password on next login.")


# ==========================================
# Unlock Faculty Account
# ==========================================

def unlock_faculty_account():

    auth = load_auth()

    print("\n" + "=" * 45)
    print("        UNLOCK FACULTY ACCOUNT")
    print("=" * 45)

    username = input("Enter Faculty Username : ").strip()

    if username not in auth:

        print("\n❌ Faculty Account Not Found.")
        return

    if auth[username]["role"] != "faculty":

        print("\n❌ This account is not a Faculty account.")
        return

    if not auth[username]["locked"]:

        print("\nℹ️ This account is already unlocked.")
        return

    auth[username]["locked"] = False
    auth[username]["attempts"] = 0

    try:
        save_auth(auth)
        log_activity(f"Faculty Account Unlocked : {username}")
        print("\n✅ Faculty Account Unlocked Successfully.")
    except Exception as e:
        print("❌ Error Saving Auth Data")
        print(e)


# ==========================================
# Backup Database
# ==========================================

def backup_database():

    database_folder = "database"
    backup_folder = "backups"

    # Create backups folder if it doesn't exist
    os.makedirs(backup_folder, exist_ok=True)

    # Current date & time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    backup_name = os.path.join(
        backup_folder,
        f"backup_{timestamp}"
    )

    try:

        shutil.make_archive(
            backup_name,
            "zip",
            database_folder
        )
        log_activity("Database Backup Created")
        print("\n✅ Database Backup Created Successfully.")
        print(f"Location : {backup_name}.zip")

    except Exception as e:

        print("\n❌ Backup Failed.")
        print(e)


# ==========================================
# Restore Database
# ==========================================

def restore_database():

    backup_folder = "backups"
    database_folder = "database"

    if not os.path.exists(backup_folder):

        print("\n❌ Backup folder not found.")
        return

    backups = [

        file

        for file in os.listdir(backup_folder)

        if file.endswith(".zip")

    ]

    if not backups:

        print("\n❌ No Backup Files Found.")
        return

    print("\n" + "=" * 50)
    print("          RESTORE DATABASE")
    print("=" * 50)

    print("\nAvailable Backups\n")

    for index, backup in enumerate(backups, start=1):

        print(f"{index}. {backup}")

    while True:

        try:

            choice = int(input("\nEnter Choice : "))

            if 1 <= choice <= len(backups):

                selected_backup = backups[choice - 1]

                break

        except ValueError:

            pass

        print("❌ Invalid Choice.")

    confirm = input(
        "\nRestoring will overwrite the current database.\nContinue? (Y/N): "
    ).strip().upper()

    if confirm != "Y":

        print("\nRestore Cancelled.")
        return

    backup_path = os.path.join(
        backup_folder,
        selected_backup
    )

    try:

        with zipfile.ZipFile(
            backup_path,
            "r"
        ) as zip_file:

            zip_file.extractall(database_folder)

        
        log_activity("Database Restored Successfully")
        print("\n✅ Database Restored Successfully.")

    except Exception as e:

        print("\n❌ Restore Failed.")
        print(e)

