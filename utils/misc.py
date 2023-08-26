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

def replace_markdown_bold(text):
    splitted = text.split('**')
    #add bold after even occurences of ** and add endc after odd occurences. But attention, sometimes the string has nothing in
def printm(*args, **kwargs):
    sep = kwargs.get('sep', ' ')
    text = sep.join([str(arg) for arg in args])
    #bold processing
    print(text, **kwargs)

def getenv(var, default=None):
    with open('env.yaml', 'r') as f:
        env = yaml.safe_load(f)
    return env.get(var, default)
