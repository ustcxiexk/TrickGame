from flask import flash, redirect, render_template, \
     request, url_for, session
from application import APP,GAME
from .src import player, game
from .src.card import Card
# import card
# import player
# import board
# import game
# print('view!!')
# print(card.Card('A','10'))
APP.user = {'admin':'admin',
            'player1':'player1', 'player2':'player2',
            'player3':'player3', 'player4':'player4',
            '1':'1', '2':'2', '3':'3', '4':'4'}

# --- Login Page ---
@APP.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] not in APP.user or \
                request.form['password']  != APP.user[request.form['username']]:
            error = 'Invalid User'
        # Admin
        elif request.form['username'] == 'admin':
            flash('You were successfully logged in', category='error')
            session['username'] = request.form['username']
            return redirect(url_for('config'))
        # Player
        else:
            flash('You were successfully logged in', category='error')
            player = GAME.login(request.form['username'])
            if player == -1:
                flash('No player available now', category='error')
                return render_template('login.html', error=error)
            else:
                session['username'] = request.form['username']
                session['player'] = player
                return redirect(url_for('play'))
    return render_template('login.html', error=error)

@APP.route('/config', methods=['GET', 'POST'])
def config():
    flash('game started', category='error')
    return redirect(url_for('login'))

# --- Game Page ---
@APP.route('/play', methods=['GET', 'POST'])
def play():
    if 'username' not in session:
        flash('Skip Login Error', category='error')
        return redirect(url_for('login'))
    if session['username'] not in GAME.player_names:
        flash('Login Expired', category='error')
        return redirect(url_for('login'))
    # Normal Routine
    imagesrc = []
    need_refresh = True
    player = session['username']
    if GAME.WAITING:        
        flash("Waiting for other players to join!", category='error')
    else:
        # -- Post --
        if request.method == 'POST':
            choose_option = request.form.get('Option')
            if request.form.get('Cards'):
                choose_cards = request.form.get('Cards')[:-1]
                choose_cards = choose_cards.split(',')
                choose_cards_reform = [Card(card[0].upper(), card[1:].upper())\
                    for card in choose_cards]
            else:
                choose_cards_reform = []
            choose_claim = {'claim_length':len(choose_cards_reform),\
                    'claim_rank':request.form.get('ClaimOption')}
            error = GAME.players[session['player']].send_choices(choose_option,\
                *choose_cards_reform, claim=choose_claim)
            if error:                
                flash(error, category='error')
                
        # -- Get --
        # with GAME.log_lock:
        for i in GAME.log:
            flash(i, category='log')
        cards, options = GAME.players[session['player']].refresh()
        cards = [str(card).lower() for card in cards] # reform cards
        if options:
            need_refresh = False       

        # -- refresh page --                    
        for card in cards:
            imagesrc += [[card, "../static/pokerimg/%s.jpg " % card]]
            #flash(imagesrc, category='cards')
        if not need_refresh:
            for option in options:
                flash(option, category='options')
        # print(need_refresh)
    return render_template('cards.html', need_refresh=need_refresh, 
                            cards=imagesrc, player=player)

# --- Home Page ---
@APP.route('/', methods=['GET'])
@APP.route('/index', methods=['GET'])
def get_tasks():  
    return render_template('index.html')
