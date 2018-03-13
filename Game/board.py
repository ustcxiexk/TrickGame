#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import shuffle
from card import FullDeck

class GameBoard():
    def __init__(self):
        self.Deck = []
        self.DiscardPile = []
        self.DisplayArea = []


    def ResetBoard(self, NumOfDecks = 2):
        for i in range(NumOfDecks):
            self.Deck += FullDeck.GetFullDeck()
        self.DiscardPile.clear()
        self.DisplayArea.clear()
        shuffle(self.Deck)
        return self

    def Deal(self, CardsForEachPlayer, NumOfPlayers = 4):
        if len(self.Deck) < CardsForEachPlayer * NumOfPlayers:
            return 0
        temp = []
        for i in range(NumOfPlayers):
            temp.append(self.Deck[i * CardsForEachPlayer : (i + 1) * CardsForEachPlayer])
        self.Deck[0 : CardsForEachPlayer * NumOfPlayers] = []
        return temp

    def Draw(self):
        return self.Deck.pop() if self.Deck else 0

    def GetDisplayArea(self):
        return self.DisplayArea

    def Display(self, cardlist):
        self.DisplayArea += cardlist

    def ClearDisplay(self):
        self.DiscardPile += self.DisplayArea
        self.DisplayArea.clear()

    def Discard(self, cardlist):
        self.DiscardPile += cardlist

    def ReShuffleDeck(self):
        if self.Deck:
            shuffle(self.Deck)

if __name__ == "__main__" :
    FullDeck()
    gb = GameBoard()
    gb.ResetBoard()
    hands = gb.Deal(27, 4)
    cnt = 0
    for hand in hands:
        print("\nplayer %d's hand: " % cnt)
        for card in hand:
            print(card, end = ' ')
        cnt += 1
    print("\nEndOfHands")
    gb.Display(hands[0])
    for card in gb.GetDisplayArea():
        print(card, end = ' ')
    print("\nEndOfDisplay")
    gb.Discard(hands[1])
    gb.ClearDisplay()
    for card in gb.GetDisplayArea():
        print(card, end = ' ')
    print("\nEndOfDisplay II")



