import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

def send_email(email, subject, message, filename=""):

    msg = MIMEMultipart()
    msg['From'] = 'py_project_rpoop@outlook.com'
    msg['To'] = email
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))

    if filename != "":
        ## ATTACHMENT PART OF THE CODE IS HERE
        attachment = open(filename, 'rb')
        part = MIMEBase('application', "octet-stream")
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)  
    server.ehlo()  # mail transfer protocol
    server.starttls() # enform  emial server email client want upgrade
    server.ehlo()
    server.login('py_project_rpoop@outlook.com', 'harshvitonde22@gmail.com')  ### if applicable
    server.send_message(msg)
    server.quit()