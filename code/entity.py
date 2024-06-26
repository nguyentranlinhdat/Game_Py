import pygame
from math import sin 
"""class Entity: Xây dựng phương thức di chuyển cho các đối tượng quái vật và nhân vật"""
class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    # di chuyển của nhân vật   
    def move(self, speed):
        """def move(): di chuyển của đối tượng theo hướng cùng với tốc độ di chuyển"""
        # điều chỉnh tốc độ di chuyển chéo ở mức bình thường
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x *speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y *speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """ def collision(): Xử lý va chạm giữa đối tượng và các vật cản.
            Va chạm ngang và qua chạm dọc
        """
        #kiểm tra va chạm ngang
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #di chuyển sang phải
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #di chuyển sang phải
                        self.hitbox.left = sprite.hitbox.right
        #kiểm tra va chạm dọc
        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #di chuyển xuống 
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #di chuyển lên
                        self.hitbox.top = sprite.hitbox.bottom
    
    def wave_value(self):
        """def wave_value():  Tạo sóng sin cho hiệu ứng nhấp nháy."""
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0