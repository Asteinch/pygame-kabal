import pygame

from source.card import Card

class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Solitaire")
        self.clock = pygame.time.Clock()
        self.new_game()

    def new_game(self):
        self.Cards = Card(self)

    def draw(self):
        self.win.fill("darkgreen")
        self.Cards.draw()

    def update(self):
        pygame.display.update()

        self.clock.tick(30)

    def check_for_events(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                quit()

            if not self.Cards.check_for_win():

                if event.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()

                    if self.Cards.pick_up_cards(pos):
                        continue

                    if self.Cards.drop_cards(pos):
                        continue

                    if self.Cards.pick_from_deck(pos):
                        continue
                
            else:

                pygame.display.set_caption("Won")


    def main_loop(self):
        while True:
            self.draw()
            self.update()
            self.check_for_events()

            if self.Cards.check_for_win():

                print("w")
