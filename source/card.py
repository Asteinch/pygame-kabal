import pygame
import re
import random
import os, time

pygame.mixer.init()

class Card:

    def __init__(self, game):

        self.win = game.win

        self.pile_number = 0

        self.pile_dragged_from = -1
        self.deck_dragged_from = False

        self.back_card = pygame.image.load("resource/cards/backbluepattern.png")
        self.empty_tile = pygame.image.load("resource/cards/emptytile.png")

        self.held_cards = []
        self.all_cards = []
        self.deck = []
        self.deck_opened = []

        self.piles = [[], [], [], [], [], [], []]

        self.top_decks = [[[self.empty_tile, ["0", 0], pygame.Rect(675, 30, 106, 144)]], 
                          [[self.empty_tile, ["0", 0], pygame.Rect(800, 30, 106, 144)]], 
                          [[self.empty_tile, ["0", 0], pygame.Rect(925, 30, 106, 144)]], 
                          [[self.empty_tile, ["0", 0], pygame.Rect(1050, 30, 106, 144)]]]

        self.pile_is_empty = [False, False, False, False, False, False, False]

        self.sounds = [pygame.mixer.Sound("./resource/sounds/pick_up.wav"), 
                       pygame.mixer.Sound("./resource/sounds/drop_card.wav"), 
                       pygame.mixer.Sound("./resource/sounds/pick_from_deck.wav"), 
                       pygame.mixer.Sound("./resource/sounds/reuse_deck.wav"),
                       pygame.mixer.Sound("./resource/sounds/win.wav")]

        self.get_all_cards()
        self.shuffle()
        self.deal_cards()

# ------------ Preparation for game start and Data

    def get_value_and_type(self, name):

        icons = ["diamonds", "spades", "hearts", "clubs"]

        value = int((re.search(r'\d+', name)).group())

        for icon in icons:
            if icon in name:

                return (icon, value)

    def get_all_cards(self):

        for filename in os.listdir("resource/cards/"):

            if filename != "backbluepattern.png" and filename != "emptytile.png" and filename != "restock.png":

                self.all_cards.append(
                    [pygame.image.load("resource/cards/" + filename),
                    (self.get_value_and_type(filename)),
                    pygame.Rect(0, 0, 0, 0),
                    True]
                    )
                
    def get_card_hitbox(self, x, y, pile, card):
            
        return pygame.Rect(x, y, 106, 30) if card != pile[-1] else pygame.Rect(x, y, 106, 144)

    def shuffle(self):

        random.shuffle(self.all_cards)

    def deal_cards(self):

        for col in range (1, 7 + 1):
            for e in range(col):

                # Adds cards to the pile list using this for loop
                current_card = self.all_cards[-1]
                self.piles[col - 1].append(current_card)
                self.all_cards.pop(-1)

        # Prepears the remaining cards after dealing and adds them to a deck list
        self.deck = self.all_cards

        for pile in self.deck:

            pile[2] = pygame.Rect(300, 30, 106, 144) #G ives the cards hitboxes
            pile[3] = False # 

        for pile in self.piles:
            pile[-1][3] = False # Makes the front card in a row visable to player (not show backside)

    def reuse_cards_from_deck(self):
        # Reuses the deck if its empty so you can pick more cards

        pygame.mixer.Sound.play(self.sounds[3])

        if len(self.deck) == 0:

            self.deck_opened.reverse()
            self.deck = self.deck_opened
            self.deck_opened = []

    def pick_cards_from_deck(self):
        # Deals 3 cards to the player, fucntion called when deck is pressed

        self.deck_opened.append(self.deck[-1])
        self.deck.remove(self.deck[-1])
        self.deck_opened[-1][2] = pygame.Rect(430, 30, 106, 144)

