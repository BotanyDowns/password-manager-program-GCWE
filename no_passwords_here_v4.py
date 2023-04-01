# no_passwords_here_v4.py
# Stores a given user's passwords in a secure place that reduces the need for much memorising, in a GUI format
# G.Chua 1/4/23

# Import the Tkinter GUI builder module, as well as the particular module that allows a textbox to be scrolled through
from tkinter import *

# Imports the modules required to import and export the "users" and "passwords" dictionaries
from pathlib import Path
import json

# Imports a library that customises the Tkinter GUI appearance
import customtkinter
customtkinter.set_appearance_mode("dark")

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
        txt_loginfailed.insert(END, " LOGIN FAILED: Ensure your username and password are correct.")

def logged_in_window():
    """Once the user's credentials have been verified, they are taken to the main menu frame - here, they may either view their existing passwords, add a new password or log out"""
    global main_menu
    main_menu = customtkinter.CTkToplevel(root)
    main_menu.title("Main Menu")
    main_menu.geometry("750x250")
    main_menu.wm_transient(root)

    lbl_loggedintitle = customtkinter.CTkLabel(master=main_menu, text=f"{ent_username.get()}'s Dashboard", font=customtkinter.CTkFont(size=20, weight="bold"))
    lbl_loggedintitle.grid(row=0, column=1, pady=10)

    lbl_menuoptions = customtkinter.CTkLabel(master=main_menu, text="Options", font=customtkinter.CTkFont(size=15))
    lbl_menuoptions.grid(row=1, column=1, pady=5)

    btn_showpasswords = customtkinter.CTkButton(master=main_menu, text="Show Passwords", command=show_passwords)
    btn_showpasswords.grid(row=2, column=0, padx=20, pady=10)

    btn_addpassword = customtkinter.CTkButton(master=main_menu, text="Add Password", command=add_password)
    btn_addpassword.grid(row=2, column=1)

    btn_exit = customtkinter.CTkButton(master=main_menu, text="Log Out", command=logout)
    btn_exit.grid(row=2, column=2)

    global txt_messages
    txt_messages = customtkinter.CTkTextbox(master=main_menu, height=80, width=400)
    txt_messages.grid(row=3, column=1, pady=20)

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
    add_password_frame = customtkinter.CTkToplevel(main_menu)
    add_password_frame.title(f"Add Password for {ent_username.get()}")
    add_password_frame.geometry("400x270")
    add_password_frame.wm_transient(main_menu)

    lbl_addpasswordtitle = customtkinter.CTkLabel(master=add_password_frame, text="Add Password", font=customtkinter.CTkFont(size=20, weight="bold"))
    lbl_addpasswordtitle.pack(pady=15)

    lbl_address = customtkinter.CTkLabel(master=add_password_frame, text="Where will the password be stored?")
    lbl_address.pack(pady=5)

    global ent_address
    ent_address = customtkinter.CTkEntry(add_password_frame)
    ent_address.pack()

    lbl_password = customtkinter.CTkLabel(master=add_password_frame, text="Type the password:")
    lbl_password.pack(pady=10)
    
    global ent_password
    ent_password = customtkinter.CTkEntry(master=add_password_frame, show="*")
    ent_password.pack()

    btn_addpassword = customtkinter.CTkButton(master=add_password_frame, text="Add Password", command=append_new_password)
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

