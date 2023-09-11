# This is an simple web application created using Flask and Pyvibe
# Deploy it on your second computer or Raspberry Pi
# Enter your teammates' nickname and the program will show his stats
# Stats retrieved from WarGaming API
# Please do not use the result for stats shaming
# Author: Jason Qin
# Date: 9/9/2023
# Version: 0.1.0

from flask import Flask, render_template, request
from stats import getAccountID, getOperSoloStats, getPlayerPvPStats
import pyvibe as pv

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home() -> str:
    page = pv.Page('Home')
    page.add_header('WoWS PvE Stats')

    with page.add_card() as card:
        card.add_header("hello")
        with card.add_form(action="/detail") as form:
            form.add_formtext(label="Nickname", name="nickname", placeholder="Enter your nickname")
            form.add_formsubmit(label="Send")
    return page.to_html()

@app.route('/detail')
def detail() -> str:
    page = pv.Page("PvE Stats")

    input = request.args['nickname']
    nickname, account_id = getAccountID(input)
    wr_percent, avg_xp = getPlayerPvPStats(account_id)
    opr_btl, opr_wr, opr_avg_xp, opr_perfect = getOperSoloStats(account_id)
    line1 = 'Player {} has UID {}'.format(nickname, account_id)
    line2 = 'Win Rate: {}%; Average Exp: {}'.format(wr_percent, avg_xp)
    line3 = 'Played {} solo random operations'.format(opr_btl)
    line4 = 'Operation win rate is: {}%'.format(opr_wr)
    line5 = 'Operation average exp is: {}'.format(opr_avg_xp)
    line6 = 'Probability of getting 5 star is: {}%'.format(opr_perfect)
    with page.add_card() as card:
        card.add_header("Player PvE Stats")
        card.add_text(value=line1)
        card.add_text(value=line2)
        card.add_text(value=line3)
        card.add_text(value=line4)
        card.add_text(value=line5)
        card.add_text(value=line6)
        # Check if inexperienced NOOB
        if opr_btl <= 100:
            card.add_alert(text='Inexperienced <100 btl', badge='Warning', color='red')
        else:
            card.add_alert(text='Experienced', badge='Pass', color='green')
            # Check if experienced NOOB
            if opr_wr <= 85:
                card.add_alert(text='Low operation win rate', badge='Warning', color='orange')
            else:
                card.add_alert(text='Normal operation win rate', badge='Pass', color='green')

            if opr_perfect < 50:
                card.add_alert(text='Low 5 stars probabilities', badge='Warning', color='orange')
            else:
                card.add_alert(text='Normal 5 stars probability', badge='Pass', color='green')

            if opr_avg_xp < 1500:
                card.add_alert(text='Not enough contribution', badge='Warning', color='orange')
            else:
                card.add_alert(text='Normal contribution', badge='Pass', color='green')
            
    return page.to_html()

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
