from flask import render_template, redirect, url_for, session, Blueprint
from sqlalchemy.orm import sessionmaker
from database import engine, User
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import secrets, string


auth_bp = Blueprint('auth', __name__)

# Connect to database via SQLAlchemy
Session = sessionmaker(bind=engine)

# temporary set until i setup databsae


def generateRandomString():
    Vtoken = string.ascii_letters + string.digits
    return ''.join(secrets.choice(Vtoken) for _ in range(10))

def checkUniqueness(checkThisString, tempUsedStringSet):
    return checkThisString not in tempUsedStringSet

def generateUserVtoken(tempUsedStringSet):
    while True:
        userVtoken = generateRandomString()
        if checkUniqueness(userVtoken, tempUsedStringSet):
            return userVtoken

tempUsedStringSet = set()

def sendEmail(TO_EMAIL):
    HOST = "smtp-mail.outlook.com"
    PORT = 587


    #getpass.getpass("Enter Password: ")
    TO_EMAIL = "mquino57@nmsu.edu"

    MESSAGE = MIMEMultipart("alternative")
    MESSAGE['Subject'] = "Mail Sent using python for in lab Demo"
    MESSAGE['From'] = FROM_EMAIL
    MESSAGE['To'] = TO_EMAIL
    MESSAGE['Cc'] = FROM_EMAIL
    MESSAGE['Bcc'] = FROM_EMAIL

    userVtoken = generateUserVtoken(tempUsedStringSet)

    html_content = f"<p>Your verification code is: {userVtoken}</p>"
    html_part = MIMEText(html_content, 'html')

    MESSAGE.attach(html_part)


    smtp = smtplib.SMTP(HOST, PORT)

    status_code, response = smtp.ehlo()
    print(f"[*] Echoing the server: {status_code} {response}")

    status_code, response = smtp.starttls()
    print(f"[*] Starting TLS connection: {status_code} {response}")

    status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
    print(f"[*] Logging in: {status_code} {response}")

    smtp.sendmail(FROM_EMAIL, TO_EMAIL, MESSAGE.as_string())
    smtp.quit()
    return userVtoken

#sendEmail()

'''
@auth_bp.route('/auth', methods=['GET','POST'])
def auth():
   print("hello") 
'''
