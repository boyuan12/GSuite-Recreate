import string
import random

def validate_password(password):
    """
    8 - 20 characters
    at least 1 lowercase letter
    at least 1 uppercase letter
    at least 1 number
    at least 1 special character
    """

    def check_str_in_str(s1, s2):
        passed = False
        for i in string.digits:
            for j in password:
                if i == j:
                    passed = True
                    break

        if passed != True:
            return False


    if len(password) > 20 or len(password) < 8:
        return False

    if check_str_in_str(password, string.ascii_lowercase) == False:
        return False

    if check_str_in_str(password, string.ascii_uppercase) == False:
        return False

    if check_str_in_str(password, string.digits) == False:
        return False

    if check_str_in_str(password, string.punctuation) == False:
        return False

    return True


def random_str(n=6):
    return "".join([random.choice(string.digits) for i in range(n)])

