import os

import smtplib

from datetime import datetime

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


def get_newest_file(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)


def send_email(fromaddr, password, toaddr):
    message = MIMEMultipart()

    message['From'] = fromaddr
    message['To'] = toaddr
    message['Subject'] = 'Face detected'

    now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    body = 'This face was detected on camera at {}.'.format(now)

    message.attach(MIMEText(body, 'plain'))

    attachment = open(get_newest_file('history'), 'rb')
    filename = 'face_detected.jpg'

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)

    message.attach(part)
    print 'Sending email to {}'.format(toaddr)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = message.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    print 'E-mail sent to to {}.'.format(toaddr)


if __name__ == '__main__':
    pass
