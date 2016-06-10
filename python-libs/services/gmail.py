import smtplib

class Gmail:
    def __init__(self,user,password):
        self._from = user

        self._server = smtplib.SMTP("smtp.gmail.com", 587)
        self._server.ehlo()
        self._server.starttls()
        self._server.login(user, password)
    
    def send(self, to, subject, content):
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (self._from, ", ".join(to), subject,content)
        self._server.sendmail(self._from, to, message)
        
    def destroy(self):
        self._server.close()
