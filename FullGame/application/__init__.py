from flask import Flask
from .src import *
from os import urandom
APP = Flask(__name__)
APP.secret_key = urandom(24)
GAME = game.Game()
from application import views
import _thread
import time
# def abc():
#     time.sleep(10)
#     print('thread end')
if not GAME.run_game_started:
    _thread.start_new_thread(GAME.run_game,())
    # time.sleep(0.01)
# print('main end')