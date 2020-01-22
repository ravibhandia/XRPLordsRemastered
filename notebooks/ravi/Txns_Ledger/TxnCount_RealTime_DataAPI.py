def check_tx_count_great200():
    url=f'https://data.ripple.com/v2/ledgers/'
    #ledger_identifier=2020-01-22T11:20:00Z\
    resmain= requests.get(url)
    x=resmain.json()
    if (int(x['ledger']['tx_count'])>200):
        return True
    else:
        return False
