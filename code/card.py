import pygame
import re
import random
import os
import time

class Card:

    def __init__(self, game):

        self.win = game.win

        self.all_cards = []
        self.piles = [[], [], [], [], [], [], []]
        self.deck =[]
        self.held_cards = []

        self.top_decks = [[], [], [], []]

        self.pile_is_empty = [pygame.Rect(0,0,0,0),pygame.Rect(0,0,0,0),pygame.Rect(0,0,0,0),pygame.Rect(0,0,0,0),pygame.Rect(0,0,0,0),pygame.Rect(0,0,0,0),pygame.Rect(0,0,0,0),pygame.Rect(0,0,0,0)]
        self.from_pile_hitbox = pygame.Rect(0,0,0,0)

        self.pile_number = 0

        self.pile_dragged_from = int

        self.back_card = pygame.image.load("images/h96/upscaled/backbluepattern.png")
        self.empty_tile = pygame.image.load("images/h96/upscaled/emptytile.png")

        self.top_decks = [[[self.empty_tile, ["0", 0], pygame.Rect(675, 30, 106, 144)]], 
                          [[self.empty_tile, ["0", 0], pygame.Rect(800, 30, 106, 144)]], 
                          [[self.empty_tile, ["0", 0], pygame.Rect(925, 30, 106, 144)]], 
                          [[self.empty_tile, ["0", 0], pygame.Rect(1050, 30, 106, 144)]]]

        self.get_all_cards()
        self.shuffle()
        self.deal_cards()


    def get_value_and_type(self, name):

        icons = ["diamonds", "spades", "hearts", "clubs"]

        value = self.extract_number(name)

        for icon in icons:
            if icon in name:

                return (icon, value)

    def get_all_cards(self):

        for filename in os.listdir("images/h96/upscaled"):

            if filename != "backbluepattern.png" and filename != "emptytile.png" and filename != "restock.png":

                self.all_cards.append(
                    [pygame.image.load("images/h96/upscaled/" + filename),
                    (self.get_value_and_type(filename)),
                    pygame.Rect(0, 0, 0, 0),
                    True]
                    )
                
    def get_card_hitbox(self, x, y, pile, card):
            
        return pygame.Rect(x, y, 104, 30) if card != pile[-1] else pygame.Rect(x, y, 106, 144)
    
    def extract_number(self, filename):

        return int((re.search(r'\d+', filename)).group()) if re.search(r'\d+', filename) else None

    def shuffle(self):

        random.shuffle(self.all_cards)

    def deal_cards(self):

        for i in range (1, 7 + 1):
            for e in range(i):

                current_card = random.choice(self.all_cards)
                self.piles[i - 1].append(current_card)
                self.all_cards.remove(current_card)

        self.deck = self.all_cards

        for pile in self.piles:
            pile[-1][3] = False

        print(self.piles)


    def print_held_cards(self):

        pos = pygame.mouse.get_pos()

        y_increase = 0

        if len(self.held_cards) != 0:

            for card in self.held_cards:

                self.win.blit(card[0], (pos[0], pos[1] + y_increase))

                y_increase += 30


    def print_top_decks(self):

        pos_x = 675

        for i in range(4):

            self.win.blit(self.top_decks[i][-1][0], (pos_x, 30))

            pos_x += 100 + 25

    def print_piles(self):

        print_x, print_y = 300, 200

        for pile_index, pile in enumerate(self.piles):
            print_y = 200

            if len(pile) == 0:

                self.pile_is_empty[pile_index] = pygame.Rect(print_x, print_y, 106, 144)
                self.win.blit(self.empty_tile, (print_x, print_y))

            for card in pile:

                card[2] = self.get_card_hitbox(print_x, print_y, pile, card)

                self.win.blit(self.back_card, (print_x, print_y)) if card[3] else self.win.blit(card[0], (print_x, print_y))

                print_y += 30
            print_x += 125


    def pick_up_cards(self):

        # sjekker alle kort og om spillern prøver å plukke de opp, hvis så vil kortene bli plukket opp

        if len(self.held_cards) == 0:

            pos = pygame.mouse.get_pos()

            for pile_number, pile in enumerate(self.piles):
                for card in pile:

                    if card[2].collidepoint(pos) and card[3] == False:

                        if len(self.held_cards) == 0:


                            index_of_card = pile.index(card)
                            self.held_cards = [inner_list for inner_list in pile[index_of_card:]]

                            self.piles[pile_number] = [card for card in pile if card not in self.held_cards]

                            self.pile_dragged_from = pile_number

                            self.pile_number = pile_number
          
    def drop_cards(self):

        if len(self.held_cards) > 0:

            pos = pygame.mouse.get_pos()

            for hitbox_index, hitbox in enumerate(self.pile_is_empty):
                if (hitbox.collidepoint(pos)) and (self.held_cards[0][1][1] == 13 or hitbox_index == self.pile_number):
                # for tomme bunker

                    self.piles[hitbox_index].extend(self.held_cards)
                    self.held_cards = []
                    self.pile_is_empty[hitbox_index] = pygame.Rect(0,0,0,0)

                    if len(self.piles[self.pile_dragged_from]) > 0 and self.piles[self.pile_dragged_from][-1][3]:
                        self.piles[self.pile_dragged_from][-1][3] = False

                    return False
                
            for pile_number, pile in enumerate(self.piles):
                for card in pile:
                # for vanlig plasseringer

                    if card[2].collidepoint(pos) and (self.can_place(card, pile_number) == True):

                        self.piles[pile_number].extend(self.held_cards)
                        self.held_cards = []

                        if len(self.piles[self.pile_dragged_from]) > 0 and self.piles[self.pile_dragged_from][-1][3]:
                            self.piles[self.pile_dragged_from][-1][3] = False
                
            if len(self.held_cards) == 1:
                for index, slot in enumerate(self.top_decks):
                # for toppbunkene

                    if slot[0][2].collidepoint(pos):

                        if slot[0][1][1] == 0 and self.held_cards[0][1][1] == 1:

                            slot.append(self.held_cards[0])
                            self.held_cards = []

                            if len(self.piles[self.pile_dragged_from]) > 0 and self.piles[self.pile_dragged_from][-1][3]:
                                self.piles[self.pile_dragged_from][-1][3] = False
                            break

                        elif (slot[-1][1][1] == self.held_cards[0][1][1] - 1) and (slot[-1][1][0] == self.held_cards[0][1][0]):

                            slot.append(self.held_cards[0])
                            self.held_cards = []

                            if len(self.piles[self.pile_dragged_from]) > 0 and self.piles[self.pile_dragged_from][-1][3]:
                                self.piles[self.pile_dragged_from][-1][3] = False
                            break


    def can_place(self, card, pile_number):

        if len(self.held_cards) > 0 and card[1][1] - 1 == self.held_cards[0][1][1]:

            if (card[1][0] == "diamonds" or card[1][0] == "hearts") and (self.held_cards[0][1][0] == "spades" or self.held_cards[0][1][0] == "clubs"):
                return True
            if (card[1][0] == "spades" or card[1][0] == "clubs") and (self.held_cards[0][1][0] == "diamonds" or self.held_cards[0][1][0] == "hearts"):
                return True
            
        elif pile_number == self.pile_number:
            return True
                
        return False
    
    #def can_place_on_top_deck(card):


            

    def draw(self):

        self.print_piles()
        self.print_top_decks()
        self.print_held_cards()

    