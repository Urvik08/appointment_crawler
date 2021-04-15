import base64
import os
import smtplib

from twilio.rest import Client


# Mac Notification
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


def send_text(title, text):
    client = Client("", "")
    body = title + "\n" + text
    client.messages.create(to="whatsapp:",
                           from_="whatsapp:",
                           body=body)


def email_to_user(title, text):
    # Try to log in to server and send email
    # ssl.create_default_context()
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = ""
    receiver_email = ""
    password = base64.b64decode("")
    try:

        print("setting up smtp server now")
        server = smtplib.SMTP(smtp_server, port)
        print("server.ehlo()")
        server.ehlo()
        print("establishing ttls")
        server.starttls()
        print("logging in")
        server.login(sender_email, password)
        message = title + '.' + text
        print("sending email")
        server.sendmail(sender_email, receiver_email, message)
    except Exception as ex:
        print("exception caught while trying to send email: {}".format(str(ex)))
