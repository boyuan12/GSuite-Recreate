import string
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


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


def random_str(n=6, alpha=False):
    if alpha == True:
        return "".join([random.choice(string.digits) + random.choice(string.ascii_letters) for i in range(n)])
    return "".join([random.choice(string.digits) for i in range(n)])


def send_mail(receiver, subject, message):

    me = "boyuan@boyuan12.me"
    my_password = os.getenv("EMAIL_PASSWORD")
    you = receiver

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    html = message
    part2 = MIMEText(html, 'html')

    msg.attach(part2)

    # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
    s = smtplib.SMTP_SSL('mail.privateemail.com')
    # uncomment if interested in the actual smtp conversation
    # s.set_debuglevel(1)
    # do the smtp auth; sends ehlo if it hasn't been sent already
    s.login(me, my_password)

    s.sendmail(me, you, msg.as_string())
    s.quit()

# send_mail("boyuan@boyuan12.me", "Hello!", "<h1>Hello!</h1>")