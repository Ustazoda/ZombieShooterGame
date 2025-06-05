# player.py

import pygame
from settings import *
from bullet import Bullet

class Player:
    def __init__(self, x, y, gun_sound_single_obj, gun_sound_auto_obj):
        self.x = x
        self.y = y

        original_width = 590
        original_height = 842
        scale_factor = 1

        self.width = int(original_width * scale_factor)
        self.height = int(original_height * scale_factor)

        self.speed = PLAYER_SPEED

        self.gun_sound_single = gun_sound_single_obj
        self.gun_sound_auto = gun_sound_auto_obj

        pygame.mixer.set_num_channels(8)
        self.auto_fire_channel = pygame.mixer.Channel(0)

        def load_and_scale(image_path):
            img = pygame.image.load(image_path)
            return pygame.transform.scale(img, (self.width, self.height))

        self.walkRight = [load_and_scale('assets/right1.png'), load_and_scale('assets/right2.png'),
                          load_and_scale('assets/right3.png'), load_and_scale('assets/right4.png'),
                          load_and_scale('assets/right5.png'), load_and_scale('assets/right6.png')]
        self.walkLeft = [load_and_scale('assets/left1.png'), load_and_scale('assets/left2.png'),
                         load_and_scale('assets/left3.png'), load_and_scale('assets/left4.png'),
                         load_and_scale('assets/left5.png'), load_and_scale('assets/left6.png')]
        self.playerStand = load_and_scale('assets/right1.png')

        self.isJump = False
        self.jumpCount = PLAYER_JUMP_HEIGHT
        self.left = False
        self.right = False
        self.animCount = 0
        self.lastMove = "right"

        self.last_shot_time = 0
        self.bullets = []
        self.mouse_was_held = False

        self.hitbox_offset_x = self.width * 0.3
        self.hitbox_offset_y = self.height * 0.1
        self.hitbox_width = self.width * 0.4
        self.hitbox_height = self.height * 0.8
        self.hitbox = pygame.Rect(self.x + self.hitbox_offset_x, self.y + self.hitbox_offset_y,
                                  self.hitbox_width, self.hitbox_height)

        self.health = 100
        self.alive = True

    def move(self, keys):
        """
        O'yinchining klaviatura orqali harakatini boshqaradi.
        O'yinchi WORLD_WIDTH ichida harakatlanishi mumkin.
        """
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.left = True
            self.right = False
            self.lastMove = "left"
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.left = False
            self.right = True
            self.lastMove = "right"
        else:
            self.left = False
            self.right = False
            self.animCount = 0

        # O'yinchi WORLD_WIDTH ichida qolishini ta'minlash
        if self.x < 0:
            self.x = 0
        if self.x > WORLD_WIDTH - self.width:
            self.x = WORLD_WIDTH - self.width

        # Sakrash mexanikasi.
        if not (self.isJump):
            if keys[pygame.K_UP]:
                self.isJump = True
        else:
            if self.jumpCount >= -PLAYER_JUMP_HEIGHT:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.y = PLAYER_START_Y
                self.jumpCount = PLAYER_JUMP_HEIGHT

        self.hitbox.x = self.x + self.hitbox_offset_x
        self.hitbox.y = self.y + self.hitbox_offset_y


    def shoot(self, mouse_held):
        current_time = pygame.time.get_ticks()

        if mouse_held:
            if not self.mouse_was_held:
                if self.gun_sound_single:
                    self.gun_sound_single.play()

                if self.gun_sound_auto and not self.auto_fire_channel.get_busy():
                    self.auto_fire_channel.play(self.gun_sound_auto, loops=-1)

                self.last_shot_time = current_time

                facing = 1 if self.lastMove == "right" else -1
                bullet_start_x = round(self.x + self.width * (0.79 if facing == 1 else 0.3))
                bullet_start_y = round(self.y + self.height * 0.506)
                self.bullets.append(Bullet(bullet_start_x, bullet_start_y, BULLET_RADIUS, BULLET_COLOR, facing))

            else:
                if current_time - self.last_shot_time > SHOOT_DELAY:
                    self.last_shot_time = current_time

                    facing = 1 if self.lastMove == "right" else -1
                    bullet_start_x = round(self.x + self.width * (0.79 if facing == 1 else 0.3))
                    bullet_start_y = round(self.y + self.height * 0.506)
                    self.bullets.append(Bullet(bullet_start_x, bullet_start_y, BULLET_RADIUS, BULLET_COLOR, facing))

                if self.gun_sound_auto and not self.auto_fire_channel.get_busy():
                    self.auto_fire_channel.play(self.gun_sound_auto, loops=-1)

            self.mouse_was_held = True

        else:
            if self.auto_fire_channel.get_busy():
                self.auto_fire_channel.stop()

            self.mouse_was_held = False


    def update_bullets(self):
        """
        O'qlarning holatini yangilaydi (harakati, ekran chegarasini tekshirish).
        Endi o'qlar butun WORLD_WIDTH bo'ylab harakatlanadi.
        """
        for bullet in self.bullets[:]:
            # O'q WORLD_WIDTH chegaralaridan chiqib ketganini tekshirish
            if 0 < bullet.x < WORLD_WIDTH: # SCREEN_WIDTH o'rniga WORLD_WIDTH
                bullet.x += bullet.vel
                bullet.update_hitbox()
            else:
                self.bullets.remove(bullet)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            print("O'yinchi o'ldi! Game Over.")

    def draw(self, win, camera_offset):
        """
        O'yinchini o'yin oynasiga chizadi, kamera ofsetini hisobga olgan holda.
        """
        if self.animCount + 1 >= 30:
            self.animCount = 0

        # O'yinchining ekrandagi chizish koordinatasini hisoblash
        draw_x = self.x - camera_offset

        if self.left:
            win.blit(self.walkLeft[self.animCount // 5], (draw_x, self.y))
            self.animCount += 1
        elif self.right:
            win.blit(self.walkRight[self.animCount // 5], (draw_x, self.y))
            self.animCount += 1
        else:
            if self.lastMove == "right":
                win.blit(self.playerStand, (draw_x, self.y))
            else:
                win.blit(pygame.transform.flip(self.playerStand, True, False), (draw_x, self.y))

        # Otilgan o'qlarni chizish (o'qlar ham kamera ofsetini hisobga oladi)
        for bullet in self.bullets:
            bullet.draw(win, camera_offset)