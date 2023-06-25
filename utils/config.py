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

loadingmessage = f"""{bcolors.OKGREEN}
   ▄████████    ▄████████ ▀█████████▄   ▄█          ▄████████ 
  ███    ███   ███    ███   ███    ███ ███         ███    ███ 
  ███    █▀    ███    ███   ███    ███ ███         ███    █▀  
 ▄███▄▄▄       ███    ███  ▄███▄▄▄██▀  ███        ▄███▄▄▄     
▀▀███▀▀▀     ▀███████████ ▀▀███▀▀▀██▄  ███       ▀▀███▀▀▀     
  ███          ███    ███   ███    ██▄ ███         ███    █▄  
  ███          ███    ███   ███    ███ ███▌    ▄   ███    ███ 
  ███          ███    █▀  ▄█████████▀  █████▄▄██   ██████████ 
                                       ▀                      
{bcolors.ENDC}{bcolors.OKBLUE}Film and Artistic Bot for Lively Entertainment{bcolors.ENDC}
{bcolors.OKCYAN}
Made with 💖 by: *@paillat-dev*
https://paillat.dev

Thanks to *@Code7G* for the suggestions!

Thanks to *ChatGPT* for the name suggestions!

{bcolors.ENDC}
"""

if __name__ == '__main__':
    print(loadingmessage)