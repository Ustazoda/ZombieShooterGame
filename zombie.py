# zombie.py

import pygame
from settings import *
import random

class Zombie:
    """
    Zombie (Zombi) klassi. O'yinchiga hujum qiluvchi dushmanni ifodalaydi.
    Harakati, animatsiyasi, sog'ligi va to'qnashuvni boshqaradi.
    """
    def __init__(self, x, y, zombie_hit_sound_obj):
        """
        Zombie obyektini initsializatsiya qilish.

        Args:
            x (int): Zombining boshlang'ich X koordinatasi.
            y (int): Zombining boshlang'ich Y koordinatasi.
            zombie_hit_sound_obj (pygame.mixer.Sound): Zombi zarba ovozi obyekti.
        """
        self.x = x
        self.y = y

        original_width = 596
        original_height = 842
        scale_factor = 1 # <-- BU YERDA O'ZGARISH: Rasmlarni masshtablash koeffitsienti 0.3 ga o'zgartirildi

        self.width = int(original_width * scale_factor)
        self.height = int(original_height * scale_factor)

        self.speed = ZOMBIE_SPEED

        self.zombie_hit_sound = zombie_hit_sound_obj

        def load_and_scale(image_path):
            """Rasmni yuklaydi va belgilangan o'lchamga masshtablaydi."""
            img = pygame.image.load(image_path)
            return pygame.transform.scale(img, (self.width, self.height))

        # Animatsiya rasmlarini yuklash va masshtablash
        self.zombie_R = [load_and_scale('assets/z_right1.png'), load_and_scale('assets/z_right2.png'),
                          load_and_scale('assets/z_right3.png')]
        self.zombie_L = [load_and_scale('assets/z_left1.png'), load_and_scale('assets/z_left2.png'),
                          load_and_scale('assets/z_left3.png')]
        self.zombieStand = load_and_scale('assets/z_right1.png') # Bu rasm zombining o'ngga qarab turgan holati uchun

        self.health = ZOMBIE_HEALTH # Hozirgi sog'liq
        self.max_health = ZOMBIE_HEALTH # Maksimal sog'liq (settings.py dan olinadi)
        self.active = False # Zombi hozirda ekranda faolmi
        self.spawn_time = pygame.time.get_ticks() # Zombining oxirgi paydo bo'lish vaqti

        self.left_z = False # Chapga yurish holati
        self.right_z = False # O'ngga yurish holati
        self.zombie_count = 0 # <-- QO'SHILDI: Animatsiya kadr hisoblagichini initsializatsiya qilish
        self.last_direction = "right" # <-- QO'SHILDI: Zombining oxirgi yo'nalishini saqlash

        # Hitbox (to'qnashuvni aniqlash zonasi) sozlamalari.
        self.hitbox_offset_x = self.width * 0.1
        self.hitbox_offset_y = self.height * 0.1
        self.hitbox_width = self.width * 0.4
        self.hitbox_height = self.height * 0.8
        self.hitbox = pygame.Rect(self.x + self.hitbox_offset_x, self.y + self.hitbox_offset_y,
                                   self.hitbox_width, self.hitbox_height)


    def update(self, player):
        """
        Zombining holatini yangilaydi (harakati, paydo bo'lishi, o'yinchiga hujumi).

        Args:
            player (Player): O'yinchi obyekti (zombining o'yinchiga qarab harakatlanishi uchun).
        """
        current_time = pygame.time.get_ticks()

        # Zombining paydo bo'lishini boshqarish
        if not self.active:
            if current_time - self.spawn_time > ZOMBIE_SPAWN_DELAY:
                self.active = True
                self.health = self.max_health # Yangi zombining sog'ligini to'liq qilish
                # Zombining boshlang'ich joylashuvini WORLD_WIDTH bo'ylab tasodifiy qilish
                # Zombi SCREEN_WIDTH dan WORLD_WIDTH - self.width gacha bo'lgan joyda paydo bo'lishi mumkin
                self.x = random.randrange(SCREEN_WIDTH, WORLD_WIDTH - self.width) # <-- BU YER O'ZGARTIRILDI
                self.y = ZOMBIE_START_Y # Y koordinatasi sabit qoladi
                self.zombie_count = 0 # Yangi zombi paydo bo'lganda animatsiya hisoblagichini qayta o'rnatish
                # print("Yangi zombi paydo bo'ldi!")


        if self.active:
            # Zombining o'yinchiga qarab harakatlanishi
            if self.x > player.x: # Agar zombi o'yinchidan o'ngda bo'lsa
                self.x -= self.speed # Chapga harakatlanish
                self.left_z = True
                self.right_z = False
                self.last_direction = "left" # <-- O'ZGARTIRILDI: Oxirgi yo'nalishni yangilash
            elif self.x < player.x: # Agar zombi o'yinchidan chapda bo'lsa
                self.x += self.speed # O'ngga harakatlanish
                self.left_z = False
                self.right_z = True
                self.last_direction = "right" # <-- O'ZGARTIRILDI: Oxirgi yo'nalishni yangilash
            else: # Agar zombi o'yinchiga yetib kelgan bo'lsa (harakatlanmaydi)
                self.left_z = False
                self.right_z = False
                # self.zombie_count = 0 # Harakat to'xtaganda animatsiyani qayta o'rnatish (agar kerak bo'lsa)

            # Hitboxni yangilash
            self.update_hitbox()

            # Zombi va O'yinchi to'qnashuvini tekshirish.
            if self.hitbox.colliderect(player.hitbox):
                player.take_damage(0.5) # O'yinchiga 0.5 zarar yetkazish.


    def take_damage(self, damage):
        """
        Zombiga zarar yetkazadi.
        """
        self.health -= damage
        if self.health <= 0:
            self.active = False
            self.spawn_time = pygame.time.get_ticks() # Yangi zombi uchun taymerni qayta boshlash
            # print("Zombi yo'q qilindi!")
        else: # Agar zombi hali tirik bo'lsa, urilish ovozini ijro etish
            if self.zombie_hit_sound: # Agar ovoz yuklangan bo'lsa
                self.zombie_hit_sound.play() # Zombi zarba ovozini ijro etish


    def update_hitbox(self):
        """
        Zombining hitbox koordinatalarini yangilaydi.
        """
        self.hitbox.x = self.x + self.hitbox_offset_x
        self.hitbox.y = self.y + self.hitbox_offset_y


    def draw(self, win, camera_offset): # <-- camera_offset parametri qo'shildi
        """
        Zombini o'yin oynasiga chizadi va uning sog'liq chizig'ini ko'rsatadi.

        Args:
            win (pygame.Surface): O'yin oynasi obyekti (chiziladigan sirt).
            camera_offset (int): Kameraning gorizontal siljishi.
        """
        if not self.active:
            return # Zombi faol bo'lmasa, chizmaymiz

        if self.zombie_count + 1 >= 30: # Animatsiya kadr hisoblagichini qayta o'rnatish
            self.zombie_count = 0

        # Zombining ekrandagi chizish koordinatasini hisoblash
        draw_x = self.x - camera_offset # <-- camera_offset ishlatilgan

        if self.left_z:
            win.blit(self.zombie_L[self.zombie_count // 10], (draw_x, self.y)) # <-- draw_x ishlatilgan
            self.zombie_count += 1
        elif self.right_z:
            win.blit(self.zombie_R[self.zombie_count // 10], (draw_x, self.y)) # <-- draw_x ishlatilgan
            self.zombie_count += 1
        else:
            # Agar zombi harakatlanmayotgan bo'lsa, oxirgi yo'nalish bo'yicha turgan holat rasmini chizish
            if self.last_direction == "left": # <-- BU QISM O'ZGARTIRILDI: player.x o'rniga self.last_direction ishlatildi
                win.blit(pygame.transform.flip(self.zombieStand, True, False), (draw_x, self.y))
            else:
                win.blit(self.zombieStand, (draw_x, self.y))


        # Zombining sog'liq chizig'ini chizish
        self.draw_health_bar(win, camera_offset) # <-- camera_offset uzatildi

    def draw_health_bar(self, win, camera_offset): # <-- camera_offset parametri qo'shildi
        """
        Zombining boshiga sog'liq chizig'ini chizadi.
        """
        # Sog'liq chizig'ining joylashuvi va o'lchamlari
        health_bar_width = self.width * 0.30 # Zombining kengligining 30%
        health_bar_height = 10 # Chiziq balandligi
        # Sog'liq chizig'ining X koordinatasi (zombining o'rtasiga tekislash)
        health_bar_x = (self.x + (self.width - health_bar_width) // 2) - camera_offset # <-- camera_offset hisobga olingan
        # Sog'liq chizig'ining Y koordinatasi (zombining boshidan biroz yuqorida)
        health_bar_y = self.y + 250 # Zombining yuqori chetidan 20 piksel yuqorida

        # Umumiy (orqa fon) sog'liq chizig'ini chizish (qora rangda)
        pygame.draw.rect(win, BLACK, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        # Hozirgi sog'liqni ifodalovchi yashil qismni hisoblash
        current_health_width = (self.health / self.max_health) * health_bar_width
        pygame.draw.rect(win, GREEN, (health_bar_x, health_bar_y, current_health_width, health_bar_height))

        # Sog'liq chizig'iga ramka chizish (opsional)
        pygame.draw.rect(win, WHITE, (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 1) # 1 piksel qalinlikda ramka