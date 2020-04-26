import slack
from slacker import Slacker
#from IPython.display import Image
import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import time
from datetime import datetime
import re

tx_count_bound = 200
fees_bound = 15395

token = 'your token here'
slack = Slacker(token)

# Check for success
if slack.api.test().successful:
    print(f"Connected to {slack.team.info().body['team']['name']}")
else:
    print('Try Again!')

def check_tx_count_great(bound):
    url = 'https://data.ripple.com/v2/ledgers/' + datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    # ledger_identifier=2020-01-22T11:20:00Z\
    resmain = requests.get(url)
    x = resmain.json()

    while 'result' not in x.keys():
        stop_Num = float(re.findall(r"\d+\.?\d*", x['error'])[-1]) + 1
        time.sleep(stop_Num)
        resmain = requests.get(url)
        x = resmain.json()

    print(x['ledger']['ledger_index'])
    if (int(x['ledger']['tx_count']) > bound):
        return True, x
    else:
        return False, x

def fees_great(bound):
    url = 'https://data.ripple.com/v2/network/fees?' + datetime.now().strftime(
        '%Y-%m-%dT%H:%M:%SZ') + '&limit=1&descending=true'
    resmain = requests.get(url)
    x = resmain.json()

    while 'result' not in x.keys():
        stop_Num = float(re.findall(r"\d+\.?\d*", x['error'])[-1]) + 1
        time.sleep(stop_Num)
        resmain = requests.get(url)
        x = resmain.json()

    if (x['rows'][0]['avg'] * 1000000 > bound):
        return True, x
    else:
        return False, x

no_repeat = ''
ledger = ''
no_repeat1 = ''
ledger1 = ''
while True:
    check, y = check_tx_count_great(tx_count_bound)
    check1, x = fees_great(fees_bound)
    if check:
        a = str(y['ledger']['tx_count'])
        ledger = str(y['ledger']['ledger_index'])
        if ledger != no_repeat:
            linkk = 'https://livenet.xrpl.org/ledgers/' + ledger
            message = '<!everyone> *Careful bros, unusual amount of transactions per ledger*\n We got ' + a + ' transactions per ledger in the last period\n Check out ledger ' + ledger + '\nHere\n' + linkk
            slack.chat.post_message(channel='#anomaly_detection',
                                    text=message,
                                    username='transactions_bot',
                                    icon_emoji=':female-firefighter:')
    if check1:
        ledger1 = str(x['rows'][0]['ledger_index'])
        if ledger1 != no_repeat1:
            message1 = '<!everyone> *Careful bros, unusual average fees per ledger*\n We got an average of  ' + str(
                x['rows'][0]['avg']) + ' fees per ledger in the last period\n Check out ledger ' + str(
                x['rows'][0]['ledger_index']) + '\nHere\n' + 'https://livenet.xrpl.org/ledgers/' + str(
                x['rows'][0]['ledger_index'])
            # print(message1)
            slack.chat.post_message(channel='#anomaly_detection',
                                    text=message1,
                                    username='fee_bot',
                                    icon_emoji=':money_with_wings:')

    no_repeat = ledger
    no_repeat1 = ledger1
    time.sleep(2)
