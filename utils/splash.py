# ==========================================
# utils/splash.py
# ==========================================

import time
import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def loading_bar():

    print("\nLoading System...\n")

    bar_length = 30

    for i in range(bar_length + 1):

        percent = int((i / bar_length) * 100)

        bar = "█" * i + "-" * (bar_length - i)

        print(f"\r[{bar}] {percent}%", end="")

        time.sleep(0.05)

    print("\n")


def splash_screen():

    clear_screen()

    print()

    print("╔" + "═" * 62 + "╗")
    print("║" + "COLLEGE ATTENDANCE MANAGEMENT SYSTEM".center(62) + "║")
    print("║" + "Version 1.0".center(62) + "║")
    print("║" + " ".center(62) + "║")
    print("║" + "Developed By".center(62) + "║")
    print("║" + "CHILAKA MADHU BABU".center(62) + "║")
    print("╚" + "═" * 62 + "╝")

    loading_bar()

    time.sleep(1)

    clear_screen()