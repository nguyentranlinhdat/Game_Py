import pygame
from settings import *
from support import import_folder
from entity import Entity
"""class Player  - Khởi tạo đối tượng nhân vật Chevalier. chứa các phương thức khởi tạo hình ảnh hoạt ảnh nhân vật, hành động tấn công của nhân vật"""
class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic) :
        """
        Attributes:
            image (pygame.Surface): Vùng hình ảnh của Nhân vật.
            rect (pygame.Rect): Vùng hình chữ nhật xác định vị trí và kích thước của nhân vật trên màn hình.
            hitbox (pygame.Rect): Hình chữ nhật xác định khu vực va chạm của nhân vật.
            animations (dict): Danh sách các hình ảnh cho các hoạt ảnh khác nhau của nhân vật.
            status (str): Trạng thái hiện tại của nhân vật.
            attacking (bool): Biến đánh dấu xem nhân vật có đang tấn công không.
            attack_cooldown (int): Thời gian hồi chiêu giữa các lần tấn công.
            attack_time (int): Thời điểm cuối cùng nhân vật tấn công. 
            obstacle_sprites (pygame.sprite.AbstractGroup): Nhóm sprite chứa các vật cản của game.
            create_attack (function): Hàm tạo đòn tấn công.
            destroy_attack (function): Hàm hủy đòn tấn công.
            weapon_index (int): index của vũ khí hiện tại mà nhân vật đang giữ.
            weapon (str): Tên của vũ khí.
            can_switch_weapon (bool): Biến đánh dấu xem nhân vật có thể đổi vũ khí không.
            weapon_switch_time (int): Thời điểm cuối cùng nhân vật đổi vũ khí.
            switch_duration_cooldown (int): Thời gian hồi chiêu giữa các lần đổi vũ khí.
            create_magic (function): Hàm tạo ra tấn công phép thuật.
            magic_index (int): index của phép thuật hiện tại nhân vật đang giữ.
            magic (str): Tên của phép thuật.
            can_switch_magic (bool): Biến đánh dấu xem nhân vật có thể đổi phép thuật không.
            magic_switch_time (int): Thời điểm cuối cùng nhân vật đổi phép thuật. 
            stats (dict): Thống kê các thuộc tính: máu, năng lượng, tấn công, phép thuật và tốc độ.
            max_stats (dict): Giá trị tối đa cho các thuộc tính của nhân vật.
            upgrade_cost (dict): Chi phí nâng cấp các thuộc tính của nhân vật.
            health (float): Mức máu hiện tại của nhân vật.
            energy (float): Mức năng lượng hiện tại của nhân vật.
            exp (int): Kinh nghiệm của nhân vật.
            speed (int): Tốc độ di chuyển của nhân vật.
            vulnerable (bool): Biến đánh dấu xem nhân vật có thể bị tấn công không.
            hurt_time (int): Thời điểm cuối cùng nhân vật bị tấn công.
            invulnerability_duration (int): Thời gian miễn nhiễm tấn công sau khi bị tấn công.
            weapon_attack_sound (pygame.mixer.Sound): Âm thanh khi tấn công với vũ khí.
        """
        super().__init__(groups)

        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()  
        self.rect = self.image.get_rect(topleft = pos)

        self.hitbox = self.rect.inflate(-10, HITBOX_OFFSET['player'])
        
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
        self.stats = {'health': 100,'energy':60,'attack': 10,'magic': 4,'speed': 5}
        self.max_stats = {'health': 300,'energy':140,'attack': 20,'magic': 10,'speed': 10}
        self.upgrade_cost = {'health': 100,'energy':100,'attack': 100,'magic': 100,'speed': 100}
        self.health = self.stats['health'] *0.5
        self.energy = self.stats['energy'] *0.8
        self.exp = 0
        self.speed = self.stats['speed']

        #damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        #import a sound
        self.weapon_attack_sound = pygame.mixer.Sound('audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.8)


    #hoạt ảnh nhân vật khi tương tác phím 
    def import_player_assets(self):
        """def import_player_assets load tất cả hoạt ảnh đồ hoạ của nhân vật"""
        character_path = 'graphics/player/'

        self.animations = {'up': [],'down': [],'left': [],'right': [],
            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
            'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        """def input()  Xử lý các sự kiện đầu vào từ bàn phím của người chơi và thực hiện các hành động tương ứng của nhân vật."""
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

                self.weapon_attack_sound.play()
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
        """ get_status() Kiểm tra, cập nhật trạng thái hiện tại của nhân vật dựa trên hướng di chuyển và hành động tấn công.
            Kiểm tra trạng nghỉ và tấn công nhân vật tránh trường hợp bị chồng hoạt ảnh
        """
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
        """def cooldowns():Cập nhật thời gian hồi chiêu và thời gian có thể đổi vũ khí/phép thuật của nhân vật.
        tránh trường hợp người chơi tấn côn liên tục.
        """
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
        """def animate(): Cập nhật hoạt ảnh của người chơi dựa trên trạng thái hiện tại và thời gian.
            Sử dụng vòng lập để load các hoạt ảnh của nhân vật.
            Hiệu ứng nhấp nháy của nhân vật.
        """
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
        """def get_full_weapon_damage(): Tính toán xác thương gây ra bằng vũ khí
            Sát thương = lượng sát thương mặc định + sát thương từ vũ khí
        """
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage
    
    def get_value_by_index(self,index):
        """def get_value_by_index(): Trả về giá trị của một thuộc tính của người chơi dựa trên chỉ số."""
        return list(self.stats.values())[index]
    def get_cost_by_index(self,index):
        """def get_cost_by_index(): Trả về chi phí nâng cấp của một thuộc tính của người chơi dựa trên chỉ số."""
        return list(self.upgrade_cost.values())[index]

    #hồi năng lượng theo thời gian
    def energy_recovery(self):
        """def energy_recovery(): Hồi phục năng lượng của người chơi theo thời gian."""
        if self.energy <=self.stats['energy']:
            self.energy += 0.05 * self.stats['magic']
        else:
            self.energy = self.stats['energy']
    def get_full_magic_damage(self):
        """get_full_magic_damage: Tính toán xác thương gây ra bằng phép
            Sát thương = lượng sát thương mặc định + sát thương phép
        """
        base_damage = self.stats['magic']
        magic_damage = magic_data[self.magic]['strength']
        return base_damage + magic_damage

    def update(self):
        """def update(): cập nhật các trạng thái hoạt động của người chơi"""
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()