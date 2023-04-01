# Version 1: Basic Password Manager 

# Creating an empty dictionary to store account name and password
passwords = {}

# Using 3 functions for adding passwords to account and asking to get password from dictionary

def add_password(account, password):
    passwords[account] = password 

def get_password(account):
    return passwords.get(account, None) 

def main():
    while True:
        print("\n1. Add Password")
        print("2. Get Password")
        print("3. Exit") 
        
        choice = input("\nEnter your choice: ") 
    
        if choice == "1":
            account = input("\nEnter account name: ")
            password = input("Enter password: ")
            add_password(account, password)
        elif choice == "2":
            account = input("\nEnter account name: ")
            password = get_password(account)
            if password:
                print(f"Password for {account}: {password}")
            else:
                print(f"No password found for {account}")
        elif choice == "3":
            break
        else: print("Invalid choice") 
if __name__ == "__main__": 
    main()
## It Allows You to Execute Code When the File Runs as a Script,but Not When It's Imported as a Module. 
