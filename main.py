import pygame # Pygame kutubxonasini import qilish. O'yinni rivojlantirish uchun asosiy kutubxona.
from settings import * # 'settings.py' faylidan barcha sozlamalarni (masalan, SCREEN_WIDTH, FPS, PLAYER_SPEED) import qilish.
from player import Player # 'player.py' faylidan Player klassini import qilish.
from zombie import Zombie # 'zombie.py' faylidan Zombie klassini import qilish.
# Bullet sinfini bevosita import qilish shart emas, chunki u Player sinfi orqali ishlatiladi.

pygame.init() # Pygame kutubxonasini ishga tushirish. Bu Pygame funksiyalaridan foydalanish uchun zarur.

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
fon = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombie Shooter")

# Fon rasmini yuklash va masshtablash
try:
    bg1 = pygame.image.load('assets/zed.jpg')
    bg1 = pygame.transform.scale(bg1, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bg2 = pygame.image.load('assets/zed2.jpg')
    bg2 = pygame.transform.scale(bg2, (SCREEN_WIDTH, SCREEN_HEIGHT))
except FileNotFoundError:
    print("Xato: Fon rasmi topilmadi. 'assets/zed.jpg' fayli mavjudligini tekshiring.")
    bg1 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg1.fill((0, 0, 0))
    bg2 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg2.fill((0, 0, 0))

# O'yinchi va Zombi obyektlarini yaratish
player = Player(PLAYER_START_X, PLAYER_START_Y, gun_sound_single, gun_sound_auto)
zombie = Zombie(ZOMBIE_START_X, ZOMBIE_START_Y, zombie_hit_sound) # Zombi yaratishda ovoz obyektini uzatish

score = 0 # O'yin bali
font = pygame.font.Font(None, 36) # Ballni ko'rsatish uchun shrift
camera_offset = 0

def draw_game_elements():
    """Barcha o'yin elementlarini oynaga chizadi."""
    # Fon rasmlarini chizish - TUZATILGAN QISM
    # Birinchi fon rasmi
    bg1_x = 0 - camera_offset
    fon.blit(bg1, (bg1_x, 0))
    
    # Ikkinchi fon rasmi (birinchi fonning davomi sifatida)
    bg2_x = SCREEN_WIDTH - camera_offset
    fon.blit(bg2, (bg2_x, 0))
    
    # Uchinchi fon rasmi (cheksiz takrorlash uchun)
    # Agar kamera 2-fon oralig'iga yetib kelsa
    if camera_offset > 0:
        bg3_x = (SCREEN_WIDTH * 2) - camera_offset
        fon.blit(bg1, (bg3_x, 0))  # bg1 ni uchinchi pozitsiyada takrorlash
    
    # To'rtinchi fon rasmi
    if camera_offset > SCREEN_WIDTH:
        bg4_x = (SCREEN_WIDTH * 3) - camera_offset  
        fon.blit(bg2, (bg4_x, 0))  # bg2 ni to'rtinchi pozitsiyada takrorlash

    player.draw(fon, camera_offset)
    zombie.draw(fon, camera_offset)

    # O'yinchining sog'lig'ini chizish
    player_health_text = font.render(f"Sog'liq: {player.health}", True, WHITE)
    fon.blit(player_health_text, (SCREEN_WIDTH - player_health_text.get_width() - 10, 10))

    pygame.display.update() # Ekranni yangilash

run = True # O'yin tsikli davom etishini belgilovchi flag

# O'yin tsikli
while run:
    pygame.time.delay(FPS) # O'yin tezligini boshqarish (kadr tezligini belgilaydi)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed() # Klaviatura tugmalarining holatini olish

    if player.alive:
        player.move(keys)
        mouse_held = pygame.mouse.get_pressed()[0]
        player.shoot(mouse_held)
        player.update_bullets()

        zombie.update(player) # Zombining holatini yangilash (harakati, o'yinchiga hujumi)
        
        # Kamera siljishini boshqarish (tuzatilgan)
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
            # Har bir o'qning hitboxi va zombining hitboxi o'rtasida to'qnashuvni tekshirish
            if bullet.rect.colliderect(zombie.hitbox):
                # O'ZGARISH BU YERDA: O'q zombining rasmi o'rtasiga yetganini tekshirish
                # Zombining markaziy hududini aniqlash (masalan, kengligining 40% dan 60% gacha)
                zombie_center_left_bound = zombie.x + zombie.width * 0.4
                zombie_center_right_bound = zombie.x + zombie.width * 0.6

                # Agar o'qning markazi zombining belgilangan "markaziy" hududida bo'lsa
                if zombie_center_left_bound <= bullet.x <= zombie_center_right_bound:
                    if zombie.active: # Agar zombi faol bo'lsa (tirik bo'lsa)
                        player.bullets.remove(bullet) # O'qni ro'yxatdan o'chirish (chunki u zombiga tekkan)
                        zombie.take_damage(1) # Zombiga 1 zarar yetkazish

                        if not zombie.active: # Agar zombi endi faol bo'lmasa (ya'ni o'lgan bo'lsa)
                            score += 100 # Ballni oshirish
                            print(f"Zombi yo'q qilindi! Ball: {score}") # Konsolga xabar
                else:
                    # Agar o'q hitboxga tegsa-yu, lekin markaziy qismga yetib bormagan bo'lsa,
                    # o'qni hali ham o'chirishni istamasligingiz mumkin.
                    # Hozircha o'qni o'chirmaymiz, u o'tishda davom etadi.
                    pass

        draw_game_elements() # O'yin elementlarini chizish funksiyasini chaqirish.
    else:
        # Game Over ekrani.
        fon.fill(BLACK) # O'yin oynasini qora rang bilan to'ldirish.
        font = pygame.font.Font(None, 74) # Katta shrift yaratish (74 o'lchamda).
        game_over_text = font.render("O'YIN TUGADI", True, RED) # "O'YIN TUGADI" matnini qizil rangda yaratish.
        # Matnni ekran markaziga joylashtirish uchun to'rtburchak (rect) obyektini olish.
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        fon.blit(game_over_text, text_rect) # "O'YIN TUGADI" matnini ekranga chizish.

        # Yakuniy ballni ko'rsatish.
        final_score_text = font.render(f"Sizning balingiz: {score}", True, WHITE) # Yakuniy ball matnini yaratish.
        # Yakuniy ball matnini biroz pastroqqa joylashtirish.
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        fon.blit(final_score_text, final_score_rect)

        pygame.display.update() # Ekranni yangilash

pygame.quit() # Pygame ni yopish