# settings.py

# Ekran sozlamalari
SCREEN_WIDTH = 1600   # O'yin oynasining kengligi piksellarda.
SCREEN_HEIGHT = 1043  # O'yin oynasining balandligi piksellarda.
FPS = 40              # Sekundiga kadrlar soni (Frames Per Second). O'yin tezligini belgilaydi.

# O'yin dunyosi sozlamalari
WORLD_WIDTH = SCREEN_WIDTH * 2 # Dunyo kengligi (2 ta fon rasmi)
CAMERA_SCROLL_BORDER = SCREEN_WIDTH // 2 # Kamera siljishni boshlaydigan chegara (ekran markazi)

# Player sozlamalari
PLAYER_SPEED = 15     # O'yinchining harakatlanish tezligi piksellarda.
PLAYER_JUMP_HEIGHT = 13 # Sakrash balandligi uchun hisoblagichning boshlang'ich qiymati.
                        # Bu qiymat qancha katta bo'lsa, o'yinchi shuncha baland sakraydi.
PLAYER_START_X = 10   # O'yinchining boshlang'ich X koordinatasi.
PLAYER_START_Y = 325  # O'yinchining boshlang'ich Y koordinatasi (yerga nisbatan).

# Zombie sozlamalari
ZOMBIE_SPEED = 5      # Zombining harakatlanish tezligi. O'yinchidan sal sekinroq.
ZOMBIE_HEALTH = 10  # Har bir zombining sog'liq balli.
ZOMBIE_SPAWN_DELAY = 5000 # Yangi zombining paydo bo'lishi orasidagi kechikish milisaniyalarda (5 soniya).
ZOMBIE_START_X = 1150 # Zombining paydo bo'ladigan boshlang'ich X koordinatasi (dastlabki joylashuv uchun).
ZOMBIE_START_Y = 310  # Zombining paydo bo'ladigan boshlang'ich Y koordinatasi.

# Bullet sozlamalari
BULLET_SPEED = 20     # O'qning tezligi.
BULLET_RADIUS = 5     # O'qning radiusi (dumaloq shakli uchun).
BULLET_COLOR = (255, 0, 0) # O'qning rangi (Qizil).
SHOOT_DELAY = 100     # O'q otishlar orasidagi minimal kechikish (millisekundda).

# Ranglar (RGB formatida)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)