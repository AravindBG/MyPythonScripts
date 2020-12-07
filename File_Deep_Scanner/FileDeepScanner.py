import os
import sys
import logging
from shutil import copyfile
import Sys_Notification

# Enabled logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)

FILECOUNTER = 0

def copyfiles(currentpath, filename, ext, copypath, fileObj):
    logging.debug('')
    if not os.path.isdir(copypath):
        logging.debug('Directory created')
        os.mkdir(copypath)

    filefolderpath = os.path.join(copypath,ext.upper())
    if not os.path.isdir(filefolderpath):
        logging.debug('Sub directory created')
        os.mkdir(filefolderpath)
    size_bytes = os.path.getsize(currentpath)
    size_mb = size_bytes/(1024*1024)
    filemsg = '{currentpath} *** {size_mb: .2f} MB ***.'.format(currentpath = currentpath, size_mb = size_mb)
    fileObj.write(filemsg + '\n')

    copyfile(currentpath, os.path.join(filefolderpath,filename))


def startsearch(path, extens, copyfolder, fileObj):
    logging.debug('Starting search in path %s with extension %s', path, ','.join(extens))
    logging.debug('----------------------------------- \n -----------------------------------')
    listfiles(path, extens, copyfolder, fileObj)
    print('Total files found: ', FILECOUNTER)


# identify the files with extension in the current folder
def listfiles(path, extens, copyfolder, fileObj):
    logging.debug('Listing files in path %s with extension %s', path, ','.join(extens))
    logging.debug('----------------------------------- \n -----------------------------------')

    for filename in os.listdir(path):
        concat_path = os.path.join(path,filename)
        if os.path.isfile(concat_path):
            get_ext = filename.split('.')[-1]
            if get_ext.upper().lower() in extens:
                print('File path:', concat_path)
                global FILECOUNTER
                FILECOUNTER = FILECOUNTER + 1
                copyfiles(concat_path, filename, get_ext, copyfolder, fileObj)
                
        elif os.path.isdir(concat_path):
            # logging.debug('Directory name: %s', concat_path)
            listfiles(concat_path, extens, copyfolder, fileObj)
            

if len(sys.argv) == 4:
    # get the folder provided as the argument
    path = sys.argv[1]
    copyfolder = sys.argv[2]
    # get the extension of the file we need to search from the argument
    exts = sys.argv[3].split(',')
    extens = list(map(lambda x: str(x).strip().lower(), exts))

    if not os.path.isdir(copyfolder):
        logging.debug('Directory created')
        os.mkdir(copyfolder)

    namefile = open(os.path.join(copyfolder,'CopyFilePaths.txt'), 'a')
    namefile.write('\n')
    startsearch(path,extens,copyfolder, namefile)
    namefile.close()

    msg = '{filecount} files have been copied to new location.'.format(filecount = FILECOUNTER)
    Sys_Notification.notifyuser('Task Completed', msg)

else:
    raise Exception('No valid arguments found')