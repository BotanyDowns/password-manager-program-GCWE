# no_passwords_here_v3.py
# Stores a given user's passwords in a secure place that reduces the need for much memorising, in a GUI format
# G.Chua 22/3/23

# Import the Tkinter GUI builder module, as well as the particular module that allows a textbox to be scrolled through
from tkinter import *
from tkinter import scrolledtext

# Imports the modules required to import and export the "users" and "passwords" dictionaries
from pathlib import Path
import json

# Imports the "users" dictionary into the program
path = Path("current_users.json")
contents = path.read_text()
users = json.loads(contents)

# Imports the "passwords" dictionary into the program
path = Path("passwords.json")
contents = path.read_text()
passwords = json.loads(contents)

def check_login():
    """Identifies whether the entered username and password exist in the database - if yes, they are logged in. If not, they are asked to try again"""
    if ent_username.get() in users and ent_accesstoken.get() == users.get(ent_username.get()):
            root.withdraw()
            logged_in_window()
    else:
        txt_loginfailed.delete("1.0", END)
        txt_loginfailed.insert(END, " Login failed - ensure your username and password are correct.")

def logged_in_window():
    """Once the user's credentials have been verified, they are taken to the main menu frame - here, they may either view their existing passwords, add a new password or log out"""
    global main_menu
    main_menu = Toplevel()
    main_menu.title(f"Main Menu for {ent_username.get()}")
    main_menu.geometry("800x400")

    lbl_loggedintitle = Label(main_menu, text="Main Menu", font=20)
    lbl_loggedintitle.pack(pady=10)

    lbl_menuoptions = Label(main_menu, text="Options", font=15)
    lbl_menuoptions.pack(pady=10)

    btn_showpasswords = Button(main_menu, text="Show Passwords", command=show_passwords)
    btn_showpasswords.pack(pady=10)

    btn_addpassword = Button(main_menu, text="Add Password", command=add_password)
    btn_addpassword.pack(pady=10)

    btn_exit = Button(main_menu, text="Log Out", command=logout)
    btn_exit.pack(pady=10)

    global txt_messages
    txt_messages = scrolledtext.ScrolledText(main_menu, height=10, width=90)
    txt_messages.pack()

def show_passwords():
    """Shows all existing passwords for the user in the format Address: Password"""
    txt_messages.delete("1.0", END)
    individual_passwords = passwords[ent_username.get()]

    txt_messages.insert(END, "Here are your list of passwords:")
    for address in passwords[ent_username.get()]:
        txt_messages.insert(END, f"\n{address.title()}: {individual_passwords[address]}")

def add_password():
    """Requests the user to give an address and the password for it - when they click the button this pair is then saved into the database"""
    txt_messages.delete("1.0", END)

    global add_password_frame
    add_password_frame = Toplevel()
    add_password_frame.title(f"Add Password for {ent_username.get()}")
    add_password_frame.geometry("400x300")

    lbl_addpasswordtitle = Label(add_password_frame, text="Add Password", font=20)
    lbl_addpasswordtitle.pack(pady=10)

    lbl_address = Label(add_password_frame, text="Where will the password be stored?")
    lbl_address.pack(pady=10)

    global ent_address
    ent_address = Entry(add_password_frame)
    ent_address.pack()

    lbl_password = Label(add_password_frame, text="Type the password:")
    lbl_password.pack(pady=10)
    
    global ent_password
    ent_password = Entry(add_password_frame, show="*")
    ent_password.pack()

    btn_addpassword = Button(add_password_frame, text="Add Password", command=append_new_password)
    btn_addpassword.pack(pady=20)

def append_new_password():
    """Adds the address and password to the "passwords.json" file"""
    to_append = {ent_address.get().lower(): ent_password.get()}
    passwords[ent_username.get()].update(to_append)

    # Saves the newly entered passwords into the external "passwords.json" file
    with open("passwords.json", "w") as outfile:
        json.dump(passwords, outfile)
    
    add_password_frame.withdraw()
    txt_messages.insert(END, f"Password saved for {ent_address.get().title()}!")

def logout():
    """Closes the Main Menu frame and re-opens the login screen"""
    main_menu.withdraw()
    root.deiconify()
    ent_username.delete(0, END)
    ent_accesstoken.delete(0, END)

# Creates the initial login screen and gives it the desired width and height
root = Tk()
root.title("Password Manager")
root.geometry("550x500")

canvas = Canvas(root, width=200, height=200)   
canvas.pack()

user_icon = PhotoImage(file="Images/user_icon_v3.png")
canvas.create_image(15,20, anchor=NW, image=user_icon)

# Title of the program
lbl_title = Label(root, text="Password Manager", font=20)
lbl_title.pack(pady=10)

# Description of what the user is supposed to do
lbl_login = Label(root, text="Log In to your Account")
lbl_login.pack()

# Allows the user to input their registered username
lbl_username = Label(root, text="\nUsername:")
lbl_username.pack()

ent_username = Entry(root)
ent_username.pack()

# Allows the user to input their registered password
lbl_accesstoken = Label(root, text="\nPassword:")
lbl_accesstoken.pack()

ent_accesstoken = Entry(root, show="*")
ent_accesstoken.pack()

# When the button is clicked, the credentials are checked for whether they exist in the database
btn_login = Button(root, text="Log In", command=check_login)
btn_login.pack(pady=10)

# The textbox in which the "login failure" message is ouputted
txt_loginfailed = Text(root, height=1, width=63)
txt_loginfailed.pack()

root.mainloop()