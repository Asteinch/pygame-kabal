import pygame

from card import Card

class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Kabal")
        self.clock = pygame.time.Clock()
        self.new_game()

    def new_game(self):
        self.Cards = Card(self)

    def draw(self):
        self.win.fill("darkgreen")
        self.Cards.draw()

    def update(self):
        pygame.display.update()

    def check_for_events(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                self.Cards.pick_up_cards()

                self.Cards.drop_cards()

    def main_loop(self):
        while True:
            self.draw()
            self.update()
            self.check_for_events()

if __name__ == "__main__":

    game = Game()

    game.main_loop()