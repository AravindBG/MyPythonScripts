
import imaplib
import os
import email
import logging
import sys
import Sys_Notification

# Enabled logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.CRITICAL)
# os.chdir('/Users/aravindb/Documents/Mobile_bill/')
os.chdir('Enter the path where you want to download the bill')

mail = imaplib.IMAP4_SSL('imap.gmail.com',993)
mail.login('Enter email id here','Enter app specific password here')
# Add the email folder here
mail.select('Add the email folder here')
type, data = mail.search(None, 'ALL')
print(type)
mail_ids = data[0]
id_list = mail_ids.split()

attachments_to_be_downlaoded = 1

if len(sys.argv) == 2:
    attachments_to_be_downlaoded = int(sys.argv[1])


# Attachments will be dowloaded from the emails by the order of recent email first.

num_emails_read = 0

for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)' )
    raw_email = data[0][1]# converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)# downloading attachments
    if num_emails_read == attachments_to_be_downlaoded:
        break
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        # Check if the file name extension is PDF
        file_name_parts = fileName.split('.')
        ext = file_name_parts[-1]
        
        # logging.debug('File name %s' % (fileName))
        # logging.debug('File name parts %s' % (file_name_parts))
        # logging.debug('Extension %s', ext.lower())

        if ext.lower() != 'pdf':
            continue

        if bool(fileName):
            logging.debug(os.getcwd())
            filePath = os.path.join(os.getcwd(), fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
            log_message = 'Downloaded "{file}" from email titled "{subject}".'.format(file=fileName, subject=subject)
            Sys_Notification.notifyuser('Success', 'Pdf attachments downloaded')
            logging.debug(log_message)
            num_emails_read = num_emails_read + 1
            # Add the correct path of the files in your machine.
            # exec_command = 'python3 /Users/aravindb/Documents/GitHub/PrivatePythonScripts/Pdf_Image.py'
            exec_command = 'Enter the python command with the correct path to execute the script'
            # print(exec_command)
            os.system(exec_command)
            break
    