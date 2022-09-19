import time
import argparse
import requests

#TODO remember to change these values or it will not function
TELEGRAM_API = 'BOT FATHER TOKEN FOR TELEGRAM'
CHAT_ID='THE CHAT ID'
AUTHORIZED_USER = 'YOUR TELEGRAM USERNAME'

def send_notification(message):
    r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_API}/sendMessage?chat_id={CHAT_ID}&text={message}")


def wait_for_user(wait_for_msg = 'Ok', secret=False, prefix_msgs='Bot:', user_reminder = 180):
    msg = f"{prefix_msgs} waiting for user interaction"
    if secret is False:
        msg = msg + f" ({wait_for_msg})"
    send_notification(msg)
    #get the oldest message date
    r = requests.get(F"https://api.telegram.org/bot{TELEGRAM_API}/getUpdates")
    results = r.json()['result']
    offset = 0
    if len(results) > 0:
        for result in results:
            offset = result['update_id']
        

    MAX_WAIT = 60
    INCREMENT_WAIT = 1
    
    start_wait = 1
    wait_interval = start_wait
    cycle = 0
    while True:
        body = {"offset": offset}
        r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_API}/getUpdates",data=body)

        if r.status_code == 200:
            results = r.json()['result']
            for result in results:
                if result['update_id'] > int(offset):
                    wait_interval = start_wait
                    cycle = 0
                    offset = result['update_id']
                    if result['message']['from']['username'] == AUTHORIZED_USER:
                        if result['message']['text'] == wait_for_msg:
                            send_notification(f"{prefix_msgs} Thanks.")
                            return True
                        else:
                            message = f'{prefix_msgs} Not the response I was waiting for'
                            if secret == False:
                                message = message + f' ({wait_for_msg})'
                            send_notification(message)

        time.sleep(wait_interval)
        if wait_interval < MAX_WAIT:
            wait_interval = cycle * INCREMENT_WAIT
            if wait_interval > MAX_WAIT:
                wait_interval = MAX_WAIT
        cycle = cycle + 1

        if user_reminder > 0:
            if cycle%user_reminder == 0:
                message = f'{prefix_msgs} waiting for user input....'
                if secret == False:
                    message = message + f' ({wait_for_msg})'
                send_notification(message)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send a notification via telegram.')
    parser.add_argument('text', help='The text to send')

    args = parser.parse_args()

    if args.text == '':
        print('No text provided to send')
        quit(1)
    send_notification(args.text)

