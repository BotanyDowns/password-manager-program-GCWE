# no_passwords_here_v2.py
# Stores a given user's passwords in a secure place that reduces the need for much memorising
# G.Chua 15/3/2023

# Imports the modules required to import and export the "users" and "passwords" dictionaries
from pathlib import Path
import json

# Imports the module that "asterisks" the login password inputs
from pwinput import pwinput

def show_passwords(username):
    """Shows the passwords for a given user"""
    individual_passwords = passwords[username]
    print("\nHere are your list of passwords:")
    for address in passwords[username]:
        print(f"{address.title()}: {individual_passwords[address]}")
    
    main_menu(username)

def add_password(username):
    """Adds passwords to a given user's database"""
    append_address = input("\nWhere do you want to add this password? ").lower()
    append_password = input(f"Type your password for {append_address.title()}: ")
    to_append = {append_address: append_password}
    passwords[username].update(to_append)

    # Saves the newly entered passwords into the external "passwords.json" file
    with open("passwords.json", "w") as outfile:
        json.dump(passwords, outfile)

    print("\nPassword added!")
    
    main_menu(username)

def main_menu(username):
    """The main menu of the program - gives the user the option to either show their current passwords,
    add new passwords or log out of their account"""
    option = input("""\nPick an option:
1. Show passwords
2. Add password
3. Exit
Option: """)
    while option not in ["1", "2", "3"]:
        option = input("""\nInvalid option selected - pick an option:
1. Show passwords
2. Add password
3. Exit
Option: """)
    
    if option == "1":
        show_passwords(username)
    elif option == "2":
        add_password(username)
    else:
        print("\n------------------------- Logging out. -------------------------")
        return

# Imports the "users" dictionary into the program
path = Path("current_users.json")
contents = path.read_text()
users = json.loads(contents)

# Imports the "passwords" dictionary into the program
path = Path("passwords.json")
contents = path.read_text()
passwords = json.loads(contents)

# Asks whether the user is registered into the system - only "y" and "n" are allowed as responses
registered_user = input("Welcome to the Password Manager - are you registered with us? (y/n) ")

while registered_user not in ["y", "n"]:
    registered_user = input("Invalid response - are you registered with us? (y/n) ")

# If the user is not registered yet, they are added into a system through a questionnaire for a username and password
if registered_user == "n":
    new_user = input("\nPick a username: ")
    if new_user in users.keys():
        new_user = input("Username already exists - pick another username: ")
    
    passwords_same = "n"
    while passwords_same == "n":
        new_password = pwinput("\nPick a password: ")
        confirm_new_password = pwinput("\nRe-type your password: ")
        if confirm_new_password != new_password:
            print("\nPasswords do not match! Password prompt reset.")
        else:
            break

    users[new_user] = new_password
    passwords[new_user] = {}

    with open("current_users.json", "w") as outfile:
        json.dump(users, outfile)

    print("\nAccount successfully registered!")

# If the user is registered/has just registered, the log-in interface boots and requests for the username and password
print("\n------------------------- Login Interface -------------------------")

username = input("\nEnter your username: ")
while username not in users.keys():
    username = input("Unregistered username entered - enter your username: ")

access_token = pwinput("\nEnter your password: ")
while access_token != users.get(username):
    access_token = pwinput("Access Denied - enter your password: ")

# The user is logged into their account
print(f"\n------------------------- Logged in as {username} -------------------------")

# Opens the "main menu" for the individual logged in
main_menu(username)