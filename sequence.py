
def get_main_sequences():
    sequences = {
        # "login_linkedIn": 'Login to LinkedIn',
        # "logout_linkedIn": 'Logout from LinkedIn',
        # "login_gmail": 'Login to Gmail',
        # "logout_gmail": 'Logout from Gmail',
        # "exit": "Exits the script"
        "one": 'Login to LinkedIn',
        # "three": 'Login to Gmail',
        "five": 'Login to Yahoo',
        # "eleven": "Import Contacts from Gmail",
        "twelve": "Import Contacts from yahoo",
        # "thirteen": "Import Contacts from AOL",
        "fifteen": "Export Contacts",
        "sixteen": "Delete Exported Contacts",
        # "four": 'Logout from Gmail',
        "six": 'Logout from Yahoo',
        "two": 'Logout from LinkedIn',
        "zero_exit": "Exits the script"
    }
    return sequences

def get_gamail_login_sequences():
    sequences = {
        "email_screen": 'Email Screen',
        "password_screen": 'Password Screen'
    }
    return sequences