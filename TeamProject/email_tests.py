import smtplib, ssl
context = ssl.create_default_context()
server = smtplib.SMTP("smtp.gmail.com",587)
server.ehlo()
server.starttls(context=context)
server.ehlo()
# Test credentials
server.login("testcasesg@gmail.com", "123456789Ou*")
#server.sendmail("testcasesg@gmail.com","ousamashami1999@gmail.com","hey, how are you")
#server.quit()

def sendemail(email_text,reciever):
    server.sendmail("testcasesg@gmail.com",reciever,email_text)
    print("sending an email with text : ",email_text,"to ",reciever)
    return True

