#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Card():
    def __init__(self, suit, rank):
        self.suit = suit  # suit is poker suit
        self.rank = rank  # rank is poker number

    def __str__(self):
        d = {'H':u'♥', 'S':u'♠', 'D':u'♦', 'C':u'♣', 'W':None}
        if d[self.suit]:
            return d[self.suit] + str(self.rank)
        else:
            return u'joker' if self.rank == 'w' else u'JOKER'

    def __eq__(self, othercard):
        return Card.rank2num(self.rank) == Card.rank2num(othercard.rank)

    def __gt__(self, othercard):
        return Card.rank2num(self.rank) > Card.rank2num(othercard.rank)

    def __hash__(self):
        return hash(self.suit + self.rank)

    @staticmethod
    def islegal(card):
        if  hasattr(card, 'suit') and \
            card.suit in ['H', 'S', 'D', 'C', 'W'] and \
            hasattr(card, 'rank') and \
            card.rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10',
                          'J', 'Q', 'K', 'A', 'w', 'W']:
            return True
        return False

    @staticmethod
    def rank2num(rank):
        rank2numdict = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
                        '10':10, 'J':11, 'Q':12, 'K':13, 'A':14, 'w':15, 'W':16}
        return rank2numdict[rank]

class FullDeck():
    cards = []
    def __init__(self):
        if FullDeck.cards:
            return
        NumberCards = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
        ColorCards = ['J', 'Q', 'K', 'A']
        suits = ['H', 'S', 'D', 'C'] # H for Hearts, S for Spades, D for Diamonds, C for Clubs.
        for suit in suits:
            for NumberCard in NumberCards:
                FullDeck.cards.append(Card(suit, NumberCard))
            for ColorCard in ColorCards:
                FullDeck.cards.append(Card(suit, ColorCard))
        FullDeck.cards.append(Card('W', 'w'))  # build the Jokers, W for Wang
        FullDeck.cards.append(Card('W', 'W'))

    @classmethod
    def GetFullDeck(self):
        return FullDeck.cards.copy()

if __name__ == "__main__":
    FullDeck()
    for i in FullDeck.GetFullDeck():
        print(i, end = ' ')
    print()