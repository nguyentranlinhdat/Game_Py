import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer

from magic import MagicPlayer
from upgrade import Upgrade

"""Khởi tạo lớp quản lí việc tạo map, quản lí hành động, tương tác của các sprite"""
class Level:
    """
      Attribute:

        game_paused (bool): Trạng thái của trò chơi, có đang tạm dừng hay không.
        visible_sprites (YSortCameraGroup): Nhóm sprite có thể nhìn thấy được trên màn hình.
        obstacle_sprites (Group): Nhóm sprite là vật cản không thể xuyên qua.
        current_attack (Weapon): Vũ khí hiện tại của nhân vật.
        attack_sprites (Group): Nhóm sprite tấn công.
        attackable_sprites (Group): Nhóm sprite có thể bị tấn công.
        ui (UI): Giao diện người dùng.
        upgrade (Upgrade): Cửa sổ nâng cấp.
        animation_player (AnimationPlayer): Hoạt ảnh nhân vật.
        magic_player (MagicPlayer): Quản lý phép của nhân vật.
    Phương thức:
        create_map(): Tạo bản đồ cấp độ từ các tệp layout và graphics.
        create_attack(): Tạo hoạt ảnh tấn công.
        destroy_attack(): Hủy hoạt ảnh tấn công hiện tại.
        create_magic(style, strength, cost): Tạo hiệu ứng phép.
        player_attack_logic(): Xử lý logic tấn công của nhân vật với các sprite khác.
        damage_player(amount, attack_type): Gây sát thương cho nhân vật.
        trigger_death_paricles(pos, particle_type): Kích hoạt hiệu ứng sau khi một sprite chết hoặc phá hủy.
        add_exp(amount): Cộng điểm kinh nghiệm cho nhân vật sau khi tiêu diệt một quái vật.
        toggle_menu(): Chuyển đổi trạng thái tạm dừng của trò chơi và hiển thị hoặc ẩn menu nâng cấp.
        run(): Cập nhật trạng thái và hiển thị trò chơi.
    """
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # sprite group setup
        self.visible_sprites =YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        # attack sprite
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        #mục tiêu có thể bị tấn công
        self.attackable_sprites = pygame.sprite.Group()

        #sprite setup
        self.create_map()

        #user_interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        #particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)


    def create_map(self):
        """def create_map():
        Dựa vào các file csv được tạo ra bởi Tiled để tiến hành duyệt các phần tử để hiển thị chúng theo vị trí tương ứng trên bản đồ
        Đối với boundary thì cần phải ẩn chúng đi vì nó không cần thiết trong việc hiển thị hình ảnh của bản đồ"""
        layouts = {
            'boundary': import_csv_layout("map/map_FloorBlocks.csv"),
            'grass': import_csv_layout("map/map_Grass.csv"),
            'object': import_csv_layout("map/map_Objects.csv"),
            'entities': import_csv_layout("map/map_Entities.csv")

        }
        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [ self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'grass', random_grass_image)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                        #tạo sự xuất hiện của các loại monster với các số tương ứng, phù hợp đã thiết lập ở file csv
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                        (1020,2310),
                                        [self.visible_sprites],
                                        self.obstacle_sprites,
                                        self.create_attack,
                                        self.destroy_attack,
                                        self.create_magic)

                            else:
                                if col == '390': monster_name = 'cyclope'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name ='raccoon'
                                else: monster_name = 'squid'
                                Enemy(
                                    monster_name,
                                    (x, y), 
                                    [self.visible_sprites, self.attackable_sprites], 
                                    self.obstacle_sprites,
                                    self.damage_player,

                                    self.trigger_death_paricles,
                                    self.add_exp)

    def create_attack(self):
        """def create_attack(): tạo đòn tấn công weapon"""
        self.current_attack = Weapon(self.player,[self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.create_attack = None
    
    def create_magic(self, style, strength, cost):
        """def create_magic() Xây dựng hàm tạo đòn tấn công từ class weapon:"""
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])    

    # Xử lý va chạm giữa các sprite. 
    def player_attack_logic(self):
        """ def player_attack_logic(): Xử lý va chạm giữa các sprite. Kiểm tra va chạm giữa các sprite và xác định xem sprite nào bị tấn công sẽ bị hủy bỏ (cỏ)."""
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                #Sử dụng pygame.sprite.spritecollide() để kiểm tra va chạm giữa các sprite và xác định xem sprite nào bị tấn công sẽ bị hủy bỏ (cỏ).
                collision_sprite = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprite:
                    for target_sprite in collision_sprite:
                        #mục tiêu phá huỷ "cỏ"
                        if target_sprite.sprite_type == 'grass':
                            #hiệu ứng khi cỏ bị diệt
                            pos = target_sprite.rect.center
                            #thêm kích thước cho hiệu ứng bit
                            offset = pygame.math.Vector2(0,75)
                            #tăng số lượng hiệu ứng lá rơi ra từ 3-6 lá
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    # Nhân vật nhận sát thương
    def damage_player(self, amount, attack_type):
        """
        def damage_player(): nhận sát thương của nhân vật. Khi bị tấn công nhân vật sẽ bị mất máu đồng thời hình ảnh của nhân vật sẽ nhấp nháy
        Máu của nhân vật sẽ bị trừ đi bằng với lượng sát thương nhận phải từ quái vật.
        Đối số:
            amount (int): Lượng sát thương.
            attack_type (str): Loại tấn công.
        """
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            #spawn pariticles
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    # Gọi animation player để tạo hiệu ứng sau khi chết
    def trigger_death_paricles(self, pos, particle_type):

        """ def trigger_death_paricles(): Tạo hiệu ứng hạt bằng cách gọi animation player"""
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)
  # Cộng điểm exp khi tiêu diệt monster
    def add_exp(self, amount):
        """def add_exp() cộng điểm exp khi tiêu diệt monster"""
        self.player.exp += amount

    def toggle_menu(self):
        """def toggle_menu(): Dừng game mở menu updrae game"""
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
            #display updrate menu
        else:
            #run the game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            

        #update and raw the game
        # debug(self.player.direction)
        # debug(self.player.status)
        
