
def get_main_sequences():
    sequences = {
        "linkedIn_login": 'Login to LinkedIn',
        "email_operation": get_email_operation_sequences(),
        "linkedIn_logout": 'Logout LinkedIn'
    }
    return sequences

def get_email_operation_sequences():
    sequences = {
        "email_login": 'Email Login',
        "import_contacts": 'Import Contacts From Email Account',
        "export_contacts": 'Export Contacts From LinkedIn',
        "delete_contacts": 'Delete Exported Contacts',
        "email_logout": 'Email Logout',
    }
    return sequences