import os
import yaml

clear_screen = lambda: os.system('cls' if os.name == 'nt' else 'clear')
open_explorer_here = lambda path: os.system(f'explorer.exe "{path}"' if os.name == 'nt' else f'open "{path}"')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class realbcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printm(*args, **kwargs):
    result = ''
    underline_counter = 0
    bold_counter = 0
    sep = kwargs.get('sep', ' ')
    text = sep.join([str(arg) for arg in args])
    i = 0
    while i < len(text):
        if text[i:].startswith('$***'):
            result += text[i:i+4].replace('$', '')
            i += 4
            continue
        elif text[i:].startswith('$**'):
            result += text[i:i+3].replace('$', '')
            i += 3
            continue
        elif text[i:].startswith('$*'):
            result += text[i:i+2].replace('$', '')
            i += 2
            continue
        elif text[i:].startswith('***'):
            if bold_counter % 2 == 0 and underline_counter % 2 == 0:
                result += bcolors.BOLD + bcolors.UNDERLINE
            elif bold_counter % 2 == 0:
                result += bcolors.BOLD
            elif underline_counter % 2 == 0:
                result += bcolors.UNDERLINE
            else:
                result += bcolors.ENDC
            i += 3
            bold_counter += 1
            underline_counter += 1
            continue
        elif text[i:].startswith('**'):
            if bold_counter % 2 == 0:
                result += bcolors.BOLD
            else:
                result += bcolors.ENDC
            i += 2
            bold_counter += 1
            continue
        elif text[i:].startswith('*'):
            if underline_counter % 2 == 0:
                result += bcolors.UNDERLINE
            else:
                result += bcolors.ENDC
            i += 1
            underline_counter += 1
            continue

        result += text[i]
        i += 1

    result += bcolors.ENDC  # Ensure the formatting is reset at the end

    print(text, **kwargs)

def getenv(var, default=None):
    with open('env.yaml', 'r') as f:
        env = yaml.safe_load(f)
    return env.get(var, default)