# ------------- Graphics 

    def print_held_cards(self):
        # draws card the player is holding

        pos = pygame.mouse.get_pos()
        y_increase = 0

        if len(self.held_cards) != 0:

            for card in self.held_cards:

                self.win.blit(card[0], (pos[0] - 53, pos[1] + y_increase - 15))
                y_increase += 30

    def print_top_decks(self):
        # draws the ace piles or whatever they called

        pos_x = 675 

        for i in range(4):

            self.win.blit(self.top_decks[i][-1][0], (pos_x, 30))
            pos_x += 100 + 25

    def print_piles(self):
        # prints the piles 

        print_x, print_y = 300, 200

        for pile_index, pile in enumerate(self.piles):
            print_y = 200

            if len(pile) == 0:

                self.pile_is_empty[pile_index] = pygame.Rect(print_x, print_y, 106, 144)
                self.win.blit(self.empty_tile, (print_x, print_y))

            for card in pile:

                # gets the cards hitbox based on location

                card[2] = self.get_card_hitbox(print_x, print_y, pile, card)

                # draws the card visable for the cards at the bottom of each pile, else it draws the backside
                self.win.blit(self.back_card, (print_x, print_y)) if card[3] else self.win.blit(card[0], (print_x, print_y))

                print_y += 30
            print_x += 125

    def print_deck(self):

        # draws the main deck

        if len(self.deck_opened) == 0:
            self.win.blit((pygame.image.load("resource/cards/restock.png")), (430, 30))
        else:

            x_increase = 0

            for i in reversed(range(1, (3 if len(self.deck_opened) >= 3 else len(self.deck_opened)) + 1)):
                # draws the card pulled from the deck

                self.win.blit((self.deck_opened[-i][0]), (430 + x_increase, 30))
                self.deck_opened[-i][2] = pygame.Rect(430 + x_increase, 30, 106, 144)
                x_increase += 30

        if len(self.deck) == 0:
            self.win.blit((pygame.image.load("resource/cards/restock.png")), (300, 30))
        else:
            self.win.blit(self.back_card, (300, 30))

