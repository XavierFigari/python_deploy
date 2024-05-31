import json
import subprocess
import time

import requests

username = 'xavcampus'
token = '6fcae02b547afa1f4f83443e4dbd63e4ff66a5eb'
host = 'www.pythonanywhere.com'
domain_name = 'xavcampus.pythonanywhere.com'

headers_json = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
}

def deploiement_access():
    send_push()
    time.sleep(20)
    console_id = 34037823
    # time.sleep(15)
    print(console_id)
    send_pull(console_id)
    time.sleep(10)
    reload_site()
    # kill_them_all(console_id)


def reload_site():
    headers = {
        'Authorization': f'Token {token}'
    }
    url = f"https://{host}/api/v0/user/{username}/webapps/{domain_name}/reload/"
    response = requests.post(url, headers=headers)
    print("reload_site : " + str(response.status_code))
    if response.status_code == 200:
        print("Rechargement réussi!")
    else:
        print(f"Erreur lors du rechargement: {response.status_code}")
        print(response.json())



def send_pull(id_console):
    url = f"https://{host}/api/v0/user/{username}/consoles/{id_console}/send_input/"
    response = requests.post(url, headers=headers_json, json={'input': "cd ~/mysite && git pull origin main\n"})
    print("send_pull : " + str(response.status_code))
    if response.status_code == 200:
        print("le repo a été téléchargé")
    else:
        print("le pull n'est pas passé")


def open_console():
    url = f"Https://{host}/api/v0/user/{username}/consoles/"
    data = {
        'executable': "/bin/bash"
    }
    response = requests.post(url, headers=headers_json, data=json.dumps(data))
    print("open console : " + str(response.status_code))
    if response.status_code == 201 or response.status_code == 200:
        console_id = response.json()['id']
        print(f"Nouvelle console bash créée avec ID: {console_id}")
        return console_id
    else:
        print(f"Erreur lors de la création de la console: {response.status_code}")
        print(response.json())
        return "lol"


def kill_them_all(id):
    headers = {
        'Authorization': f'Token {token}',
    }
    url = f"Https://{host}/api/v0/user/{username}/consoles/{id}"
    response = requests.delete(url, headers=headers)
    print("kill them all : " + str(response.status_code))
    if response.status_code == 200:
        print("la console est fermée")
    else:
        print("la console n'est pas fermée")


def send_push():
    message = input("Tape ton message pour commit : ")
    subprocess.run(["git", "commit", "-am", f"{message}"])
    subprocess.run(["git", "push", "origin", "main"])


deploiement_access()
