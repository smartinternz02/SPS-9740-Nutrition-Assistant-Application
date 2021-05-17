import smtplib
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

from sendgrid import SendGridAPIClient


SUBJECT = "Prajwal's Nutrition Assistant"
s = smtplib.SMTP('smtp.gmail.com', 587)
TEMPLATE_ID = 'TEMPLATE ID'

def sendgridmail(user,TEXT,CONTACT,VALUE):
    sg = sendgrid.SendGridAPIClient('API')
    from_email = Email("EMAIL")  # Change to your verified sender
    to_email = To(user)  # Change to your recipient
    subject = "Prajwal's Nutrition Assistant"
    #content=Content("text/plain",TEXT,content)
    
    mail = Mail(from_email, to_email, subject)
    mail.dynamic_template_data = { 'TEXT': TEXT ,'Content' :CONTACT,'value':VALUE}
    mail.template_id = TEMPLATE_ID
    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()
    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    
    print("wait we are processing your candidature")
    print(response.status_code)
    print(response.headers)
