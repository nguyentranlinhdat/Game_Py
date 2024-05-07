import pygame, sys
from settings import *
# from debug import debug
from level import Level
from button import Button
class Game:
    def __init__(self, screen):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))

        self.state = "main_menu"
        self.bg = pygame.image.load("../Chevalier/assets/Background.png")
        self.font = pygame.font.Font("../Chevalier/assets/font.ttf", 100)
        self.buttons = []
        self.clock = pygame.time.Clock()

        self.level = Level()
        #sound main
        main_sound = pygame.mixer.Sound("../Chevalier/audio/main.ogg")
        main_sound.play(loops = -1)
        main_sound.set_volume(0.3)
    #thêm font
    def get_font(size): 
        return pygame.font.Font("../Chevalier/assets/font.ttf", size)
    #Hiển thị giao diện các Button
    def add_button(self, image, pos, text_input, font_size, base_color, hovering_color):
        font = pygame.font.Font("../Chevalier/assets/font.ttf", font_size)
        button = Button(image, pos, text_input, font, base_color, hovering_color)
        self.buttons.append(button)
    #Phần giao diện đầu game
    def run_main_menu(self):
        while self.state == "main_menu":
            self.screen.blit(self.bg, (0, 0))
            menu_mouse_pos = pygame.mouse.get_pos()
            menu_text = self.font.render("MAIN MENU", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(640, 100))
            self.screen.blit(menu_text, menu_rect)

            for button in self.buttons:
                button.changeColor(menu_mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #Kiểm tra thao tác chuột của người chơi
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.checkForInput(menu_mouse_pos):
                            if button.text_input == "PLAY":
                                self.state = "play"
                            elif button.text_input == "QUIT":
                                pygame.quit()
                                sys.exit()

            pygame.display.update()
    #Phần giao diện khi người chơi chọn play
    def run_play(self):
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
    

    def run(self): 
            while True:
                if self.state == "main_menu":
                    self.run_main_menu()
                elif self.state == "play":
                    self.run_play()
def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_mode((WIDTH,HEIGTH))
    menu = Game(screen)
    menu.add_button(pygame.image.load("../Chevalier/assets/Play Rect.png"), (640, 350), "PLAY", 75, "#d7fcd4", "White")
    menu.add_button(pygame.image.load("../Chevalier/assets/Quit Rect.png"), (640, 500), "QUIT", 75, "#d7fcd4", "White")

    menu.run()

if __name__ == "__main__":
    main()