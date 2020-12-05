import smtplib, ssl
context = ssl.create_default_context()
server = smtplib.SMTP("smtp.gmail.com",587)
server.ehlo()
server.starttls(context=context)
server.ehlo()
# Test credentials
server.login("testcasesg@gmail.com", "123456789Ou*")
subject=" WELCOME TO EVAGED-Api key"
txt="Hey thank you for signing up with Evaged here is your api key"
email_text= f"Subject:{subject}\n\n{txt}"
server.sendmail("testcasesg@gmail.com","ousama_shami@hotmail.com",email_text)
server.quit()

#def sendemail(email_text,reciever):
 #   server.sendmail("testcasesg@gmail.com",reciever,email_text)
  #  print("sending an email with text : ",email_text,"to ",reciever)
   # return True

