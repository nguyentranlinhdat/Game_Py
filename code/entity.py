import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    # di chuyển của nhân vật   
    def move(self, speed):
        # điều chỉnh tốc độ di chuyển chéo ở mức bình thường
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x *speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y *speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
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