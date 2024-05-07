import pygame
from settings import *
from random import randint
class MagicPlayer:
    """
    Lớp để tạo ra phép cho nhân vật
    Thuộc tính:
        animation_player (AnimationPlayer): Tham chiếu đến lớp AnimationPlayer để tạo hiệu ứng của phép.
        sounds (dict): Từ điển chứa hiệu ứng âm thanh cho các phép thuật.
    Phương thức:
        heal(self, player, strength, cost, groups): Phép hồi máu cho nhân vật với lượng máu nhất định nếu có đủ năng lượng.
        flame(self, player, cost, groups): Thi triển phép lửa theo hướng nhân vật đang đối mặt.
    """
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
		'heal': pygame.mixer.Sound('audio/heal.wav'),
		'flame':pygame.mixer.Sound('audio/Fire.wav')
		}
    def heal(self, player, strength, cost, groups):
        """
        Hồi máu cho nhân vật và tạo hiệu ứng hồi phục.
        Khi còn năng lượng, có thể thi triển phép
        Phát âm thanh hiệu ứng tương ứng.
        Hồi máu của nhân vật bằng mức độ được chỉ định.
        Đảm bảo máu của nhân vật không vượt quá máu tối đa được xác định trong thuộc tính của người chơi.
        Tạo ra các hạt hiệu ứng 'aura' tại vị trí trung tâm của người chơi.
        Tạo ra các hạt hiệu ứng 'heal' tại vị trí trung tâm của nhân vật với một vị trí dịch chuyển y lệch lên trên.

        Tham số:
            self (object): Thể hiện của lớp chứa phương thức này.
            player (object): Đối tượng của nhân vật cần được hồi phục máu.
            strength (int): Sức mạnh của sự hồi phục, tức là số lượng máu được tăng thêm cho người chơi.
            cost (int): Chi phí năng lượng cần thiết để thi triển.
            groups (pygame.sprite.Group): Một nhóm chứa các nhóm sprite để thêm các hạt hiệu ứng vào.
        """
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal',player.rect.center + pygame.math.Vector2(0, -40), groups)

    def flame(self, player, cost, groups):
        """
        Thi triển phép lửa theo hướng chỉ định
        Nếu nhân có đủ năng lượng, thi triển phép
        Phát âm thanh hiệu ứng tương ứng của phép.
        Xác định hướng của ngọn lửa dựa trên trạng thái hiện tại của người chơi.
        Tạo ra các hạt lửa theo hướng chỉ định lên đến khoảng cách 6 ô.
        Các hạt lửa được tạo ra tại các vị trí ngẫu nhiên trong khu vực gần vị trí của người chơi.

        Tham số:
            player (object): Đối tượng của nhân vật khởi tạo hiệu ứng lửa.
            cost (int): Chi phí năng lượng cần thiết để thực hiện hành động lửa.
            groups (pygame.sprite.Group): Một nhóm chứa các nhóm sprite để thêm các hạt lửa vào.
        """
        if player.energy >= cost:
            player.energy -= cost
            self.sounds['flame'].play()
            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0,-1)
            else:
                direction = pygame.math.Vector2(0,1)
            for i in range(1,6):
                if direction.x: #horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame',(x,y),groups)
                else: # vertical
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame',(x,y),groups)