# bullet.py

import pygame  # Pygame kutubxonasini import qilish. Bu o'yinni yaratish uchun asosiy kutubxona.
from settings import * # settings.py faylidan barcha o'zgaruvchilarni (masalan, BULLET_SPEED, BULLET_RADIUS, BULLET_COLOR) import qilish.

class Bullet:
    """
    Bullet (O'q) klassi. O'yinchining otgan o'qlarini ifodalaydi.
    """
    def __init__(self, x, y, radius, color, facing):
        """
        O'q obyektini initsializatsiya qilish.

        Args:
            x (int): O'qning boshlang'ich X koordinatasi.
            y (int): O'qning boshlang'ich Y koordinatasi.
            radius (int): O'qning radiusi (dumaloq shakli uchun).
            color (tuple): O'qning rangi (RGB formatida, masalan, (255, 0, 0) qizil uchun).
            facing (int): O'qning yo'nalishi (-1 chapga, 1 o'ngga).
        """
        self.x = x  # O'qning gorizontal joylashuvi (markazi).
        self.y = y  # O'qning vertikal joylashuvi (markazi).
        self.radius = radius  # O'qning radiusi.
        self.color = color  # O'qning rangi.
        self.facing = facing  # O'qning harakatlanish yo'nalishi.
        self.vel = BULLET_SPEED * facing  # O'qning tezligi. Yo'nalishga qarab (musbat yoki manfiy).
        # O'qning hitboxini (to'qnashuvni aniqlash uchun to'rtburchak) yaratish.
        # Markazdan radiusni ayirib, to'rtburchakning yuqori-chap burchak koordinatalarini hisoblash.
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update_hitbox(self):
        """
        O'q harakatlanganda hitboxini yangilash.
        """
        self.rect.x = self.x - self.radius  # X koordinatasini yangilash.
        self.rect.y = self.y - self.radius  # Y koordinatasini yangilash.

    def draw(self, win, camera_offset): # <-- camera_offset parametri qo'shildi
        """
        O'qni ekranga chizish.

        Args:
            win (pygame.Surface): O'yin oynasi obyekti (chiziladigan sirt).
            camera_offset (int): Kameraning gorizontal siljishi.
        """
        # O'qning ekrandagi chizish koordinatasini hisoblash
        draw_x = self.x - camera_offset # <-- BU YERDA camera_offset ishlatilgan

        pygame.draw.circle(win, self.color, (draw_x, self.y), self.radius) # <-- draw_x ishlatilgan
        # # DEBUG: O'q hitboxini chizish (o'qning hitboxini ko'rish uchun kommentni oching)
        # pygame.draw.rect(win, (0, 0, 255), self.rect, 1) # Ko'k ramka