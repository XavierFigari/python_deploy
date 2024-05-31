import json
import subprocess
import time

import requests

username = 'xavcampus'
token = '6fcae02b547afa1f4f83443e4dbd63e4ff66a5eb'
host = 'www.pythonanywhere.com'
domain_name = 'xavcampus.pythonanywhere.com'
console_id = 34037823

headers_json = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
}
headers = {
    'Authorization': f'Token {token}'
}

# URL for the get_console_output endpoint
url_get_latest_output = f'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{console_id}/get_latest_output/'


def deploiement_access():
    send_push()
    time.sleep(20)
    # time.sleep(15)
    print(console_id)
    send_pull(console_id)
    time.sleep(10)
    reload_site()
    # kill_them_all(console_id)


def reload_site():
    url = f"https://{host}/api/v0/user/{username}/webapps/{domain_name}/reload/"
    response = requests.post(url, headers=headers)
    print("reload_site : " + str(response.status_code))
    if response.status_code == 200:
        print("Rechargement réussi!")
    else:
        print(f"Erreur lors du rechargement: {response.status_code}")
        print(response.json())




# Function to get the console output
def get_console_output():
    response = requests.get(url_get_latest_output, headers=headers)
    if response.status_code == 200:
        return response.json()['output']
    else:
        print(f'Failed to get console output. Status code: {response.status_code}')
        return None


def send_pull(id_console):
    url = f"https://{host}/api/v0/user/{username}/consoles/{id_console}/send_input/"
    response = requests.post(url, headers=headers_json, json={'input': "cd ~/mysite && git pull origin main; echo $!\n"})

    # Wait a bit for the command to execute
    time.sleep(2)  # Adjust the sleep time as needed

    # Get the console output
    output = get_console_output()
    print(output)

    # Check for the return status
    # This part assumes your command includes an echo of the $? variable (if using bash), like this:
    # command = 'your_command_here; echo $?'
    if output:
        lines = output.splitlines()
        return_status = int(lines[-1])  # Assuming the last line contains the return status
        print(f'Return status: {return_status}')

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

