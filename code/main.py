import pygame, sys
from settings import *
# from debug import debug
from level import Level
class Game:
    def __init__(self):
        
        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        pygame.display.set_caption("Chevalier")
        self.clock = pygame.time.Clock()

        self.level = Level()

        #sound main
        main_sound = pygame.mixer.Sound("../Chevalier/audio/main.ogg")
        main_sound.play(loops = -1)
        main_sound.set_volume(0.3)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            # debug("hello")
            pygame.display.update() 
            self.clock.tick(FPS)
            
if __name__ == '__main__':
    game = Game()
    game.run()
   