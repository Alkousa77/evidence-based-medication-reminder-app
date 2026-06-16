import smtplib 
import os
from email.message import EmailMessage


class EmailService:



    @staticmethod
    def send_email(to, body):
        Email = os.getenv("EMAIL")
        Password = os.getenv("PASSWORD")
        
        msg = EmailMessage() #create empty email object 
        
        msg["From"] = Email
        msg["To"] = to
        msg["Subject"] = "Medication Adhernce Alert"
        
        msg.set_content(body) #set message content
        
        
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp: #connect to gmail server using tls port
            smtp.starttls()                               # connection encryption  tls
            smtp.login(Email, Password)                   # log into the email account  
            smtp.send_message(msg)                        #send message
            
            print("EMAIL SENT")