""" class YSortCameraGroup()
    Một lớp để quản lý các sprite trong một khung nhìn camera với sắp xếp theo trục Y.
    Lớp này mở rộng chức năng của pygame.sprite.Group để xử lý các sprite trong một khung nhìn camera
    với sắp xếp theo trục Y để vẽ đúng vị trí. Được thiết kế đặc biệt cho các trò chơi 2D nơi camera
    theo dõi một nhân vật chính và các sprite được sắp xếp dựa trên tọa độ Y của họ để vẽ đúng."""
class YSortCameraGroup(pygame.sprite.Group):
    """
    Thuộc tính:
        display_surface (Surface): Bề mặt mà các sprite được vẽ lên.
        half_width (int): Nửa chiều rộng của bề mặt hiển thị.
        half_height (int): Nửa chiều cao của bề mặt hiển thị.
        offset (Vector2): Phần dời được sử dụng để điều chỉnh vị trí của các sprite so với khung nhìn camera.
        floor_surf (Surface): Bề mặt biểu diễn hình nền/sàn.
        floor_rect (Rect): Hình chữ nhật biểu diễn vị trí và kích thước của bề mặt sàn.

    Phương thức:
        custom_draw(player): Vẽ các sprite lên bề mặt hiển thị với sắp xếp theo trục Y.
        enemy_update(player): Cập nhật các sprite kẻ địch dựa trên vị trí của nhân vật.

    """
    def __init__(self):

        """ 
        Thuộc tính:
        display_surface (Surface): Bề mặt mà các sprite được vẽ lên.
        half_width (int): Nửa chiều rộng của bề mặt hiển thị.
        half_height (int): Nửa chiều cao của bề mặt hiển thị.
        offset (Vector2): Phần dời được sử dụng để điều chỉnh vị trí của các sprite so với khung nhìn camera.
        floor_surf (Surface): Bề mặt biểu diễn hình nền/sàn.
        floor_rect (Rect): Hình chữ nhật biểu diễn vị trí và kích thước của bề mặt sàn.
        Phương thức:
        custom_draw(player): Vẽ các sprite lên bề mặt hiển thị với sắp xếp theo trục Y.
        enemy_update(player): Cập nhật các sprite kẻ địch dựa trên vị trí của nhân vật."""
        #general setup

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2 
        self.half_height = self.display_surface.get_size()[1] // 2    
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load("graphics/tilemap/ground.png")
        self.floor_rect = self.floor_surf.get_rect(topleft =(0,0))

    def custom_draw(self, player):
        """ def custom_draw(): Vẽ các sprite lên bề mặt hiển thị với sắp xếp theo trục Y.
        Đối số:
            player (Sprite): Sprite nhân vật được sử dụng để tính toán khung nhìn camera.

        """
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprites: sprites.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
    def enemy_update(self,player):
        """

        def enemy_update():

        Cập nhật các sprite quái vật dựa trên vị trí của nhân vật.
        Kẻ địch sẽ di chuyển về phía nhân vật và tấn công nhân vật khi nhân vật lại gần
        Đối số:
            player (Sprite): Sử dụng nhân vật để tính toán hành vi của quái vật.
        """
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)