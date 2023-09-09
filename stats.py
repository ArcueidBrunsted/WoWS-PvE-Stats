import requests

realm = 'asia'
# Add your own Wargaming Application ID here
application_id = ''

def getAccountID(search):
    # Get WarGaming account id from nickname
    r_id = requests.get('https://api.worldofwarships.asia/wows/account/list/?application_id={}&search={}'.format(application_id, search))
    r_id = r_id.json()
    # Handle errors
    if r_id['status'] != 'ok':
        print('Field of error in {}\n'.format(r_id['error']['field']))
        print('Type of error is {}\n'.format(r_id['error']['message']))
        exit()
    if len(r_id['data']) == 0:
        print('No player found')
        exit()
    nickname = r_id['data'][0]['nickname']
    account_id = r_id['data'][0]['account_id']

    return nickname, account_id

def getPlayerPvPStats(account_id):
    # Get player statistics
    r_stat = requests.get('https://api.worldofwarships.asia/wows/account/statsbydate/?application_id={}&account_id={}'.format(application_id, account_id))
    r_stat = r_stat.json()
    # Handle errors
    if r_stat['data']['{}'.format(account_id)] == None:
        print('Hidden statistics')
        exit()
    pvp_stat = r_stat['data']['{}'.format(account_id)]['pvp']
    win = [p['wins'] for p in pvp_stat.values()]
    battles = [p['battles'] for p in pvp_stat.values()]
    total_xp = [p['xp'] for p in pvp_stat.values()]

    # Calculate metrics
    wr_percent = round((int(win[0])/int(battles[0]))*100,2)
    avg_xp = int(int(total_xp[0])/int(battles[0]))

    return wr_percent, avg_xp

def getOperSoloStats(account_id):
    r = requests.get('https://api.worldofwarships.asia/wows/ships/stats/?application_id={}&account_id={}&extra=oper_solo&fields=-pvp&in_garage=1'.format(application_id, account_id))
    r = r.json()
    wins = 0
    battles = 0
    total_xp = 0
    opr_perShip = []
    for p in r['data']['{}'.format(account_id)]:
        wins += p['oper_solo']['wins']
        battles += p['oper_solo']['battles']
        total_xp += p['oper_solo']['xp']
        opr_perShip.append(p['oper_solo'])

    task_star = []
    for q in opr_perShip:
        if len(q['wins_by_tasks']) != 0:
            task_star.append(q['wins_by_tasks'])
    five_star = []
    four_star = []
    three_star = []
    two_star = []
    one_star = []
    for x in task_star:
        if '5' in x:
            five_star.append(x['5'])
        if '4' in x:
            four_star.append(x['4'])
        if '3' in x:
            three_star.append(x['3'])
        if '2' in x:
            two_star.append(x['2'])
        if '1' in x:
            one_star.append(x['1'])
    # Calculate metrics
    wr = round((wins/battles)*100,2)
    avg_xp = int(total_xp/battles)
    perfect = round((sum(five_star)/battles)*100,2)

    return battles, wr, avg_xp, perfect