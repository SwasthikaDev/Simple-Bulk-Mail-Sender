import smtplib
import datetime as dt
import time
from email.mime.text import MIMEText
import json
import docx
import openpyxl
import pandas as pd

'''Read the doc file'''


def readtxt(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def sendMail():
    path = "userDetails.xlsx"
    df = pd.read_excel(path)
    names = df.NAME
    email = df.EMAIL
    index = 0
    for i in range(3):

        email_user = "4nm18cs199@nmamit.in"  # email id

        nameString = names[index]
        emailIdString = email[index]
        index += 1

        msg = MIMEText("Hi " + nameString +
                       "\n" + readtxt('template.docx'))

        msg['From'] = email_user
        msg['To'] = emailIdString
        msg['Subject'] = "Template! mail"
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # generate password and attach -> keep 2FA on and generate app password and paste here!
        server.login(email_user, 'vvczscozlfuhebas')
        server.sendmail(email_user, emailIdString, text)
        server.quit()
        # set your sending time in UTC
        #send_time = dt.datetime(2023, 4, 13, 3, 55, 0, 0)
        #time.sleep(send_time.timestamp() - time.time())


if __name__ == "__main__":
    sendMail()
