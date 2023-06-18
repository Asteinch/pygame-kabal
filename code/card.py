import pygame

import re

import random

import os

class Card:

    def __init__(self, game):

        self.win = game.win

        self.all_cards = []

        self.piles = [[], [], [], [], [], [], []]

        self.deck =[]

        self.held_cards = []

        self.back_card = pygame.image.load("images/h96/upscaled/backbluepattern.png")

        self.empty_tile = pygame.image.load("images/h96/upscaled/emptytile.png")

        self.get_all_cards()
        self.shuffle()
        self.deal_cards()

    
    def extract_number(self, filename):
        #skrevet av chatgpt fordi jeg kan ikke programmere

        pattern = r'\d+'  # Regular expression pattern to match one or more digits
        match = re.search(pattern, filename)
        
        if match:
            value = int(match.group())
            return value
        else:
            return None
        
    def draw_held_cards(self):

        pos = pygame.mouse.get_pos()

        x_inc, y_inc = 0, 0 


        if len(self.held_cards) != 0:

            for card in self.held_cards:

                self.win.blit(card[0], (pos[0], pos[1] + y_inc))

                y_inc += 30


    def get_value_and_type(self, name):

        # finner kort type og verdi fra filnavnet til bilde gitt

        icons = ["diamonds", "spades", "hearts", "clubs"]

        value = self.extract_number(name)

        for icon in icons:
            if icon in name:

                return (icon, value)

    def get_all_cards(self):

        # henter alle kort bildene og legger de i en lioste med bilde, korttype og verdi

        for filename in os.listdir("images/h96/upscaled"):

            if filename != "backbluepattern.png" and filename != "emptytile.png":

                self.all_cards.append( 
                    
                    
                    [pygame.image.load("images/h96/upscaled/" + filename),

                    (self.get_value_and_type(filename)),

                    pygame.Rect(0, 0, 0, 0)])



    def shuffle(self):

        # forklarer seg selv

        random.shuffle(self.all_cards)

    def deal_cards(self):

        # henter tilfeldige kort fra kortstokken som skal brukes av spillern

        card_pile_length = 1

        for i in range (1, 7 + 1):

            for e in range(card_pile_length):

                current_card = random.choice(self.all_cards)
                self.piles[i - 1].append(current_card)
                self.all_cards.remove(current_card)

            card_pile_length += 1

        self.deck = self.all_cards

        #print(self.piles)


    def print_top_decks(self):

        # printer dekkene øverst på brettet

        pos_x = 675

        for i in range(4):

            self.win.blit(self.empty_tile, (pos_x, 30))

            pos_x += 100 + 25

    def get_card_hitbox(self, x, y, pile, piles):


        if pile != pile[-1]:
            return pygame.Rect(x, y, 104, 30)      
        else: 
            return pygame.Rect(x, y, 106, 144)


    def print_piles(self):

        # Viser spillern kortene de kan bruke

        print_x = 300
        print_y = 200

        for pile in self.piles:

            print_y = 200

            for card in pile:

                #print(card)
                """"

                if len(pile) > 0 and card != pile[-1]:

                    # skjuler kortet hvsi det ikke er fremst i rekken

                    self.win.blit(self.back_card, (print_x, print_y))
                
                else:
                """

    
                self.win.blit(card[0], (print_x, print_y))

                card[2] = self.get_card_hitbox(print_x, print_y, pile, self.piles)

                print_y += 30

            print_x += 125

    def pick_up_cards(self):

        if len(self.held_cards) == 0:

            pos = pygame.mouse.get_pos()

            pile_number = 0

            for pile in self.piles:

                for card in pile:

                    if card[2].collidepoint(pos):

                        index_of_card = pile.index(card)
                        self.held_cards = [inner_list for inner_list in pile[index_of_card:]]

                        self.piles[pile_number] = [cock for cock in pile if cock not in self.held_cards]

                pile_number += 1

    def drop_cards(self):

        if len(self.held_cards) > 0:

            pos = pygame.mouse.get_pos()

            pile_number = 0

            for pile in self.piles:

                for card in pile:

                    if card[2].collidepoint(pos):

                        for held_card in self.held_cards:

                            self.piles[pile_number].append(held_card)

                        self.held_cards = []

                pile_number += 1

                    



            
    def draw(self):

        self.print_piles()
        self.print_top_decks()
        self.draw_held_cards()

    