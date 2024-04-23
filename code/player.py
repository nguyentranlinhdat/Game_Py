import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic) :
        super().__init__(groups)

        self.image = pygame.image.load('../Chevalier/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26)
        #graphics setup
        self.import_player_assets()
        self.status = 'down'

        #movement
        #thiết lập thời gian ra chiêu
        #Tạo 1 biến attacking tránh trường hợp sử dụng tấn công và phép thuật cùng 1 lúc
        self.attacking = False
        self.attack_cooldown = 400 # milisecons
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        #weapon 
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        #duyệt các phần tử weapong có trong data (file setting)
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index] 
        # print(self.weapon)   
        #change weapone
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        #tốc độ ra chiêu tuỳ theo độ nặng của vũ khí (giả xử axe nặng hơn sword => ra chiêu chậm hơn) cooldown thời gian thay đổi
        self.switch_duration_cooldown = 200

        #magic 
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        #stats
        self.stats = {'health': 100,'energy':60,'attack': 10,'magic': 4,'speed': 7}
        self.health = self.stats['health'] *0.5
        self.energy = self.stats['energy'] *0.8
        self.exp = 123
        self.speed = self.stats['speed']

        #damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500


    #hoạt ảnh nhân vật khi tương tác phím 
    def import_player_assets(self):
        character_path = '../Chevalier/graphics/player/'
        self.animations = {'up': [],'down': [],'left': [],'right': [],
            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
            'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        """
        WSAD để di chuyển
        Q để chuyển đổi vũ khí
        E để chuyển đổi phép
        J để tấn công bằng vũ khí
        K để dùng phép
        """
        #tránh người chơi đổi hướng trong thời gian tung chiêu
        if not self.attacking:
            # Thiết lập các nút di chuyển
            keys = pygame.key.get_pressed()
            # lên, xuống    
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0
            # phải trái
            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0
    
            #attack input
            if keys[pygame.K_j]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            # magic input
            if keys[pygame.K_k]:
            
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)
    
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index +=1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index +=1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index] 
            
    def get_status(self):
        #trang thái nghỉ
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + "_idle"
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    # overwrite idle
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace("_attack","")

    
    #thời gian hồi chiêu của đòn tấn công
    def cooldowns(self):
        # thực hiện việc đo lường time
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
    def animate(self):
        animation = self.animations[self.status]
        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        #set the image
        self.image = animation[int(self.frame_index)]
        #set khung hoạt ảnh thành 1 khung hình chung
        self.rect = self.image.get_rect(center = self.hitbox.center)

        #flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    # Tính sát thương đầu ra = sát thương cơ bản + sát thương từ vũ khí
    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage
    #hồi năng lượng theo thời gian
    def energy_recovery(self):
        if self.energy <=self.stats['energy']:
            self.energy += 0.02 * self.stats['magic']
        else:
            self.energy = self.stats['energy']
    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        magic_damage = magic_data[self.magic]['strength']
        return base_damage + magic_damage

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()