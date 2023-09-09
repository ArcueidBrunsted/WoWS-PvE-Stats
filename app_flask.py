from flask import Flask, render_template, request
from stats import getAccountID, getOperSoloStats, getPlayerPvPStats
import pyvibe as pv
app = Flask(__name__)

@app.route('/wows', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_input = request.form.get('text_input')
        
        nickname, account_id = getAccountID(text_input)
        wr_percent, avg_xp = getPlayerPvPStats(account_id)
        opr_btl, opr_wr, opr_avg_xp, opr_perfect = getOperSoloStats(account_id)

        line1 = 'Player {} has UID {}'.format(nickname, account_id)
        line2 = 'Win Rate: {}%; Average Exp: {}'.format(wr_percent, avg_xp)
        line3 = 'Played {} solo random operations'.format(opr_btl)
        line4 = 'Operation win rate is: {}%'.format(opr_wr)
        line5 = 'Operation average exp is: {}'.format(opr_avg_xp)
        line6 = 'Probability of getting 5 star is: {}%'.format(opr_perfect)
        return render_template('index.html', line1=line1, line2=line2, line3=line3, line4=line4, line5=line5, line6=line6)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
