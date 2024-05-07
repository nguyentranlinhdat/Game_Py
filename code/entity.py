import pygame
from math import sin 
"""class Entity: Xây dựng phương thức di chuyển cho các đối tượng quái vật và nhân vật"""
class Entity(pygame.sprite.Sprite):
    """
    Lớp này đại diện cho một thực thể trong trò chơi (nhân vật, quái vật) với khả năng di chuyển và phát hiện va chạm.
    Lớp này kế thừa từ `pygame.sprite.Sprite` và cung cấp các chức năng bổ sung để quản lý việc di chuyển và va chạm của thực thể.

    Thuộc tính:
        groups (pygame.sprite.Group): Danh sách các nhóm mà thực thể thuộc về.
        frame_index (int): Chỉ số khung hình hiện tại được sử dụng cho hoạt hình (bắt đầu từ 0).
        animation_speed (float): Tốc độ hoạt ảnh.
        direction (pygame.math.Vector2): Hướng di chuyển của thực thể dưới dạng vector.
        hitbox (pygame.Rect): Hình chữ nhật va chạm của thực thể để phát hiện va chạm.
        obstacle_sprites (pygame.sprite.Group): Nhóm các sprite đại diện cho chướng ngại vật để phát hiện va chạm.

    Phương thức:
        __init__(self, groups):
            Khởi tạo thực thể với các nhóm được chỉ định.
        move(self, speed):
            Di chuyển thực thể dựa trên hướng và tốc độ của nó, xử lý chuyển động chéo và phát hiện va chạm.
        collision(self, direction):
            Kiểm tra va chạm với chướng ngại vật theo hướng được chỉ định ("ngang" hoặc "dọc") và điều chỉnh vị trí của thực thể nếu cần thiết.
        wave_value(self):
            Trả về giá trị dao động giữa 255 và 0 dựa trên thời gian hiện tại, có thể hữu ích cho hiệu ứng hình ảnh hoặc hoạt hình.
    """
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        self.hitbox = pygame.Rect(0, 0, 0, 0)  # Giả sử bạn khởi tạo hitbox ở nơi khác
        self.obstacle_sprites = None

    # Di chuyển của nhân vật   
    def move(self, speed):
        # Điều chỉnh tốc độ di chuyển chéo ở mức bình thường
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x *speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y *speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        # Kiểm tra va chạm ngang
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # Di chuyển sang phải
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # Di chuyển sang phải
                        self.hitbox.left = sprite.hitbox.right
        # Kiểm tra va chạm dọc
        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # Di chuyển xuống 
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # Di chuyển lên
                        self.hitbox.top = sprite.hitbox.bottom
    
    def wave_value(self):
        """def wave_value():  Tạo sóng sin cho hiệu ứng nhấp nháy."""
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0