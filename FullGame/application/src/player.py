#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter
from threading import Event
from . import card
class Player:
    def __init__(self, name):
        # attributes
        self.name = name
        self.cards = []
        # C/S arguments
        self.args = {}
        self.new_turn = False
        # C/S syn control
        self.turn_result_available = Event()  # server can get result
        self.turn_start = Event()  # client should gather input
        self.result_has_got = Event()  # server has got result

    # def __eq__(self, other):
    #     return self.name == other.name

    # def __hash__(self):
    #     return hash('hash_of' + self.name)

    def initial_cards(self, cardlist):
        self.cards = cardlist

    # ---- interface for server ----
    def play_cards(self, cardlist):
        for card in cardlist:
            self.cards.remove(card)

    def insert_cards(self, cardlist):
        self.cards += cardlist

    def get_turn(self, new_turn) -> dict:
        self.new_turn = new_turn
        self.turn_start.set()
        self.turn_result_available.wait()
        self.turn_result_available.clear()
        self.result_has_got.set()
        return self.args
    # -------- END --------

    # ---- interface for client ----
    def refresh(self) -> list:
        self.cards.sort()
        if self.turn_start.is_set():
            if self.new_turn:
                options = ['Claim']
            else:
                options = ['Follow', 'Question', 'Pass']
            return [self.cards, options]
        else:
            return [self.cards, []]

    def send_choices(self, option: str, *cardlist: list, claim: dict = {}) -> bool:
        if self.turn_start.is_set():            
            self.args = {}
            # --- Check Option ---
            if not option or option not in ['Claim', 'Question', 'Pass', 'Follow']:
                return 'Option invalid'
            else:
                self.args['Choice'] = option
            # --- Check CardList ---
            if option == 'Claim' or option == 'Follow':
                # Check CardList Length
                if not cardlist or len(cardlist) > 8:
                    return 'Too many cards'
                # Validate Cards
                for card in cardlist:
                    if card not in self.cards:
                        return 'Card not in hand'
                else:
                    self.args['Cards'] = cardlist
            # --- Check Claim ---
            if option == 'Claim':
                if claim['claim_length'] != len(cardlist):
                    return 'Claim length not match'
                if claim['claim_rank'] not in ['2', '3', '4', '5', '6', '7', '8', '9', '10',
                    'J', 'Q', 'K', 'A']:
                    return 'Claim rank error'
                else:
                    self.args['Claim'] = claim
            # All Clear
            self.turn_result_available.set()
            self.turn_start.clear()
            self.result_has_got.wait()
            self.result_has_got.clear()
            return None
        else:
            return None
    # -------- END --------
