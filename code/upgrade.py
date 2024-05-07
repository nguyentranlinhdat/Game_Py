from settings import *
import pygame
"""class Upgrade: xây dụng menu nâng cấp cho nhân vật trong game"""
class Upgrade:
    def __init__(self, player):
        """Attribute:
        attribute_nr: Số lượng thuộc tính để nâng cấp.
        attribute_names: Danh sách tên thuộc tính.
        max_values: Danh sách giá trị tối đa cho mỗi thuộc tính.
        font: Font cho việc hiển thị văn bản.
        height: Chiều cao của menu upgrade.
        width: Chiều rộng của mỗi box thuộc tính nâng cấp.
        selection_index: index của box nâng cấp được chọn.
        selection_time: Thời gian lựa chọn(cooldown di chuyển các box).
        can_move: cờ lệnh có thể di chuyển trong menu nâng cấp.
        """
        #general setup:
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        #item dimensions
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()
        #selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
    #thiết lập nút di chuyển và nâng cấp trong phần menu Up
    def input(self):
        """def input(): Xử lý tín hiệu đầu vào người chơi để điều hướng và kích hoạt nâng cấp trong menu."""
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr -1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                # print(self.selection_index)
                self.item_list[self.selection_index].trigger(self.player)
    #thời gian dừng, tránh việc thao tác quá nhanh
    def selection_cooldown(self):
        """def selection_cooldown(): Cơ chế cooldown để tránh thay đổi box quá nhanh của người chơi"""
        if not self.can_move:
            current_time =pygame.time.get_ticks()
            if current_time - self.selection_time >= 200:
                self.can_move = True
    #
    def create_items(self):
        """def create_items(): Xây dựng các box của các thuộc tính cần năng cấp"""
        self.item_list = []
        for item, index in enumerate(range(self.attribute_nr)):
            #horizontal positions
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + (increment - self.width) // 2
            #vertical position
            top = self.display_surface.get_size()[1] * 0.1
            #create the object
            item = Item(left, top, self.width, self.height, index ,self.font)
            self.item_list.append(item)
    #Giao diện hiển thị phần menu Up   
    def display(self):
        """def display(): Giao diện hiển thị phần menu Up  """
        # self.display_surface.fill('black')
        self.input()
        self.selection_cooldown()
        for index, item  in enumerate(self.item_list):
            #get attribute
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)
#Khởi tạo class Item chứa các box của thuộc tính cần nâng cấp
class Item:
    """class Item: Khởi tạo class Item chứa các box của thuộc tính cần nâng cấp"""
    def __init__(self, l, t, w, h, index, font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font
    def display_names(self, surface, name, cost, selected):
        """def display_names(): Hiển thị tên các thuộc tính nâng cấp trên màn hình."""
        color = TEXT_COLOR_SELECTED if  selected else TEXT_COLOR
        #title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        #cost
        cost_surf = self.font.render(f'{int(cost)}', False, color)
        cost_rect = title_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0, 20))
        #draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)
    #line
    def display_bar(self, surface, value, max_value, selected):
        """ def display_bar() hiển thị đường thẳng biểu diễn thuộc tính đã nâng cấp"""
        #drawing setup
        top= self.rect.midtop + pygame.math.Vector2(0,60)
        bottom= self.rect.midbottom - pygame.math.Vector2(0,60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR
        #bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value/max_value) * full_height
        value_rect = pygame.Rect(top[0]-15, bottom[1] - relative_number, 30, 10)
        #draw elements
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)
    #Hàm trigger thay đổi(nâng cấp) các thuọc tính khi nhận input cần nâng cấp
    def trigger(self, player):
        """def trigger(): thay đổi(nâng cấp) các thuộc tính khi nhận input cần nâng cấp"""
        upgrade_attribute = list(player.stats.keys())[self.index]
        # print(upgrade_attribute)
        if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4    
        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]
    #Giao diện khung viền của box thuộc tính
    def display(self, surface, selection_num, name, value, max_value, cost):
        """def display(): Giao diện khung viền của box thuộc tính"""
        #highlight
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface,name, cost, self.index == selection_num)
        self.display_bar(surface,value, max_value, self.index == selection_num)