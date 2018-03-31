import threading
class EmailThread(threading.Thread):
    def __init__(self, email, subject, body):
        threading.Thread.__init__(self)
        self.email = email
        self.subject = subject
        self.body = body

    def run(self):
        try:
            username = ""
            password = ""
            SMTP_SERVER = ""
	    SMTP_SERVER_PORT = 0 

            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from email.header import Header

            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
            me = username
            you = self.email
            mail_body = str(self.body)
            mail_body = "<br />".join(mail_body.split("\n"))
            #msg = MIMEText(mail_body.encode('utf-8'), 'plain', 'utf-8')
            msg = MIMEMultipart('alternative')
            #msg['Subject'] = self.subject
            msg['Subject'] = Header(self.subject, 'utf-8')
            msg['From'] = me
            msg['To'] = you
            html = """<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8"> <!-- utf-8 works for most cases -->
		<meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
		<meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
		
		<title>Second solution</title> <!-- The title tag shows in email notifications, like Android 4.4. -->
	</head>
	<body>
	    <p>%s</p>	
	</body>
</html>""" % mail_body
            #part1 = MIMEText(mail_body.encode('utf-8'), 'plain', 'utf-8')
            part2 = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
            
            #msg.attach(part1)
            msg.attach(part2)
            try:
                SMTP_SERVER = str(SMTP_SERVER)
                server = smtplib.SMTP(SMTP_SERVER, SMTP_SERVER_PORT)
                server.ehlo()
                server.starttls()
                server.login(username, password)
                try:
                    server.sendmail(me, you, msg.as_string())
                    print "Mail sent successfully."
                except Exception, e:
                    print "Exception during mail send: " + str(e)
                server.quit()
            except:
                print "Invalid smtp server configuration"
        except:
            print  "Unable to send email"

def send_email(email, subject, body):
    print "sending email"
    status = True
    message = "Successfully email send"
    
    email_thread = EmailThread(email, subject, body)
    email_thread.start()
    return status, message

