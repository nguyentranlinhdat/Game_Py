import pygame 
from settings import *
""" class UI - Xây dựng giao diện thanh máu, thanh năng lượng, số kinh nghiệm, ô thay đổi vũ khí/phép thuật"""

class UI:
    def __init__(self):
        """ Attributes:
            font: Font chữ được sử dụng cho văn bản trên giao diện.
            health_bar_rect: vùng hình chữ nhật đại diện cho thanh máu.
            energy_bar_rect: vùng hình chữ nhật đại diện cho thanh năng lượng.
            weapon_graphics: Danh sách hình ảnh các loại vũ khí.
            magic_graphics: Danh sách hình các loại phép thuật."""
        #general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        #bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH, BAR_HEIGHT)
        
        #convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
        
        #convert weapon dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            magic = pygame.image.load(magic['graphic']).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        """def show_bar() hiển thị thanh trạng thái (thanh máu và năng lượng)
            current: Giá trị hiện tại của thanh.
            max_amount: Giá trị tối đa của thanh.
            bg_rect: Vùng hình chữ nhật đại diện cho phần nền của thanh.
            color: Màu của thanh.
        """
        #draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        #converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
    def show_exp(self, exp):
        """def show_exp(): hiển thị ô kinh nghiệm"""
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        #vị trí của ô EXP (góc dưới phải màn, hình cách màn 20px)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))
        # background của exp
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf, text_rect)
        # border của exp
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20), 3)
        
    # selection box of the weapon and magic
    def selection_box(self, left, top, has_switched):
        """def selection_box() Hiện thị ô vuông  chọn vũ khí và phép thuật, tạo highlight khi chuyển đổi"""
        # tạo box (hình vuông) và bg
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)    

        # create Highlight when change weapon
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)    
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)  
        return bg_rect 

    # swap weapon
    def weapon_overlay(self, weapon_index, has_switched):
        """def weapon_overlay() Hiển thị hình ảnh vũ khí thay đổi khi thay đổi trong ô vuông"""
        bg_rect = self.selection_box(10, 630, has_switched) #weapon
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    #swap magic
    def magic_overlay(self, magic_index, has_switched):
        """def magic_overplay() Hiển thị hình ảnh của phép khi thay đổi trong ô vuông"""
        bg_rect = self.selection_box(80, 635, has_switched) #magic
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        """def display(): hiển thị tất cả các phần giao diện trên màn hình"""
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        
        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
        # self.selection_box(80, 635) #magic