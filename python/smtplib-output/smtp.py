import smtplib
from config import * # create it with variables `fromaddr`, `toaddr`, `login` and `server`

def prompt(prompt):
    return input(prompt).strip()

# Add the From: and To: headers at the start!
msg = ("From: %s\r\nTo: %s\r\n\r\n"
       % (fromaddr, ", ".join(toaddr)))
msg = msg + """hello"""
print("Message length is", len(msg))

server = smtplib.SMTP(server)
server.set_debuglevel(1)
#server.starttls()
server.login(*login)
server.sendmail(fromaddr, toaddr, msg)
server.quit()
