import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic) :
        super().__init__(groups)

        self.image = pygame.image.load('../Chevalier/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26)
        #graphics setup
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        #movement
        self.direction = pygame.math.Vector2()
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
        #tránh người chơi đổi hướng trong thời gian tung chiêu
        if not self.attacking:
            # Thiết lập các nút di chuyển
            keys = pygame.key.get_pressed()
            # lên, xuống    
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0
            # phải trái
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0
    
            #attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            # magic input
            if keys[pygame.K_LCTRL]:
            
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
    #thời gian hồi chiêu của đòn tấn công
    def cooldowns(self):
        # thực hiện việc đo lường time
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
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


    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)