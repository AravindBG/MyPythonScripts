# Introduction

Download a password protected pdf from the email attachment and convert the first page of the pdf in to an image. 

## Check list to work Mobile_Bill_Processor.py script

* This script will work only on Python 3. (Tested verion 3.6.8)
* Install the following Python packages using pip
    > $ pip install python-imap
    $ pip install pymupdf

* Create a folder in the Gmail with the filer to keep the emails which we are planning to download pdfs. Replace ***"Add the email folder here"*** in the ***Mobile_Bill_Processor.py*** with your Gmail folder name.
* Replace ***"Enter email id here"*** and ***"Enter app specific password here"*** in the ***Mobile_Bill_Processor.py*** with your email id and app specific password. Check [here](https://support.google.com/accounts/answer/185833?hl=en) for more information about google app specific password.
* Replace ***"Enter the path where you want to download the bill"*** and ***"Enter the python command with the correct path to execute the script"*** in the ***Mobile_Bill_Processor.py*** with correct path in your machine.
* Replace ***"Enter your pdf password here"*** in ***Pdf_Image.py*** with your pdf password.
* Replace ***"Enter the path where you want to download the bill"*** in ***Pdf_Image.py*** with correct path in your machine.

## Execute Script

> *#Pick the recent email from the Gmail folder, download the attached pdf, and convert the first page of pdf to image.*<br>
$ python Mobile_Bill_Processor.py

Using arguments

> *#Pick the last 5 emails from the Gmail folder.*<br>
$ python Mobile_Bill_Processor.py 5

### Customising pdf to Image converter (You can run this script individually if needed)
> *#Convert all the files in the downloaded folder.* <br>
$ python Pdf_Image.py 

Using arguments

> *#Convert first 2 pages of sample.pdf with a password 1234 to image.*<br>
$ python Pdf_Image.py sample.pdf 1234 2

> *#Convert sample.pdf with a password 1234 to image.*<br>
$ python Pdf_Image.py sample.pdf 1234

> *#To convert sample.pdf with a no password.*<br>
$ python Pdf_Image.py sample.pdf