import os
import sys
import logging

# Enabled logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)

FILECOUNTER = 0

def startsearch(path, ext):
    logging.debug('Starting search in path %s with extension %s', path, ext)
    logging.debug('----------------------------------- \n -----------------------------------')
    listfiles(path, ext)
    print('Total files found: ', FILECOUNTER)


# identify the files with extension in the current folder
def listfiles(path, ext):
    logging.debug('Listing files in path %s with extension %s', path, ext)
    logging.debug('----------------------------------- \n -----------------------------------')

    for filename in os.listdir(path):
        concat_path = os.path.join(path,filename)
        if os.path.isfile(concat_path):
            get_ext = filename.split('.')[-1]
            if get_ext.lower() == ext.lower():
                print('File path:', concat_path)
                global FILECOUNTER
                FILECOUNTER = FILECOUNTER + 1

        elif os.path.isdir(concat_path):
            logging.debug('Directory name: %s', concat_path)
            listfiles(concat_path, ext)




if len(sys.argv) == 3:
    # get the folder provided as the argument
    path = sys.argv[1]
    # get the extension of the file we need to search from the argument
    ext = sys.argv[2]
    startsearch(path,ext)

else:
    raise Exception('No valid arguments found')