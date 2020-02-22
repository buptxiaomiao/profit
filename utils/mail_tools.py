# coding: utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from settings import MAIL_USER, MAIL_PASSWORD, MAIL_SMTP_SERVER, MAIL_RECIEVERS


class MailTools(object):

    @classmethod
    def send_mail(cls, subject, content, _subtype='plain',  # html
                  mail_user=MAIL_USER,
                  mail_password=MAIL_PASSWORD,
                  mail_smtp_server=MAIL_SMTP_SERVER,
                  mail_recievers=MAIL_RECIEVERS):

        print mail_user, mail_password, mail_smtp_server, mail_recievers
        print subject
        # mail_user = ''
        # mail_password = ''
        # mail_smtp_server = ''
        # mail_recievers = ''

        msgroot = MIMEMultipart('related')
        msgroot['Subject'] = subject
        msgroot['to'] = ','.join(['%s<%s>' % (x, x) for x in mail_recievers.split(',')])
        msgroot['from'] = '%s<%s>' % (mail_user, mail_user)

        body = MIMEText(content, _subtype, 'utf-8')
        msgroot.attach(body)

        asmtp = smtplib.SMTP_SSL()
        asmtp.connect(mail_smtp_server)
        asmtp.login(mail_user, mail_password)
        asmtp.sendmail(mail_user, mail_recievers.split(','), msgroot.as_string())
        asmtp.quit()
        return


if __name__ == 'main':
    MailTools.send_mail('你好', '测试')
