import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
    def __init__(self,monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_paricles):
        #general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        #graphics setup 
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        # status monster
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        #player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_paricles = trigger_death_paricles
        #invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300
    #đưa hình ảnh vào
    def import_graphics(self,name):
        self.animations = {'idle':[],'move':[],'attack':[]}
        # tạo path dẫn đến foder chứa hình ảnh
        main_path = f'../Chevalier/graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
    #khoảng cách monster và player để quái vật tấn công, đuổi theo nhân vật, và trạng thái nghỉ của quái vật
    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        #thu hep khoang cach khi phat hien nhan vat
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance,direction)
    #check trạng thái khoảng cách monster và player để xét các trường hợp(quái vật tấn công, đuổi theo, và trạng thái nghỉ của quái vật)
    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"
    #hành đông tiến lại gần nhân vật
    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            # print('attack')
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else: 
            self.direction = pygame.math.Vector2()
    #attack cooldown của monster
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        #kiểm tra xem đã đủ thời gian "bất tử" - invincibility_duration hay không. Nếu thời gian kể từ lần cuối bị tấn công (self.hit_time) 
        #đến thời điểm hiện tại (current_time) lớn hơn hoặc bằng thời gian bất tử (self.invincibility_duration),dk thực hiện.
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
    #hoạt ảnh quái vật
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        #tạo nhấp nháy của monster khi bị attack
        if not self.vulnerable:
            #flicker
            alpha = self.wave_value()
            self.image.set_alpha(alpha) 
        else:
            self.image.set_alpha(255)
    #Xác định sát thương và loại sprite. 
    #Tạo phương thức get_damage để xác định sát thương từ người chơi và loại tấn công, cũng như xác định loại sprite để xử lý hủy sprite tương ứng.
    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]    
            #weapon
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            #magic
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_paricles(self.rect.center, self.monster_name)
    # trạng thái đẩy lùi khi bị attack
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
    def update(self):
         self.hit_reaction()
         self.move(self.speed)
         self.animate()
         self.cooldowns()
         self.check_death()
    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
             
    