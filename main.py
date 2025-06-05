import pygame # Pygame kutubxonasini import qilish. O'yinni rivojlantirish uchun asosiy kutubxona.
from settings import * # 'settings.py' faylidan barcha sozlamalarni (masalan, SCREEN_WIDTH, FPS, PLAYER_SPEED) import qilish.
from player import Player # 'player.py' faylidan Player klassini import qilish.
from zombie import Zombie # 'zombie.py' faylidan Zombie klassini import qilish.
# Bullet sinfini bevosita import qilish shart emas, chunki u Player sinfi orqali ishlatiladi.

pygame.init() # Pygame kutubxonasini ishga tushirish. Bu Pygame funksiyalaridan foydalanish uchun zarur.

# Font modulini ishga tushirish (agar hali ishga tushirilmagan bo'lsa)
pygame.font.init()
game_font = pygame.font.Font(None, 36) # O'yin paneli uchun shrift

# Ovoz modulini ishga tushirish va ovoz fayllarini yuklash.
pygame.mixer.init() # Pygame ovoz mikserini ishga tushirish.
try:
    # Bir martalik otish ovozi faylini yuklash.
    gun_sound_single = pygame.mixer.Sound('assets/gun_sound_single.mp3')
    gun_sound_single.set_volume(0.5) # Bir martalik otish ovozi balandligini sozlash (0.0 dan 1.0 gacha).

    # Avtomatik otish ovozi faylini yuklash.
    gun_sound_auto = pygame.mixer.Sound('assets/gun_sound_auto.mp3')
    gun_sound_auto.set_volume(0.7) # Avtomat otish ovozi balandligini sozlash.

    zombie_hit_sound = pygame.mixer.Sound('assets/zombie_hit.mp3') # Zombi zarba ovozi
    zombie_hit_sound.set_volume(0.6) # Zombi zarba ovozi balandligini sozlash

    pygame.mixer.music.load('assets/background_music.mp3') # Fon musiqasi
    pygame.mixer.music.set_volume(0.2) # Fon musiqasi balandligi
    pygame.mixer.music.play(-1) # Cheksiz takrorlash

except pygame.error as e:
    print(f"Ovoz faylini yuklashda xato yuz berdi: {e}")
    # Ovoz fayllari topilmasa, ovozlarni None qilib qo'yamiz, shunda dastur ishdan chiqmaydi
    gun_sound_single = None
    gun_sound_auto = None
    zombie_hit_sound = None
    pygame.mixer.music.stop() # Agar musiqa yuklanmasa, ijro etishga urinmaslik

# O'yin oynasini sozlash
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # `fon` nomini `win` ga o'zgartirdim, odatda shunday ishlatiladi
pygame.display.set_caption("Zombie Shooter")

