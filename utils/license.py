import hashlib
import os

from utils.settings import settings
from utils.misc import printm
from pydoc import pager
from sys import platform

async def check_license_agreement():
    h = hashlib.sha256()
    with open('LICENSE', 'rb') as file:
        chunk = file.read(1024)
        while chunk:
            h.update(chunk)
            chunk = file.read(1024)
    license_hash = h.hexdigest()
    if settings.license_agreement_accepted == False or settings.license_agreement_accepted == None:
        printm("You have to accept the license agreement before using this program.")
    elif settings.license_agreement_accepted == True:
        if settings.license_agreement_hash != license_hash:
            printm("The license agreement has been updated since you last accepted it. Please accept it again.")
        else:
            return True
    else:
        printm("There was an error with the license agreement. Please accept it again.")
    while True:
        printm('\n\n')
        inp = input("Type p to print the license agreement, a to accept it, q to quit the program or o to open the LICENSE in your default text editor: ")
        if inp == "p":
            input('You can use the "Enter" key to scroll down and the "q" key to quit the license agreement. Press "Enter" to continue.')
            with open('LICENSE', 'r', encoding='utf-8') as f:
                pager(f.read())
        elif inp == "a":
            settings.set_setting('license_agreement_accepted', True)
            settings.set_setting('license_agreement_hash', license_hash)
            if os.path.exists('LICENSE.txt'):
                os.remove('LICENSE.txt')
            printm("License agreement accepted.")
            return True
        elif inp == "q":
            printm("Quitting the program...")
            raise KeyboardInterrupt
        elif inp == "o":
            dict_os_commands = {
                "linux": "xdg-open",
                "win32": "start",
                "darwin": "open"
            }
            #copy the license file to a temporary txt file
            with open('LICENSE', 'r', encoding='utf-8') as f:
                with open('LICENSE.txt', 'w', encoding='utf-8') as f2:
                    f2.write(f.read())
            os.system(f"{dict_os_commands[platform]} LICENSE.txt")