#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from . import player
from . import card
from . import board
from threading import Event,Lock
# import math



class Game():
    def __init__(self):
        '''
        Attributes are defined here
        Game Initialization is delegated to init_game()
        Attributes:
            self.board : Pubilc Decks
            self.players : List of Player Infomations
            self.pack_num  : Numbers of Pack of Cards
        '''
        self.board = board.GameBoard()
        self.players = []
        self.player_names = set()
        self.player_numbers = 0
        self.current_player_numbers = 0
        self.pack_num = 0

        self.WAITING = True # Waiting Flag
        self.wait_for_all_users = Event()
        self.run_game_started = 0

        self.log_lock = Lock()
        self.log = ['', '', '', '']

        # functions
        card.FullDeck() # initial card.FullDeck
        self.init_game()

    # def set_player_numbers(self, player_numbers, player_names):
    #     self.players = [player.Player(name) for index, name in zip(range(player_numbers), player_names)]
    #     return self.players
    #     #print (len(self.players))
    #     #print (self.players[0].display_cards())

    def init_game(self, player_number = 2, pack_number = 2):
        '''
        Parameters that will not change till the program ends
            will be initialized in this function.
        Paremeters that are initialized here include:
            player_numbers
            player_id for each player
            pack_numbers
        '''
        self.player_numbers = player_number
        self.pack_num = pack_number
        # self.players = [player.Player(i) for i in range(1, player_number + 1)]
        # player_numbers = int(input("How many players?\n"))
        # player_names = []
        # for i in range(player_number):
        #     player_names.append(input("\nType player%d's name:\t" % i) + str(i))
        # self.set_player_numbers(player_numbers, player_names)
        # self.pack_num = int(input("How many decks do you want to play?\n"))


    def next_round(self, currentPlayer):
        PassCount = 0
        lastPlayerClaim = {}  #dict(claim_length:int, claim_rank:card_rank)
        IsNewTurn = True  # or TurnCount
        while (True):
            # for i in self.board.GetDisplayArea():
            #     print(i, end = ' ')
            playerInfo = currentPlayer.get_turn(IsNewTurn)
            IsNewTurn = False
            # when passcount = 0, lastplayer = currentplayer - 1
            lastPlayer = self.players[self.players.index(currentPlayer) - PassCount - 1]

            if playerInfo['Choice'] == 'Claim':
                lastPlayerClaim = playerInfo['Claim']
                currentPlayer.play_cards(playerInfo['Cards'])
                self.board.Display(playerInfo['Cards'])
                self.write_log('%s claims %s card(s) of %s' % (currentPlayer.name,
                    lastPlayerClaim['claim_length'], lastPlayerClaim['claim_rank']))

            elif playerInfo['Choice'] == 'Question':
                LastPlayerCards = self.board.GetDisplayArea()[len(self.board.GetDisplayArea()) \
                            - lastPlayerClaim['claim_length']:] #- len(playerInfo['Cards']):]
                temp = set([card.rank for card in LastPlayerCards]) - set('BR')
                if (not temp) or (temp == set(lastPlayerClaim['claim_rank'])):
                    # Question Failed
                    self.write_log('%s questions fail' % currentPlayer.name)
                    currentPlayer.insert_cards(self.board.GetDisplayArea())
                    self.board.ClearDisplay()
                    return lastPlayer#self.players[(self.players.index(currentPlayer) + 1) % len(self.players)]
                else:
                    # Question Succeeded
                    self.write_log('%s questions succeed' % currentPlayer.name)
                    lastPlayer.insert_cards(self.board.GetDisplayArea())
                    self.board.ClearDisplay()
                    return currentPlayer

            elif playerInfo['Choice'] == 'Pass':
                PassCount += 1
                self.write_log('%s passes' % currentPlayer.name)
                if PassCount == len(self.players) - 1:
                    # Everyone choose pass
                    self.board.ClearDisplay()
                    # lastplayer = firstplayer = nextplayer
                    return lastPlayer

            elif (playerInfo['Choice'] == 'Follow'):
                # Actual Played Card may differ from what he claimed
                currentPlayer.play_cards(playerInfo['Cards'])
                self.board.Display(playerInfo['Cards'])
                lastPlayerClaim['claim_length'] = len(playerInfo['Cards'])
                PassCount = 0
                self.write_log('%s follows %s card(s) of %s' % (currentPlayer.name,
                    len(playerInfo['Cards']), lastPlayerClaim['claim_rank']))

            # Winner judgement
            if not currentPlayer.cards:
                temp = set([card.rank for card in playerInfo['Cards']]) - set('BR')
                # lastPlayerClaim already updated here
                if (not temp) or (temp == set(lastPlayerClaim['claim_rank'])):
                    # Played Cards == Claimed Cards
                    self.write_log('%s wins' % currentPlayer.name)
                    return None
                else:
                    # Played Cards != Claimed Cards
                    currentPlayer.insert_cards(self.board.GetDisplayArea())
                    self.board.ClearDisplay()
                    return self.players[(self.players.index(currentPlayer) + 1) % len(self.players)]

            # currentplayer = currentplayer + 1
            currentPlayer = self.players[(self.players.index(currentPlayer) + 1) % len(self.players)]
            continue # Continue this turn

    def run_game(self):
        # print('start run')
        self.run_game_started = 1
        self.wait_for_all_users.wait()
        self.reset_game()
        currentPlayer = random.choice(self.players)
        while(currentPlayer):
            nextPlayer = self.next_round(currentPlayer)
            currentPlayer = nextPlayer

    def reset_game(self):
        '''
        Reset the game to its initial state
        Steps of reset progress are as follows:
            1.Reset pubilc card Piles
            2.Deal cards to players
        '''
        # step 1
        self.board.ResetBoard(self.pack_num)
        # step 2
        print(self.pack_num, self.players)
        cardsPerPlayer = int(54 * self.pack_num / len(self.players))
        index = 0
        for hand in self.board.Deal(cardsPerPlayer, len(self.players)):
            self.players[index].initial_cards(hand)
            index += 1
        return

    def login(self, name:str) -> player:
        if self.current_player_numbers >= self.player_numbers or name in self.player_names:
            return -1
        else:
            self.players.append(player.Player(name))
            self.player_names.add(name)
            self.current_player_numbers += 1
            if self.current_player_numbers == self.player_numbers:
                self.wait_for_all_users.set()
                self.WAITING = False
            return self.current_player_numbers - 1

    def write_log(self, string:str):        
        # with self.log_lock:
        self.log = self.log[1:] +[string]
        

if __name__ == "__main__":
    Game()















