import time
import argparse
import requests

#TODO remember to change these values or it will not function
TELEGRAM_API = 'BOT FATHER TOKEN FOR TELEGRAM'
CHAT_ID='THE CHAT ID'
AUTHORIZED_USER = 'YOUR TELEGRAM USERNAME'

#sends a notification via telegram
def send_notification(message):
    r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_API}/sendMessage?chat_id={CHAT_ID}&text={message}")


def question(prompt, user_reminder = 0, offset=None):
    send_notification(prompt)
    offset = get_last_offset()

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
                        return result['message']['text'], offset

        time.sleep(wait_interval)
        if wait_interval < MAX_WAIT:
            wait_interval = cycle * INCREMENT_WAIT
            if wait_interval > MAX_WAIT:
                wait_interval = MAX_WAIT
        cycle = cycle + 1

        if user_reminder > 0:
            if cycle%user_reminder == 0:
                send_notification(prompt)

def get_last_offset():
    r = requests.get(F"https://api.telegram.org/bot{TELEGRAM_API}/getUpdates")
    results = r.json()['result']
    offset = 0
    if len(results) > 0:
        for result in results:
            offset = result['update_id']
    return offset


#will wait for a response from the user and return the string of that choice
def wait_for_choice(options, prompt="waiting for user's choice", secret=False, prefix_msgs='Choice:', user_reminder = 0):
    if options is None or len(options) == 0:
        raise Exception("Options are a mandatory array for the wait_for_choice")

    msg = f"{prefix_msgs} {prompt}"
    if secret is False:
        wait_for_msg = str(options)[2:-2]
        wait_for_msg = wait_for_msg.replace("', '",'/')
        msg = msg + f" ({wait_for_msg})"

    offset = None
    while True:
        response, offset = question(msg, user_reminder, offset)
        if response in options:
            send_notification(f"{prefix_msgs} Thanks.")
            return response
        else:
            message = f'{prefix_msgs} Not an option'
            if secret == False:
                message = message + f' ({wait_for_msg})'
            send_notification(message)


#wait for a single response
def wait_for_user(wait_for_msg = 'K',prompt='Waiting for user to proceed', prefix_msgs='Bot:', user_reminder = 180):
    wait_for_choice([wait_for_msg], prompt=prompt, secret=False, prefix_msgs=prefix_msgs, user_reminder=user_reminder)


#wait for any message, like a pause
def wait_any(prompt='Waiting any input to proceed.', prefix_msgs='Bot:',done_msg=None):
    response, offset = question(prompt=prompt, user_reminder=0)
    if done_msg is not None and done_msg != '':
        send_notification(done_msg)
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send a notification via telegram.')
    parser.add_argument('text', help='The text to send')

    args = parser.parse_args()

    if args.text == '':
        print('No text provided to send')
        quit(1)
    send_notification(args.text)
