import user_interaction
import os
import subprocess

print("Shell running...")
while True:
    response, offset = user_interaction.question(f'{os.getcwd()}$')
    if response == 'quit':
        print("User quit.")
        user_interaction.send_notification('Goodbye')
        break
    print(response)
    p = subprocess.Popen(response, stdout=subprocess.PIPE, shell=True)
    user_interaction.send_notification(p.stdout.read().decode('utf8'))
