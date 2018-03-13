#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter
import card
class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def initial_cards(self, cardlist):
        self.cards = cardlist

    def _display_cards(self):
        self.cards.sort()
        for card in self.cards:
            print(card, end = ' ')
        print()

    def play_cards(self, cardlist):
        for card in cardlist:
            self.cards.remove(card)

    def insert_cards(self, cardlist):
        self.cards += cardlist

    def turn(self, new_turn):
        # Must_Done_Process
        print("\nPlayer %s, now is your turn." % self.name)
        print("Your hand is:")
        self._display_cards()
        arg = {} # return arguments

        # Generate Options
        options = {}
        if new_turn:
            options['Claim'] = self._choose_claim
        else:
            options['Follow'] = self._choose_follow
            options['Question'] = self._choose_question
            options['Pass'] = self._choose_pass

        print("Your Options are as follows:")
        optionlist = []
        for ind, option in enumerate(options, 1):
            print("%s : %d" % (option, ind), end='\t')
            optionlist.append(option)
        print("Input your choice")
        choice = self._get_number(len(optionlist), 1)
        arg['Choice'] = optionlist[choice - 1]
        options[optionlist[choice - 1]](arg) # Execute Option Function

        # Final Judgements
        # Nothing to do here
        return arg

    def _choose_question(self, arg: dict):
        return

    def _choose_follow(self, arg: dict):
        print("Type how many cards you want to follow:")
        num = self._get_number(len(self.cards), 1)
        arg['Cards'] = self._input_card_list(num)
        return

    def _choose_pass(self, arg: dict):
        return

    def _choose_claim(self, arg: dict):
        print("A new round start with you, please claim.")
        print("Claim example: 5 J for 5 'J' cards, you cannot claim 'W' or >10 cards")
        claim = []
        while 1:
            claim = input("Please make your claim:")
            claim = claim.strip().split()
            if len(claim) != 2:
                continue
            # judge Number argument
            if not claim[0].isdigit:
                continue
            else:
                claim[0] = int(claim[0])
                if claim[0] <= 0 or claim[0] > 10:
                    continue
            # judge Rank argument
            if len(claim[1]) != 1:
                if(claim[1]) == '10':
                    break
                continue
            else:
                claim[1] = claim[1].upper()
                if claim[1] not in ['2', '3', '4', '5', '6', '7',
                                    '8', '9', 'J', 'Q', 'K', 'A']:
                    continue
            break
        arg['Claim'] = {'claim_length' : int(claim[0]), 'claim_rank' : claim[1]}
        arg['Cards'] = self._input_card_list(int(claim[0]))

    def _input_card_list(self, num) -> list:
        print("""   Please Input Card List, Example:
                    H5/h5 for five of hearts,
                    ww/Ww for joker, WW/wW for JOKER
                    sj/sJ/Sj/SJ for jack of spades""")
        while 1:
            string = input("Input now:")
            templist = string.strip().split()
            templist = [(string[0], string[1:]) for string in templist]
            print(templist)
            templist = [(suit.upper(), rank.upper()) if suit.upper() != 'W' else (suit.upper(), rank) \
                        for suit, rank in templist]
            print(templist)
            cardlist = [card.Card(suit,rank) for suit,rank in templist]
            if len(cardlist) != num:
                print('length error')
                continue
            delta = Counter(self.cards)
            delta.subtract(cardlist)
            #print(delta.items())
            if all(map(lambda x: x >= 0, delta.values())):
                return cardlist
            print('not in hand')

    def _get_number(self, maxm, minm = 0) -> int:
        if maxm < minm:
            return minm
        while 1:
            num = input("Input a number: ")
            if num.isdigit():
                num = int(num)
                if num <= maxm and num >= minm:
                    return num

    def print_log(self, string):
        print(string)
