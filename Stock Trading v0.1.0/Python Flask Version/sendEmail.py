import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendConfirmationEmail(sender, receiver, htmlTemplate):
      server = smtplib.SMTP(host="smtp-mail.outlook.com", port=587)
      server.starttls()
      server.login("betastockinvestment@outlook.com", "Pk123456")
      
      # Creation of the MIMEMultipart Object
      message = MIMEMultipart("alternative")
      message['From'] = sender
      message['To'] = receiver
      message['Subject'] = "BetaStock - Confirmation Email"
      
      # HTML Setup
      html = htmlTemplate
      htmlPart = MIMEText(html, 'html')
      message.attach(htmlPart)
      server.send_message(message)
      server.quit()