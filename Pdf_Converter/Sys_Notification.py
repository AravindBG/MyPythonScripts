import os
import logging
import platform

# Enabled logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)

def notifyuser(title, message):
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
