
import imaplib
import os
import email
import logging
import sys
import Sys_Notification
import Pdf_Image
import re
from datetime import datetime


# Enabled logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.CRITICAL)

directory = os.path.join(os.getcwd(), 'Mobile_bill')

if not os.path.isdir(directory):
    os.mkdir(directory)

def sort_email_list(emails):
    #subject = 'Fwd: Your Airtel Mobile Bill for 78997XXXXX for 12-11-2020 is ready to view'
    dateregex = re.compile(r'''
    \s                  # Space 
    [0-3]{1}[0-9]{1}    # Date: 2 digit number first digit 0-3 2nd 0-9
    -                   # hypen
    [0-1]{1}[0-9]{1}    # Month: 2 digit number first digit 0-1 2nd 0-9
    -                   # hypen
    [0-9]{4}            # Year
    \s                  # Space
    ''', re.VERBOSE)

    date_list = []
    for email_data in emails:
        sub = str(email_data).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
        # print('Subject :' + subject)

        datetime_str = dateregex.findall(sub)
        # print(datetime_str)
        if len(datetime_str) >= 1:
            date = datetime_str[0].strip()
            datetime_object = datetime.strptime(date, '%d-%m-%Y')
            # print(date)
            # print(datetime_object)
            date_list.append((email_data, datetime_object))

    sort_tup_list = sorted(date_list, key = lambda x: x[1], reverse=True)
    sorted_emails_filter = [tup[0] for tup in sort_tup_list]
    return sorted_emails_filter


mail = imaplib.IMAP4_SSL('imap.gmail.com',993)
mail.login('#Enter your email id here','#Enter your app secret password here')
mail.select('#Email folder')
type, data = mail.search(None, 'ALL')
mail_ids = data[0]
id_list = mail_ids.split()

attachments_to_be_downlaoded = 1

if len(sys.argv) == 2:
    attachments_to_be_downlaoded = int(sys.argv[1])

# Attachments will be dowloaded from the emails by the order of recent email first.

num_emails_read = 0
email_list = []

for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)' )
    raw_email = data[0][1]# converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)# downloading attachments
    email_list.append(email_message)

# print(len(email_list))
sorted_emails = sort_email_list(email_list)
# print(len(sorted_emails))

for email in sorted_emails:
    if num_emails_read == attachments_to_be_downlaoded:
        break
    for part in email.walk():
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
            logging.debug(directory)
            filePath = os.path.join(directory, fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
            log_message = 'Downloaded "{file}" from email titled "{subject}".'.format(file=fileName, subject=subject)
            Sys_Notification.notifyuser('Success', 'Pdf attachments downloaded')
            logging.debug(log_message)
            num_emails_read = num_emails_read + 1
            # Add the password and number of pages params in the method params.
            # print(filePath)
            Pdf_Image.processimagesfromPDF(fileName, 'Enter the pdf password', "Enter number of pages")
            break