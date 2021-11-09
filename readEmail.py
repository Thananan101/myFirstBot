#techgeekbuzz.com/how-to-read-emails-in-python/
import imaplib
import email

#credentials
username ="thananan_pi@kkumail.com"

#generated app password
app_password= "yhljrlhftfehlsvp"

# https://www.systoolsgroup.com/imap/
gmail_host= 'imap.gmail.com'

def getDBZoomLink():
  
    #set connection
    mail = imaplib.IMAP4_SSL(gmail_host)
    mail.login(username, app_password)

    mail.select("INBOX")

    #Search for keyword
    _, selected_mails = mail.search(None, '(SUBJECT "Database Systems class")')

    for num in selected_mails[0].split():

      _, data = mail.fetch(num , '(RFC822)')
      _, bytes_data = data[0]

    #convert the byte data to message
    email_message = email.message_from_bytes(bytes_data)
    print("\n===========================================")

    #access data
    i = False
    link = ''
    for part in email_message.walk():
        if part.get_content_type()=="text/plain" or part.get_content_type()     =="text/html":
          message = part.get_payload(decode=True)
          print("Message: \n", message.decode())
          for line in message.decode().splitlines():
              if i:
                print("here is the link:", line)
                i = False
                link = line
              if line == "Join Zoom Meeting":
                i = True

          print("==========================================\n")
          break
    return link