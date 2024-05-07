import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    """class tile: chức năng tạo các ô vuông với các loại sprite khác nhau như player, grass,...
    Có khả năng xác định vị trí của các sprite trên bản đồ
    xử lý va chạm giữa các sprite và xác định hành động tương ứng, ví dụ như phá hủy grass hoặc giảm máu của enemy.
    """
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))) : 
        super().__init__(groups)
        self.sprite_type = sprite_type
        y_offset = HITBOX_OFFSET[sprite_type]
        self.image = surface
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, y_offset)