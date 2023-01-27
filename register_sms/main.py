from protocol import RegisterIG
from colorama import Fore,Style
from os import system,name
from sys import argv,exit



def p_green(string):
    print(Fore.GREEN+Style.BRIGHT+string+Fore.RESET+Style.RESET_ALL)

def p_red(string):
    print(Fore.RED+Style.BRIGHT+string+Fore.RESET+Style.RESET_ALL)

def p_white(string):
    print(Fore.WHITE+Style.BRIGHT+string+Fore.RESET+Style.RESET_ALL)



def clear():
    command = 'clear'#posix
    if name in ('nt', 'dos'):#if unix or posix
        command = 'cls'#unix
    system(command)



def main():


    try:
        p_white('Choose your phone with country code\n\n\nEXAMPLE --->(+3930040050003)')
        phone = input('')
        clear()
        p_white('Choose your Name and Surname\n\n\nEXAMPLE --->(Matteo Ischia)')
        name_surname = input('')
        clear()
        p_white('Choose your password')
        password = input('')
    except Exception:
        p_red('ERROR PARAMETERS!!!')





    obj   = RegisterIG(email=phone,first_name=name_surname,pasw=password)

    datas = obj.main()






if __name__ == '__main__':
    main()