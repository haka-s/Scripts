import email, smtplib, os, time, fnmatch
from datetime import date, timedelta
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def sendMailTo(recepient_id):

    login_id = '-'
    login_pwd = '-'
    fro_ = login_id
    s_name = 'smtp.gmail.com'
    s_port = 587

  

    fileList = []
    fi_type = '*.log'
    file_path = "./logs"

    srvr = smtplib.SMTP(s_name, s_port)
    srvr.ehlo()
    srvr.starttls()
    srvr.ehlo()
    srvr.login(login_id, login_pwd)

    sub = "error"
      # loading MIMEMultipart obj onto outer var
    outer = MIMEMultipart('alternative')
    outer["From"] = 'COTI'
    outer["To"] = recepient_id 
    outer['Subject'] = sub
    outer['Message'] = 'error at:'

      # storing only pdf files          
    fileList = fnmatch.filter(os.listdir(file_path), fi_type)

    for fi in fileList:
        fi_name = os.path.join(file_path, fi)
        fp = open(fi_name, 'rb')
        img = MIMEImage(fp.read(), _subtype='jpg')
        fp.close()
        img.add_header('Content-disposition', "attachment", filename = fi)
        outer.attach(img)

      #start sending email with attachment with original file name
    srvr.sendmail(fro_, recepient_id, outer.as_string())

    part = None
    outer = None
    srvr.quit()