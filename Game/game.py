#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import player
import card
import board
# import math
# from player import Player


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
        self.pack_num = 0
        card.FullDeck() # initial card.FullDeck
        self.init_game()
        self.run_game()

    def set_player_numbers(self, player_numbers, player_names):
        self.players = [player.Player(name) for index, name in zip(range(player_numbers), player_names)]
        #print (len(self.players))
        #print (self.players[0].display_cards())

    def init_game(self):
        '''
        Parameters that will not change till the program ends
            will be initialized in this function.
        Paremeters that are initialized here include:
            player_numbers
            player_name for each player
            pack_numbers
        '''
        player_numbers = int(input("How many players?\n"))
        player_names = []
        for i in range(player_numbers):
            player_names.append(input("\nType player%d's name:\t" % i) + str(i))
        self.set_player_numbers(player_numbers, player_names)
        self.pack_num = int(input("How many decks do you want to play?\n"))

    def next_round(self, currentPlayer):
        PassCount = 0
        lastPlayerClaim = {}  #dict(claim_length:int, claim_rank:card_rank)
        IsNewTurn = True  # or TurnCount
        while (True):
            # for i in self.board.GetDisplayArea():
            #     print(i, end = ' ')
            playerInfo = currentPlayer.turn(IsNewTurn)
            IsNewTurn = False
            # when passcount = 0, lastplayer = currentplayer - 1
            lastPlayer = self.players[self.players.index(currentPlayer) - PassCount - 1]

            if playerInfo['Choice'] == 'Claim':
                lastPlayerClaim = playerInfo['Claim']
                currentPlayer.play_cards(playerInfo['Cards'])
                self.board.Display(playerInfo['Cards'])

            elif playerInfo['Choice'] == 'Question':
                LastPlayerCards = self.board.GetDisplayArea()[len(self.board.GetDisplayArea()) \
                            - lastPlayerClaim['claim_length']:] #- len(playerInfo['Cards']):]
                temp = set([card.rank for card in LastPlayerCards]) - set('wW')
                if (not temp) or (temp == set(lastPlayerClaim['claim_rank'])):
                    # Question Failed
                    print("Question Failed!")
                    currentPlayer.insert_cards(self.board.GetDisplayArea())
                    self.board.ClearDisplay()
                    return lastPlayer#self.players[(self.players.index(currentPlayer) + 1) % len(self.players)]
                else:
                    # Question Succeeded
                    print("Question Succeeded!")
                    lastPlayer.insert_cards(self.board.GetDisplayArea())
                    self.board.ClearDisplay()
                    return currentPlayer

            elif playerInfo['Choice'] == 'Pass':
                PassCount += 1
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

            # Winner judgement
            if not currentPlayer.cards:
                temp = set([card.rank for card in playerInfo['Cards']]) - set('wW')
                # lastPlayerClaim already updated here
                if (not temp) or (temp == set(lastPlayerClaim['claim_rank'])):
                    # Played Cards == Claimed Cards
                    print('Congratulations, you win!')
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
        self.board.ResetBoard()
        # step 2
        cardsPerPlayer = int(54 * self.pack_num / len(self.players))
        index = 0
        for hand in self.board.Deal(cardsPerPlayer, len(self.players)):
            self.players[index].initial_cards(hand)
            index += 1
        return

if __name__ == "__main__":
    Game()















