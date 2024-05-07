"""class Weapon có chức năng khởi tạo vũ khí, hiển thị vũ khí ra màn hình theo các hướng tấn công tương ứng"""

import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        """ Load hình ảnh tạo ra vũ khí khi tấn công.
            Sử dụng math.Vector để thiết lập hướng tấn công. Hiển thị ảnh phù hợp với hướng của nhân vật
            Attributes:
            sprite_type (str): Loại sprite, trong trường hợp này là 'weapon'.
            image (pygame.Surface): Hình ảnh của vũ khí.
            rect (pygame.Rect): Hình chữ nhật xác định vị trí và kích thước của vũ khí trên màn hình.
        """
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split("_")[0]
        # print(direction)
        #graphic
        #load ảnh vũ khí khi tấn công
        full_path = f'graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        # self.image = pygame.Surface((40,40))
        #placement
        # sử dụng math vector đê thiết lập hướng tấn công
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-8,0))
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))
help(Weapon)

