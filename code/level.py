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

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

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

        #user_interfaceq
        self.ui = UI()

        #particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)


    def create_map(self):
        layouts = {
            'boundary': import_csv_layout("../Chevalier/map/map_FloorBlocks.csv"),
            'grass': import_csv_layout("../Chevalier/map/map_Grass.csv"),
            'object': import_csv_layout("../Chevalier/map/map_Objects.csv"),
            'entities': import_csv_layout("../Chevalier/map/map_Entities.csv")

        }
        graphics = {
            'grass': import_folder('../Chevalier/graphics/grass'),
            'objects': import_folder('../Chevalier/graphics/objects')
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
                                        (x,y),
                                        [self.visible_sprites],
                                        self.obstacle_sprites,
                                        self.create_attack,
                                        self.destroy_attack,
                                        self.create_magic)
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name ='raccoon'
                                else: monster_name = 'squid'
                                Enemy(
                                    monster_name,
                                    (x, y), 
                                    [self.visible_sprites, self.attackable_sprites], 
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_paricles)

        #         if col == "x":
        #             Tile((x, y),[self.visible_sprites,self.obstacle_sprites])
        #         if col == "p":
        #            self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites)

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.create_attack = None
    
    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])    

    # Xử lý va chạm giữa các sprite. 
    def player_attack_logic(self):
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

    #Nhân vật nhận sát thương
    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            #spawn pariticles
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    # Gọi animation player để tạo hiệu ứng sau khi chết
    def trigger_death_paricles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def run(self):
        #update and raw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2 
        self.half_heigth = self.display_surface.get_size()[1] // 2    
        self.offset = pygame.math.Vector2()

        #creating the floor
        self.floor_surf = pygame.image.load("../Chevalier/graphics/tilemap/ground.png")
        self.floor_rect = self.floor_surf.get_rect(topleft =(0,0))

    def custom_draw(self, player):
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_heigth
        
        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprites: sprites.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)