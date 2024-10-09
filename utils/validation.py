def validate_registration(data):
    return 'username' in data and 'email' in data and 'password' in data

def validate_login(data):
    return 'email' in data and 'password' in data
