import smtplib, ssl
context = ssl.create_default_context()
server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls(context=context)
server.ehlo()
# Test credentials
server.login("testcasesg@gmail.com", "123456789Ou*")


def send_email(subject, email_text, receiver):
    """
    Function that sends an email given a provided recipient and text
    :param email_text: the message to be sent to the user
    :param receiver: the email of the recipient
    :return: True when done
    """
    text =  f"Subject:{subject}\n\n{email_text}"
    server.sendmail("testcasesg@gmail.com", receiver, text)
    print("sending an email with text : ", email_text, "to: ", receiver)
    return True
