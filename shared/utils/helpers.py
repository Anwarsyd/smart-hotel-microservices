import string, random

def generate_reference(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
