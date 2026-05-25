#!/usr/bin/env python3
import sys
sys.path.append("/usr/local/lib/tamo-cli/TamoAPI")

from pprint import pprint
from TamoAPI import TamoSession
import json
import datetime
from textwrap import fill
from pathlib import Path
from colorama import Fore, Style

# tamo-cli
# by makkuz2013
# credit to justinas2314 for creating TamoAPI

# script should be in /usr/local/bin



# config path
CONF_PATH = Path("/etc/tamo-cli/tamo-cli-conf.json")

today = datetime.datetime.now()

# load config
with CONF_PATH.open() as f:
    conf = json.load(f)

creds = conf["credentials"]
app_config = conf["app-config"]

# filter homeworks
def homework_filter(homework: dict):
    if homework["atlikimo data"]["d"] in range(today.day + 1, today.day + 10):
        return True
    else:
        return False

# print homework 
def print_homework(homework: dict):
    global printing_homeworks
    if homework["atlikimo data"]["d"] == today.day + 1:
        if not printing_homeworks == "rytoj":
            printing_homeworks = "rytoj"
            print(Fore.RED + "Rytoj")
    if homework["atlikimo data"]["d"] == today.day + 2:
        if not printing_homeworks == "poryt":
            printing_homeworks = "poryt"
            print(Fore.YELLOW + "Poryt")
    if homework["atlikimo data"]["d"] > today.day + 2:
        if not printing_homeworks == "after":
            printing_homeworks = "after"
            print(Fore.GREEN + "Ateitis")
    print(Fore.GREEN + "  " + homework["dalykas"])
    print()
    print(Fore.CYAN + "  Atlikimo data: " + wrap_date(homework["atlikimo data"]["d"]))
    print()
    print(Fore.WHITE + fill(
        homework["namu darbas"],
        width=80,
        initial_indent="    ",
        subsequent_indent="    "
    ))
    print()

# print all of the homeworks
def print_homeworks(session: TamoSession):
    global printing_homeworks
    homeworks = filter(homework_filter, session.namu_darbai())
    printing_homeworks = ""
    for homework in homeworks:
        homework["namu darbas"] = homework["namu darbas"].replace("Bendri namų darbai:\n", "")
        print_homework(homework)

# filter grades
def grade_filter(grade):
    if grade["data"]["d"] in range(today.day - 5, today.day + 1):
        return True
    else:
        return False

# color code grades
# 0-3 red
# 4-6 yellow
# 7-9 green
# 10 bold lightgreen
def color_grade(grade: int):
    if grade in range(0, 4):
        return Fore.RED
    elif grade in range(4, 7):
        return Fore.YELLOW
    elif grade in range(7, 10):
        return Fore.GREEN
    elif grade == 10:
        return Style.BRIGHT + Fore.LIGHTGREEN_EX
    else:
        return Fore.WHITE

# function to wrap day to actual date
# example input: 25
# example output: 2026-05-25

def wrap_date(day: int):
    return f"{today.year}-{today.month}-{day}"

# print all the grades
def print_grades(session: TamoSession):
    grades = list(filter(grade_filter, session.dienynas()["ivertinimai"]))
    sorted_grades = sorted(grades, key=lambda x: x["data"]["d"])
    for grade in sorted_grades:
        print(f"{Fore.CYAN}{wrap_date(grade["data"]["d"])} {Fore.GREEN + '(Today)' if grade['data']['d'] == today.day else ''}")
        print(Fore.MAGENTA + "  " + grade["dalykas"])
        print(color_grade(int(grade["ivertinimas"])) + "  " + grade["ivertinimas"])
        print(Style.RESET_ALL)
        print()

# entry point
def main():
    with TamoSession(creds["username"], creds["password"], timeout=1) as session:
        # check arguments
        if (len(sys.argv) > 1):
            if (sys.argv[1] == "homework"):
                print_homeworks(session)
            elif (sys.argv[1] == "grades"):
                print_grades(session)
            else:
                print(Fore.WHITE + "Invalid argument supplied\n")
                print("Usage: ")
                print("  tamo homework - print homework")
                print("  tamo grades - print grades")
                print("  tamo - default action ")
        else:
            # if no args, print the action in the config.
            if app_config["default-action"] == "homework":
                print_homeworks(session)
            else:
                print_grades(session)

if __name__ == "__main__":
    main()