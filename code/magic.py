import pygame
from settings import *
from random import randint
"""class Magic tạo chức năng sử dụng phép thuật"""
class MagicPlayer:
    def __init__(self, animation_player):
        """Khởi tạo đối tượng MagicPlayer
            animation_player (AnimationPlayer): Đối tượng AnimationPlayer được sử dụng để tạo hiệu ứng
        """
        self.animation_player = animation_player
        self.sounds = {
		'heal': pygame.mixer.Sound('../Chevalier/audio/heal.wav'),
		'flame':pygame.mixer.Sound('../Chevalier/audio/Fire.wav')
		}
    def heal(self, player, strength, cost, groups):
        """def heal(): Kỹ năng hồi máu:
           Parameters:
            player (Player): Đối tượng Player cần hồi phục.
            strength (int): Lượng máu được hồi phục.
            cost (int): Năng lượng tiêu hao khi sử dụng
            groups (list): Danh sách hiệu ứng.
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
         def flame() Kỹ năng phóng lửa,
        Parameters:
            player (Player): Đối tượng Player thực hiện kỹ năng.
            cost (int): Năng lượng tiêu hao .
            groups (list): Danh sách hiệu ứng.
        """
        """ xác định hướng phóng"""
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
            """Tạo hiệu ứng phóng"""
            for i in range(1, 6):
                if direction.x:
                    #horizontal - ngang
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE//3, TILESIZE//3)
                    y = player.rect.centery + randint(-TILESIZE//3, TILESIZE//3)
                    self.animation_player.create_particles('flame',(x, y), groups)
                else:
                    #vertical - dọc
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE//3, TILESIZE//3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE//3, TILESIZE//3)
                    self.animation_player.create_particles('flame',(x, y), groups)


        
    