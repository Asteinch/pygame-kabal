import pygame

import random

import os

class Card:

    def __init__(self, game):

        self.win = game.win

        self.all_cards = []

        self.piles = [[], [], [], [], [], [], []]

        self.deck =[]

        self.back_card = pygame.image.load("images/h96/upscaled/backbluepattern.png")

        self.empty_tile = pygame.image.load("images/h96/upscaled/emptytile.png")

        self.get_all_cards()
        self.shuffle()
        self.deal_cards()

    def get_all_cards(self):

        for filename in os.listdir("images/h96/upscaled"):

            if filename != "backbluepattern.png" and filename != "emptytile.png":
                self.all_cards.append(pygame.image.load("images/h96/upscaled/" + filename))


    def shuffle(self):

        random.shuffle(self.all_cards)

    def deal_cards(self):

        card_pile_length = 1

        for i in range (1, 7 + 1):

            for e in range(card_pile_length):

                current_card = random.choice(self.all_cards)
                self.piles[i - 1].append(current_card)
                self.all_cards.remove(current_card)

            card_pile_length += 1

        self.deck = self.all_cards

        print(self.piles)


    def print_top_decks(self):

        pos_x = 675

        for i in range(4):

            self.win.blit(self.empty_tile, (pos_x, 30))

            pos_x += 100 + 25

    def print_piles(self):

        print_x = 300
        print_y = 200

        for pile in self.piles:

            print_y = 200

            for card in pile:

                self.win.blit(card, (print_x, print_y))

                print_y += 30

            print_x += 125

    def draw(self):

        self.print_piles()
        self.print_top_decks()

    