# Fon rasmini yuklash va masshtablash
try:
    # `bg` nomini `bg1` ga o'zgartirdim, chunki endi bir nechta fonlar bor
    bg1 = pygame.image.load('assets/zed.jpg')
    bg1 = pygame.transform.scale(bg1, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg2 = pygame.image.load('assets/zed2.jpg')
    bg2 = pygame.transform.scale(bg2, (SCREEN_WIDTH, SCREEN_HEIGHT)) # Yangi fon
    bg3 = pygame.image.load('assets/zed3.jpg')
    bg3 = pygame.transform.scale(bg3, (SCREEN_WIDTH, SCREEN_HEIGHT)) # Yangi fon
except FileNotFoundError:
    print("Xato: Fon rasmi topilmadi. 'assets/zed.png', 'assets/zed2.png' yoki 'assets/zed3.png' fayllari mavjudligini tekshiring.")
    bg1 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg1.fill((0, 0, 0))
    bg2 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg2.fill((0, 0, 0))
    bg3 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg3.fill((0, 0, 0))


# O'yinchi obyektini yaratish
player = Player(PLAYER_START_X, PLAYER_START_Y, gun_sound_single, gun_sound_auto)

# Zombi obyektlari ro'yxatini yaratish
zombies = [Zombie(ZOMBIE_START_X, ZOMBIE_START_Y, zombie_hit_sound)] # Boshlang'ich zombi

score = 0 # O'yin bali
font = pygame.font.Font(None, 36) # Ballni ko'rsatish uchun shrift
camera_offset = 0 # Kamera siljishi

clock = pygame.time.Clock() # FPS ni boshqarish uchun clock obyektini yaratish

def draw_game_elements():
    """Barcha o'yin elementlarini oynaga chizadi."""
    # Fonlarni kamera ofsetiga qarab chizish
    win.blit(bg1, (0 - camera_offset, 0))
    win.blit(bg2, (SCREEN_WIDTH - camera_offset, 0)) # Ikkinchi fon
    win.blit(bg3, (SCREEN_WIDTH * 2 - camera_offset, 0)) # Uchinchi fon

    # O'yinchi va zombilarni chizish (camera_offset bilan)
    player.draw(win, camera_offset)
    for zomb in zombies: # Barcha zombilarni chizish
        zomb.draw(win, camera_offset) # Zombi chizishda camera_offset uzatildi

    # O'qlarni chizish (camera_offset bilan)
    for bullet in player.bullets:
        bullet.draw(win, camera_offset)

    # === HUD (Heads-Up Display) paneli ===
    # 1. O'yinchining sog'lig'i
    health_text = game_font.render(f"Sog'liq: {int(player.health)}", True, WHITE)
    win.blit(health_text, (10, 10)) # Yuqori chap burchakda

    # 2. Ball
    score_text = game_font.render(f"Ball: {score}", True, WHITE)
    win.blit(score_text, (10, 50)) # Sog'liq ostida

    pygame.display.update() # Ekranni yangilash

run = True # O'yin tsikli davom etishini belgilovchi flag

# O'yin tsikli
while run:
    clock.tick(FPS) # FPS ni saqlash

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed() # Klaviatura tugmalarining holatini olish

    if player.alive:
        player.move(keys)
        mouse_held = pygame.mouse.get_pressed()[0]
        player.shoot(mouse_held)
        player.update_bullets()

        # Barcha zombilarni yangilash
        for zomb in zombies:
            zomb.update(player) # Har bir zombining holatini yangilash

        # Kamera siljishini boshqarish
        # Agar o'yinchi ekranning o'ng chegarasidan o'tib ketsa
        if player.x - camera_offset > SCREEN_WIDTH - CAMERA_SCROLL_BORDER:
            camera_offset += player.speed # Kamerani o'yinchi tezligida siljitish
            # Kamera chegarasini yumshoq qilish
            if camera_offset > WORLD_WIDTH - SCREEN_WIDTH:
                camera_offset = WORLD_WIDTH - SCREEN_WIDTH
        # Agar o'yinchi ekranning chap chegarasidan o'tib ketsa
        elif player.x - camera_offset < CAMERA_SCROLL_BORDER:
            camera_offset -= player.speed # Kamerani o'yinchi tezligida siljitish
            if camera_offset < 0: # Kamera 0 dan kichik bo'lmasligi uchun
                camera_offset = 0

        # O'qlar va Zombilar o'rtasidagi to'qnashuvni tekshirish
        for bullet in player.bullets[:]: # O'qlar ro'yxati ustida iteratsiya qilish
            for zomb in zombies[:]: # Barcha zombilar ustida iteratsiya qilish
                # Har bir o'qning hitboxi va zombining hitboxi o'rtasida to'qnashuvni tekshirish
                if bullet.rect.colliderect(zomb.hitbox):
                    # O'q zombining rasmi o'rtasiga yetganini tekshirish
                    # Zombining markaziy hududini aniqlash (masalan, kengligining 40% dan 60% gacha)
                    zombie_center_left_bound = zomb.x + zomb.width * 0.4
                    zombie_center_right_bound = zomb.x + zomb.width * 0.6

                    # Agar o'qning markazi zombining belgilangan "markaziy" hududida bo'lsa
                    if zombie_center_left_bound <= bullet.x <= zombie_center_right_bound:
                        if zomb.active: # Agar zombi faol bo'lsa (tirik bo'lsa)
                            player.bullets.remove(bullet) # O'qni ro'yxatdan o'chirish (chunki u zombiga tekkan)
                            zomb.take_damage(1) # Zombiga 1 zarar yetkazish

                            if not zomb.active: # Agar zombi endi faol bo'lmasa (ya'ni o'lgan bo'lsa)
                                score += 100 # Ballni oshirish
                                print(f"Zombi yo'q qilindi! Ball: {score}") # Konsolga xabar
                                # Yangi zombi qo'shish (bu yerda spawn_delay ichida zombining o'zi reaktivatsiya bo'ladi)
                                # Agar siz har bir o'lgan zombining o'rniga yangisini paydo bo'lishini istasangiz:
                                # zombies.append(Zombie(random.randrange(SCREEN_WIDTH, WORLD_WIDTH - ZOMBIE_WIDTH), ZOMBIE_START_Y, zombie_hit_sound))
                        break # Bitta o'q faqat bitta zombiga zarar yetkazsin
                    else:
                        # Agar o'q hitboxga tegsa-yu, lekin markaziy qismga yetib bormagan bo'lsa,
                        # o'qni hali ham o'chirishni istamasligingiz mumkin.
                        # Hozircha o'qni o'chirmaymiz, u o'tishda davom etadi.
                        pass # O'qni o'chirishdan qochish uchun

        draw_game_elements() # O'yin elementlarini chizish funksiyasini chaqirish.
    else:
        # Game Over ekrani.
        win.fill(BLACK) # O'yin oynasini qora rang bilan to'ldirish.
        font = pygame.font.Font(None, 74) # Katta shrift yaratish (74 o'lchamda).
        game_over_text = font.render("O'YIN TUGADI", True, RED) # "O'YIN TUGADI" matnini qizil rangda yaratish.
        # Matnni ekran markaziga joylashtirish uchun to'rtburchak (rect) obyektini olish.
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        win.blit(game_over_text, text_rect) # "O'YIN TUGADI" matnini ekranga chizish.

        # Yakuniy ballni ko'rsatish.
        final_score_text = font.render(f"Sizning balingiz: {score}", True, WHITE) # Yakuniy ball matnini yaratish.
        # Yakuniy ball matnini biroz pastroqqa joylashtirish.
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        win.blit(final_score_text, final_score_rect)

        pygame.display.update() # Ekranni yangilash

pygame.quit() # Pygame ni yopish