def sign_up():
    """Takes the user to a separate window, whether they can enter their credentials and create an account"""
    global signup_frame
    signup_frame = customtkinter.CTkToplevel(root)
    signup_frame.title("Sign Up Form")
    signup_frame.geometry("400x360")
    signup_frame.wm_transient(root)

    lbl_signuptitle = customtkinter.CTkLabel(master=signup_frame, text="Sign Up", font=customtkinter.CTkFont(size=20, weight="bold"))
    lbl_signuptitle.pack(pady=15)

    lbl_signupname = customtkinter.CTkLabel(master=signup_frame, text="Username")
    lbl_signupname.pack()

    global ent_signupname
    ent_signupname = customtkinter.CTkEntry(signup_frame)
    ent_signupname.pack()

    lbl_signuppassword = customtkinter.CTkLabel(master=signup_frame, text="Password")
    lbl_signuppassword.pack(pady=5)
    
    global ent_signuppassword
    ent_signuppassword = customtkinter.CTkEntry(master=signup_frame, show="*")
    ent_signuppassword.pack()
    
    lbl_signupconfirmpassword = customtkinter.CTkLabel(master=signup_frame, text="Confirm Password")
    lbl_signupconfirmpassword.pack(pady=5)

    global ent_signupconfirmpassword
    ent_signupconfirmpassword = customtkinter.CTkEntry(master=signup_frame, show="*")
    ent_signupconfirmpassword.pack()

    btn_createaccount = customtkinter.CTkButton(master=signup_frame, text="Create Account", command=check_signup)
    btn_createaccount.pack(pady=20)

    global txt_signupfailed
    txt_signupfailed = customtkinter.CTkTextbox(master=signup_frame, width=350, height=1)
    txt_signupfailed.pack()

def check_signup():
    """Only registers the new account if all entries have been filled, the selected username does not already exist, and the provided passwords match"""
    txt_signupfailed.delete("1.0", END)
    txt_loginfailed.delete("1.0", END)
    
    if ent_signupname.get() == "" or ent_signuppassword.get() == "":
        txt_signupfailed.insert(END, " SIGNUP FAILED: Please fill out all entries.")
    elif ent_signupname.get() in users.keys():
        txt_signupfailed.insert(END, " SIGNUP FAILED: Username already exists in database.")
    elif ent_signuppassword.get() != ent_signupconfirmpassword.get():
        txt_signupfailed.insert(END, " SIGNUP FAILED: Passwords do not match.")
    else:
        users[ent_signupname.get()] = ent_signuppassword.get()
        passwords[ent_signupname.get()] = {}

        with open("current_users.json", "w") as outfile:
            json.dump(users, outfile)

        with open("passwords.json", "w") as outfile:
            json.dump(passwords, outfile)

        signup_frame.withdraw()
        txt_loginfailed.insert(END, f"Account for {ent_signupname.get()} successfully registered!")

# Creates the initial login screen and gives it the desired width and height
root = customtkinter.CTk()
root.title("Password Manager")
root.geometry("550x515")

# Displays a "user icon" image (for aesthetics)
canvas = Canvas(master=root, width=100, height=90, highlightthickness=0, bg="#232323")
canvas.pack(pady=10)

user_icon = PhotoImage(file="Images/user_icon_v4.png")
canvas.create_image(-40,-40, anchor=NW, image=user_icon)

# Title of the program
lbl_title = customtkinter.CTkLabel(master=root, text="Password Manager", font=customtkinter.CTkFont(size=20, weight="bold"))
lbl_title.pack(pady=10)

# Description of what the user is supposed to do
lbl_login = customtkinter.CTkLabel(master=root, text="Log-In to your Account")
lbl_login.pack()

# Allows the user to input their registered username
lbl_username = customtkinter.CTkLabel(master=root, text="\nUsername:")
lbl_username.pack()

ent_username = customtkinter.CTkEntry(master=root)
ent_username.pack(pady=5)

# Allows the user to input their registered password
lbl_accesstoken = customtkinter.CTkLabel(master=root, text="\nPassword:")
lbl_accesstoken.pack()

ent_accesstoken = customtkinter.CTkEntry(master=root, show="*")
ent_accesstoken.pack(pady=5)

# When the button is clicked, the credentials are checked for whether they exist in the database
btn_login = customtkinter.CTkButton(master=root, text="Log In", command=check_login)
btn_login.pack(pady=20)

# The textbox in which the "login failure" message is ouputted
txt_loginfailed = customtkinter.CTkTextbox(master=root, height=1, width=400)
txt_loginfailed.pack(pady=5)

# Gives the user the options to register an account into the system
lbl_signup = customtkinter.CTkLabel(master=root, text="Don't have an account?")
lbl_signup.pack(pady=5)

btn_signup = customtkinter.CTkButton(master=root, text="Sign Up", command=sign_up)
btn_signup.pack()

root.mainloop()