# ------------- Interaction and Gameplay

    def pick_from_deck(self, pos):

        if len(self.held_cards) == 0:

            if len(self.deck_opened) > 0 and self.deck_opened[-1][2].collidepoint(pos): 
                # if the mouse collides with one of the cards pulled from the deck
                
                pygame.mixer.Sound.play(self.sounds[0])

                self.pile_dragged_from = -1 # Just so the code dont crash later

                self.held_cards.append(self.deck_opened.pop())
                if len(self.deck_opened) != 0:
                    self.deck_dragged_from = self.deck_opened[-1]
                else:
                    self.deck_dragged_from = True
                return True

            if len(self.deck) > 0 and pygame.Rect(300, 30, 106, 144).collidepoint(pos): 
                # if the mosue collides with the deck

                pygame.mixer.Sound.play(self.sounds[2])

                temp_opened = [] 
                num_cards_to_draw = min(3, len(self.deck))

                for _ in range(num_cards_to_draw):

                    if len(self.deck) == 0:

                        self.reuse_cards_from_deck()

                    self.pick_cards_from_deck()
    
                remaining_cards = 3 - num_cards_to_draw
                if remaining_cards > 0:

                    for _ in range(num_cards_to_draw):
                        temp_opened.append(self.deck_opened.pop())
                                            
                    self.reuse_cards_from_deck()

                    for card in temp_opened:
                        self.deck_opened.append(card)

                    if len(self.deck) > 0:
    
                        for _ in range(remaining_cards):

                            self.pick_cards_from_deck()
                        
                return True

            
            if len(self.deck) == 0 and pygame.Rect(300, 30, 106, 144).collidepoint(pos): 
                # Reuses the deck whenever the deck runs out of cards

                self.reuse_cards_from_deck()
                 
                return True
            
    def pick_up_cards(self, pos):

        if len(self.held_cards) == 0:

            for pile_number, pile in enumerate(self.piles):
                for card in pile:

                    if card[2].collidepoint(pos) and card[3] == False: 
                        if len(self.held_cards) == 0:
                            # If the mouse collides with one of the cards OPENED in the pile

                            pygame.mixer.Sound.play(self.sounds[0])

                            index_of_card = pile.index(card)
                            self.held_cards = [inner_list for inner_list in pile[index_of_card:]]
                            self.piles[pile_number] = [card for card in pile if card not in self.held_cards]
                            self.pile_dragged_from = pile_number
                            self.pile_number = pile_number       

                            return True
                 
            for col in self.top_decks:

                if col[0][2].collidepoint(pos) and len(col) != 1: 
                    # If the mouse collides with one of the ace piles

                    pygame.mixer.Sound.play(self.sounds[0])

                    self.held_cards.append(col[-1])
                    col.pop(-1)

                    return True
                    
    def drop_cards(self, pos):

        if len(self.held_cards) > 0:

            for hitbox_index, hitbox in enumerate(self.pile_is_empty):
                if (hitbox != False and hitbox.collidepoint(pos)) and (self.held_cards[0][1][1] == 13 or (hitbox_index == self.pile_dragged_from)):
                    # If the mouse collides with a empty pile and its a king or the card is returning to its original
                    
                    pygame.mixer.Sound.play(self.sounds[1])

                    self.piles[hitbox_index].extend(self.held_cards)
                    self.held_cards = []
                    self.pile_is_empty[hitbox_index] = pygame.Rect(0,0,0,0)

                    if len(self.piles[self.pile_dragged_from]) > 0 and self.piles[self.pile_dragged_from][-1][3]:
                        self.piles[self.pile_dragged_from][-1][3] = False
                        return True

                    return False
                
            for pile_number, pile in enumerate(self.piles):
                for card in pile:

                    if card[2].collidepoint(pos) and (self.can_place(card, pile_number) == True):
                        # if the mouse collides with a pile and you are allowed to place the card(s) under

                        pygame.mixer.Sound.play(self.sounds[1])

                        self.piles[pile_number].extend(self.held_cards)
                        self.held_cards = []

                        if len(self.piles[self.pile_dragged_from]) > 0 and self.piles[self.pile_dragged_from][-1][3]:
                            self.piles[self.pile_dragged_from][-1][3] = False

                        return True
                    

                
            if len(self.held_cards) == 1:
                for index, slot in enumerate(self.top_decks):
    
                    if slot[0][2].collidepoint(pos):
                        # If the mosue collides with the ace piles

                        if slot[-1][1][1] == 0 and self.held_cards[0][1][1] == 1:
                            # If the holding card is an ace

                            pygame.mixer.Sound.play(self.sounds[1])

                            slot.append(self.held_cards[0])
                            self.held_cards = []

                            if len(self.piles[self.pile_dragged_from]) > 0 and self.piles[self.pile_dragged_from][-1][3]:
                                self.piles[self.pile_dragged_from][-1][3] = False
                            break

                    
                        elif (slot[-1][1][1] == self.held_cards[0][1][1] - 1) and (slot[-1][1][0] == self.held_cards[0][1][0]):
                            # If the holding card is the same suite and its value is 1+ the under card

                            pygame.mixer.Sound.play(self.sounds[1])

                            slot.append(self.held_cards[0])
                            self.held_cards = []

                            if len(self.piles[self.pile_dragged_from]) > 0 and self.piles[self.pile_dragged_from][-1][3]:
                                self.piles[self.pile_dragged_from][-1][3] = False
                            break

                        return True
                
                
            if pygame.Rect(430, 30, 106, 144).collidepoint(pos) and (self.pile_dragged_from == -1) and (len(self.held_cards) == 1):
                # if the mouse collides with the deck and the card was just picked up from there
                pygame.mixer.Sound.play(self.sounds[1])

                self.deck_opened.append(self.held_cards[0])
                self.held_cards = []           

                return True

# ------------- Status and Confirmation

    def can_place(self, card, pile_number):

        if pile_number == self.pile_dragged_from:
            
            return True  

        if len(self.held_cards) > 0 and card[1][1] - 1 == self.held_cards[0][1][1]:
            # Checks if the card(s) is eligble to place in a pile
                
            if (card[1][0] == "diamonds" or card[1][0] == "hearts") and (self.held_cards[0][1][0] == "spades" or self.held_cards[0][1][0] == "clubs"):
                return True
            if (card[1][0] == "spades" or card[1][0] == "clubs") and (self.held_cards[0][1][0] == "diamonds" or self.held_cards[0][1][0] == "hearts"):
                return True
                      
        return False
    
    def check_for_win(self):

        for deck in self.top_decks:
            if len(deck) != 14:
                return False
    
        return True

    def draw(self):

        self.print_piles()
        self.print_top_decks()
        self.print_deck()
        self.print_held_cards()
    
