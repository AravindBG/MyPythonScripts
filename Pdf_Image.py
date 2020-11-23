import os
import sys
import logging
import fitz
import Sys_Notification

# Enabled logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.CRITICAL)


# Create a folder in your machine to download the pdf documents

# os.chdir('/Users/aravindb/Documents/Mobile_bill/')
os.chdir('Enter the path where you want to download the bill')


# args input filename, password, number of pages

# Number of pages in the pdf

def createimagefromdoc(inputfilename, doc, numofpages):
    pageIndex = 1
    totalPages = int(numofpages)
    for page in doc:
        image_matrix = fitz.Matrix(fitz.Identity)
        image_matrix.preScale(2, 2)
        pix = page.getPixmap(alpha = False, matrix=image_matrix)
        filename = inputfilename.split('.')[-1]
        output = filename + '-image-Page-' + str(pageIndex) + ".png"
        filepath = os.path.join(os.getcwd(), 'Output', output)
        pix.writePNG(str(filepath))
        # Exit when the number of pages required matches the page index.
        if pageIndex == totalPages:
            break
        pageIndex = pageIndex + 1

    Sys_Notification.notifyuser("Success", "Images generated")


# Create image from the pdf document

def processimagesfromPDF(inputfilename, password, numofpages):
    logging.debug('File name %s' % (inputfilename))
    if 'pdf' not in inputfilename.upper().lower():
        return

    filePath = os.path.join(os.getcwd(), inputfilename)
    if not os.path.isfile(filePath):
        Sys_Notification.notifyuser('Error', inputfilename + ' does not exist')
        return

    # Open the PDF
    try:
        doc = fitz.open(inputfilename)
        # authenticate if necessary
        if doc.needsPass:
            doc.authenticate(password)

        createimagefromdoc(inputfilename, doc, numofpages)

    except Exception as e:
        Sys_Notification.notifyuser('Error', 'Unable to open the file')


# Iterate all the files in the root folder

def createimagesforallPDFs():
    rootFolder = os.getcwd()
    outputFolder = os.path.join(rootFolder, 'Output')
    if not os.path.isdir(outputFolder):
        os.makedirs(outputFolder)

    for fileName in os.listdir(rootFolder):
        if not os.path.isfile(os.path.join(rootFolder, fileName)):
            continue

        # Enter the PDF password below.
        processimagesfromPDF(fileName, "Enter your pdf password here", 1)


if len(sys.argv) == 4:
    pdffile = sys.argv[1]
    password = sys.argv[2]
    numberofpages = sys.argv[3]

    processimagesfromPDF(pdffile, password, numberofpages)

elif len(sys.argv) == 3:
    pdffile = sys.argv[1]
    password = sys.argv[2]

    processimagesfromPDF(pdffile, password, -1)

elif len(sys.argv) == 2:
    pdffile = sys.argv[1]

    processimagesfromPDF(pdffile, "", -1)

elif len(sys.argv) == 1:
    createimagesforallPDFs()
