
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


def get_selected_sequences(is_auto, payload):
    sequences = get_main_sequences()
    if is_auto:
        selected_sequences = sequences
    else:
        payload_sequences = payload.get('steps')
        selected_sequences = []
        selected_email_sequences = []
        for seq in payload_sequences:
            if seq in sequences.get('email_operation'):
                if not 'email_operation' in selected_sequences:
                    selected_sequences.append('email_operation')
                selected_email_sequences.append(seq)
            else:
                selected_sequences.append(seq)
    return selected_sequences


def get_selected_email_sequences(is_auto, payload, email_provider, email_id):
    sequences = []
    if is_auto:
        selected_email_sequences = get_email_operation_sequences()
    else:
        payload_sequences = payload.get('steps')
        selected_email_sequences = []
        for seq in payload_sequences:
            if seq in get_email_operation_sequences():
                selected_email_sequences.append(seq)
    for eseq in selected_email_sequences:
        key_name = str(eseq) + "_" + email_provider +"_" + email_id.replace('.', '').replace('@', '')
        seq1 = {'key': key_name, 'title': get_email_operation_sequences().get(eseq)}
        sequences.append(seq1)
    return sequences



def get_main_sequence_tree(is_auto, payload, email_id):
    selected_sequences = get_selected_sequences(is_auto, payload)
    sequences = get_main_sequences()
    new_seq = []
    for sequence in selected_sequences:
        sequence_title = sequences[sequence]
        if not isinstance(sequence_title, dict):
            key_name = str(sequence)+"_"+email_id.replace('.', '').replace('@', '')
            seq = {'key': key_name, 'title': sequence_title}
            new_seq.append(seq)
    return new_seq


def generate_sequence_tree(is_auto, payload, config_accounts):
    sequence_tree = []
    #main_sequences = get_main_sequence_tree(is_auto, payload)
    #email_sequences = get_selected_email_sequences(is_auto, payload)
    for account in config_accounts:
        main_sequences = get_main_sequence_tree(is_auto, payload, account.get("linkedIn").get("username"))
        account['linkedIn']['sequences'] = main_sequences
        for email_provider in account.get('email'):
            provider = account.get('email').get(email_provider)
            for email_account in provider:
                email_sequences = get_selected_email_sequences(is_auto, payload, email_provider, email_account.get("username"))
                email_account['sequences'] = email_sequences
        sequence_tree.append(account)
    return sequence_tree

