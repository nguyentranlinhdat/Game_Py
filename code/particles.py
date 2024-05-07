import pygame
from support import import_folder
from random import choice

class AnimationPlayer:
    """
    Lớp này quản lý việc tạo và phát các hiệu ứng hạt trong trò chơi.

    Thuộc tính:
        frames (dict): Từ điển chứa các khung hình hoạt hình được tải trước cho các hiệu ứng hạt khác nhau.
            - Khóa: Chuỗi đại diện cho các loại hoạt hình (ví dụ: "flame", "claw", "leaf").
            - Giá trị: Danh sách các đối tượng pygame.Surface đại diện cho các khung hình hoạt hình.

    Phương thức:
        __init__(self): Tải tất cả các khung hình hoạt hình hạt từ các thư mục được chỉ định.

        reflect_images(self, frames): Tạo phiên bản phản chiếu của các khung hình hoạt hình được cung cấp (lật theo chiều ngang).

        create_grass_particles(self, pos, groups): Tạo hiệu ứng hạt "lá" ngẫu nhiên tại vị trí đã cho.

        create_particles(self, animation_type, pos, groups):
            Tạo hiệu ứng hạt của loại hoạt hình được chỉ định (ví dụ: "flame", "slash") tại vị trí đã cho.
    """
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_folder('graphics/particles/flame/frames'),
            'aura': import_folder('graphics/particles/aura'),
            'heal': import_folder('graphics/particles/heal/frames'),
            
            # attacks 
            'claw': import_folder('graphics/particles/claw'),
            'slash': import_folder('graphics/particles/slash'),
            'sparkle': import_folder('graphics/particles/sparkle'),
            'leaf_attack': import_folder('graphics/particles/leaf_attack'),
            'thunder': import_folder('graphics/particles/thunder'),

            # monster deaths
            'squid': import_folder('graphics/particles/smoke_orange'),
            'raccoon': import_folder('graphics/particles/raccoon'),
            'spirit': import_folder('graphics/particles/nova'),
            'cyclop': import_folder('graphics/particles/smoke2'),
            
            # leafs 
            'leaf': (
                import_folder('graphics/particles/leaf1'),
                import_folder('graphics/particles/leaf2'),
                import_folder('graphics/particles/leaf3'),
                import_folder('graphics/particles/leaf4'),
                import_folder('graphics/particles/leaf5'),
                import_folder('graphics/particles/leaf6'),
                self.reflect_images(import_folder('graphics/particles/leaf1')),
                self.reflect_images(import_folder('graphics/particles/leaf2')),
                self.reflect_images(import_folder('graphics/particles/leaf3')),
                self.reflect_images(import_folder('graphics/particles/leaf4')),
                self.reflect_images(import_folder('graphics/particles/leaf5')),
                self.reflect_images(import_folder('graphics/particles/leaf6'))
                )
            }
    
    #sử dụng để tạo các hình ảnh phản chiếu của các frame trong danh sách frames
    def reflect_images(self,frames):
        #Hình ảnh phản chiếu sẽ được tạo bằng cách lật frame theo trục x (hoặc y tùy chọn).
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame,True,False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self,pos,groups):
        # Lấy khung hình hoạt ảnh từ self.frames
        animation_frames = choice(self.frames['leaf'])
        # Tạo hiệu ứng hạt cỏ
        ParticleEffect(pos,animation_frames,groups)

    def create_particles(self,animation_type,pos,groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos,animation_frames,groups)

#Hiệu ứng hạt
class ParticleEffect(pygame.sprite.Sprite):
    """
    Lớp này đại diện cho một hiệu ứng nhỏ trong trò chơi.

    Thuộc tính:
        sprite_type (str): Loại hiệu ứng hạt (ví dụ: "magic").
        frame_index (int): Chỉ số khung hình hiện tại.
        animation_speed (float): Tốc độ hoạt hình (giá trị thấp hơn = chậm hơn).
        frames (list of pygame.Surface): Danh sách các khung hình hoạt hình cho hiệu ứng hạt.
        image (pygame.Surface): Khung hình hoạt hình hiện tại đang được hiển thị.
        rect (pygame.Rect): Hình chữ nhật bao quanh hình ảnh (dựa trên tâm của hình ảnh).

    Phương thức:
        __init__(self, pos, animation_frames, groups): Khởi tạo hiệu ứng hạt với vị trí ban đầu, các khung hình hoạt hình và nhóm sprite.
        animate(self):
            - Cập nhật chỉ số khung hình và thay đổi hình ảnh hiển thị tương ứng.
            - Nếu hết khung hình, hiệu ứng sẽ tự hủy.
        update(self): Gọi phương thức animate để cập nhật hiệu ứng.
    """

    def __init__(self,pos,animation_frames,groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
