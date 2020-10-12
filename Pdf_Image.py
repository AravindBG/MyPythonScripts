#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import os
import fitz
import sys
import platform
import logging

# Enabled logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)

os.chdir('Enter root folder')

# args input filename, password, number of pages


def notifyUser(title, message):
    plt = platform.system()

    if plt == 'Darwin':
        command = f'''
	    osascript -e 'display notification "{message}" with title "{title}"'
	    '''
    elif plt == 'Linux':
        command = f'''
            	notify-send "{title}" "{message}"
            	'''
    else:
        logging.debug('Unable to get the Platform')
        return

    os.system(command)


# Number of pages in the pdf

def createimagefromdoc(inputfilename, doc, numofpages):
    pageIndex = 1
    totalPages = int(numofpages)
    for page in doc:
        image_matrix = fitz.Matrix(fitz.Identity)
        image_matrix.preScale(2, 2)
        pix = page.getPixmap(alpha = False, matrix=image_matrix)
        output = inputfilename + '-image-Page-' + str(pageIndex) + ".png"
        filepath = os.path.join(os.getcwd(), 'Output', output)
        pix.writePNG(str(filepath))
        # Exit when the number of pages required matches the page index.
        if pageIndex == totalPages:
            break
        pageIndex = pageIndex + 1

    notifyUser("Success", "Images generated")


# Create image from the pdf document

def processimagesfromPDF(inputfilename, password, numofpages):
    logging.debug('File name %s' % (inputfilename))

    if 'pdf' not in inputfilename.upper().lower():
        return

    filePath = os.path.join(os.getcwd(), inputfilename)
    if not os.path.isfile(filePath):
        notifyUser('Error', inputfilename + ' does not exist')
        return

    # Open the PDF
    try:
        doc = fitz.open(inputfilename)
        # authenticate if necessary
        if doc.needsPass:
            doc.authenticate(password)

        createimagefromdoc(inputfilename, doc, numofpages)

    except Exception as e:
        notifyUser('Error', 'Unable to open the file')


# Iterate all the files in the root folder

def createimagesforallPDFs():
    rootFolder = os.getcwd()
    outputFolder = os.path.join(rootFolder, 'Output')
    if not os.path.isdir(outputFolder):
        os.makedirs(outputFolder)

    for fileName in os.listdir(rootFolder):
        if not os.path.isfile(os.path.join(rootFolder, fileName)):
            continue

        processimagesfromPDF(fileName, "mdm3", 1)


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
