import smtplib
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

from sendgrid import SendGridAPIClient


SUBJECT = "Prajwal's Nutrition Assistant"
s = smtplib.SMTP('smtp.gmail.com', 587)
TEMPLATE_ID = 'Templet id'

def sendgridmail(user,TEXT,CONTACT,VALUE):
    sg = sendgrid.SendGridAPIClient('API key')
    from_email = Email("Mail id")

    to_email = To(user)
    subject = "Prajwal's Nutrition Assistant"
    #content=Content("text/plain",TEXT,content)

    mail = Mail(from_email, to_email, subject)
    mail.dynamic_template_data = { 'TEXT': TEXT ,'Content' :CONTACT,'value':VALUE}
    mail.reply_to = "Mail id"
    mail.template_id = TEMPLATE_ID
    mail_json = mail.get()
    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    
    print("wait we are processing your candidature")
    print(response.status_code)
    print(response.headers)
