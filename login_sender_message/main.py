from protocol.protocol import INSTA_SENDER_DM
from colorama import Fore,Back,Style
from os import system,name
from sys import argv,exit
from time import sleep


"""Main function to call the objects"""



def clear():
    command = 'clear'
    if name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    system(command)


def p_green(string):
    print(Fore.GREEN+Style.BRIGHT+string+Fore.RESET+Style.RESET_ALL)

def p_red(string):
    print(Fore.RED+Style.BRIGHT+string+Fore.RESET+Style.RESET_ALL)

def p_white(string):
    print(Fore.WHITE+Style.BRIGHT+string+Fore.RESET+Style.RESET_ALL)

def main():

    try:
        p_white('Choose your private username')
        cred1 = input('')
        clear()
        p_white('Choose your password')
        cred2 = input('')
        clear()
        p_white('Select your target username\n\n\nREMEMBER THAT IS THE @')
        target = input('')
        clear()
        p_white('Choose the massege')
        message = input('')
        clear()
    except Exception:
        p_red('ERROR PARAMETERS!!!')


    p_green('SENDING WITH CREDENTIALS {}:{} TO TARGET {}\n\n\nMESSAGE:\n\n{}\n\n\n'.format(cred1,cred2,target,message))

    obj = INSTA_SENDER_DM(username=cred1,password=cred2,target_user=target)
    ret = obj.main(message)
    
    if ret[0] == True:
        p_green('SENT MESSAGE TO {}'.format(target))
    if ret[0] == False:
        p_red('NOT SENT\n\n\n{}'.format(ret[1]))

    sleep(1.9)
    exit()




if __name__ == '__main__':
    main()
