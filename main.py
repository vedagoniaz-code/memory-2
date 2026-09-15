import pygame
import random
import os
import sys
import json
import math

# ============================================================
# ЗАПУСК PYGAME
# ============================================================

pygame.init()

# ============================================================
# ПАПКА С КАРТИНКАМИ
# ============================================================
IMAGE_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "buttons"
)

RECORD_FOLDER = os.path.dirname(
    os.path.abspath(__file__)
)
# ============================================================
# ПОЛНОЭКРАННЫЙ РЕЖИМ
# ============================================================

info = pygame.display.Info()

WINDOW_WIDTH = info.current_w
WINDOW_HEIGHT = info.current_h

screen = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT),
    pygame.FULLSCREEN
)

pygame.display.set_caption(
    "MEMORY 2.1 — игра для двоих"
)

clock = pygame.time.Clock()

print("Разрешение экрана:")
print(WINDOW_WIDTH, "x", WINDOW_HEIGHT)


# ============================================================
# КОЛИЧЕСТВО КАРТОЧЕК
# ============================================================

CARD_COUNTS = [
    8,
    12,
    16,
    20,
    24,
    32,
    40,
    50,
    64,
    100
]

card_count = 100


# ============================================================
# КАРТИНКИ
# ============================================================

images = [
    "lion.jpg",
    "tiger.jpg",
    "elephant.jpg",
    "giraffe.jpg",
    "zebra.jpg",
    "panda.jpg",
    "bear.jpg",
    "wolf.jpg",
    "fox.jpg",
    "deer.jpg",

    "rabbit.jpg",
    "monkey.jpg",
    "gorilla.jpg",
    "koala.jpg",
    "kangaroo.jpg",
    "horse.jpg",
    "cow.jpg",
    "pig.jpg",
    "sheep.jpg",
    "goat.jpg",

    "dog.jpg",
    "cat.jpg",
    "mouse.jpg",
    "hamster.jpg",
    "squirrel.jpg",
    "hedgehog.jpg",
    "owl.jpg",
    "eagle.jpg",
    "parrot.jpg",
    "penguin.jpg",

    "flamingo.jpg",
    "peacock.jpg",
    "dolphin.jpg",
    "whale.jpg",
    "shark.jpg",
    "octopus.jpg",
    "turtle.jpg",
    "frog.jpg",
    "snake.jpg",
    "crocodile.jpg",

    "butterfly.jpg",
    "bee.jpg",
    "ladybug.jpg",
    "spider.jpg",
    "dragon.jpg",
    "unicorn.jpg",
    "camel.jpg",
    "hippo.jpg",
    "rhino.jpg",
    "seal.jpg"
]


# ============================================================
# ПРОВЕРКА КОЛИЧЕСТВА КАРТИНОК
# ============================================================

if len(images) != 50:

    print("ОШИБКА: должно быть 50 картинок.")

    pygame.quit()
    sys.exit()


# ============================================================
# ЗАГРУЗКА КАРТИНОК
# ============================================================

loaded_images = {}

for filename in images:

    path = os.path.join(
        IMAGE_FOLDER,
        filename
    )

    if not os.path.exists(path):

        print()
        print("НЕ НАЙДЕН ФАЙЛ:")
        print(path)
        print()

        pygame.quit()
        sys.exit()

    try:

        loaded_images[filename] = pygame.image.load(
            path
        ).convert()

    except pygame.error as error:

        print()
        print("ОШИБКА ЗАГРУЗКИ:")
        print(path)
        print(error)
        print()

        pygame.quit()
        sys.exit()


print()
print("Все 50 картинок успешно загружены.")
print()


# ============================================================
# ЗВУКИ
# ============================================================

sound_flip = None
sound_match = None
sound_wrong = None
sound_win = None

try:

    pygame.mixer.init()

    sound_files = {
        "flip": "flip.mp3",
        "match": "match.mp3",
        "wrong": "wrong.mp3",
        "win": "win.mp3"
    }

    for sound_name, filename in sound_files.items():

        path = os.path.join(
            IMAGE_FOLDER,
            filename
        )

        if os.path.exists(path):

            try:

                sound = pygame.mixer.Sound(path)

                if sound_name == "flip":
                    sound_flip = sound

                elif sound_name == "match":
                    sound_match = sound

                elif sound_name == "wrong":
                    sound_wrong = sound

                elif sound_name == "win":
                    sound_win = sound

                print("Звук загружен:", filename)

            except pygame.error:

                print(
                    "Не удалось загрузить:",
                    filename
                )

        else:

            print(
                "Звука нет:",
                filename
            )

except pygame.error:

    print(
        "Звуковая система недоступна."
    )


# ============================================================
# ФУНКЦИЯ ВОСПРОИЗВЕДЕНИЯ ЗВУКА
# ============================================================

def play_sound(sound):

    if sound is not None:

        try:
            sound.play()

        except pygame.error:
            pass


# ============================================================
# АВТОМАТИЧЕСКИЙ МАСШТАБ ИНТЕРФЕЙСА
# ============================================================

# Базовое разрешение, относительно которого
# рассчитывается размер интерфейса.

BASE_WIDTH = 1920
BASE_HEIGHT = 1080

scale_x = WINDOW_WIDTH / BASE_WIDTH
scale_y = WINDOW_HEIGHT / BASE_HEIGHT

UI_SCALE = min(
    scale_x,
    scale_y
)

# Не даём интерфейсу стать слишком маленьким
# или слишком огромным.

UI_SCALE = max(
    0.55,
    min(UI_SCALE, 1.5)
)


# ============================================================
# ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ МАСШТАБИРОВАНИЯ
# ============================================================

def S(value):

    return max(
        1,
        int(value * UI_SCALE)
    )


# ============================================================
# ШРИФТЫ
# ============================================================

font_title = pygame.font.SysFont(
    "Arial",
    S(42),
    bold=True
)

font_score = pygame.font.SysFont(
    "Arial",
    S(30),
    bold=True
)

font_small = pygame.font.SysFont(
    "Arial",
    S(22),
    bold=True
)

font_card = pygame.font.SysFont(
    "Arial",
    S(32),
    bold=True
)

font_winner = pygame.font.SysFont(
    "Arial",
    S(60),
    bold=True
)

font_timer = pygame.font.SysFont(
    "Arial",
    S(28),
    bold=True
)

font_big = pygame.font.SysFont(
    "Arial",
    S(90),
    bold=True
)


# ============================================================
# СЕТКИ
# ============================================================

GRID_SIZES = {

    8: (2, 4),

    12: (3, 4),

    16: (4, 4),

    20: (4, 5),

    24: (4, 6),

    32: (4, 8),

    40: (5, 8),

    50: (5, 10),

    64: (8, 8),

    100: (10, 10)
}


# ============================================================
# ПАРАМЕТРЫ ПОЛЯ
# ============================================================

ROWS = 10
COLS = 10

CARD_SIZE = 100
GAP = S(6)

field_x = 0
field_y = 0


# ============================================================
# ПАРАМЕТРЫ ВЕРХНЕЙ ПАНЕЛИ
# ============================================================

TOP_SPACE = S(145)

BOTTOM_SPACE = S(25)


# ============================================================
# РАСЧЁТ ПОЛЯ
# ============================================================

def calculate_field():

    global ROWS
    global COLS
    global CARD_SIZE
    global GAP
    global field_x
    global field_y

    ROWS, COLS = GRID_SIZES[card_count]

    GAP = S(6)

    # --------------------------------------------------------
    # Верхняя панель
    # --------------------------------------------------------

    top_space = TOP_SPACE

    bottom_space = BOTTOM_SPACE

    # --------------------------------------------------------
    # Свободная область
    # --------------------------------------------------------

    available_width = (
        WINDOW_WIDTH
        - S(40)
    )

    available_height = (
        WINDOW_HEIGHT
        - top_space
        - bottom_space
    )

    # --------------------------------------------------------
    # Размер карточки по ширине
    # --------------------------------------------------------

    card_width = (
        available_width
        - (COLS - 1) * GAP
    ) // COLS

    # --------------------------------------------------------
    # Размер карточки по высоте
    # --------------------------------------------------------

    card_height = (
        available_height
        - (ROWS - 1) * GAP
    ) // ROWS

    # --------------------------------------------------------
    # Берём минимальный размер
    # --------------------------------------------------------

    CARD_SIZE = min(
        card_width,
        card_height
    )

    # --------------------------------------------------------
    # Минимальный размер
    # --------------------------------------------------------

    CARD_SIZE = max(
        20,
        CARD_SIZE
    )

    # --------------------------------------------------------
    # Размер поля
    # --------------------------------------------------------

    field_width = (
        COLS * CARD_SIZE
        + (COLS - 1) * GAP
    )

    field_height = (
        ROWS * CARD_SIZE
        + (ROWS - 1) * GAP
    )

    # --------------------------------------------------------
    # Центрирование по горизонтали
    # --------------------------------------------------------

    field_x = (
        WINDOW_WIDTH
        - field_width
    ) // 2

    # --------------------------------------------------------
    # Центрирование по вертикали
    # --------------------------------------------------------

    field_y = (
        top_space
        + (
            available_height
            - field_height
        ) // 2
    )


# ============================================================
# СОЗДАНИЕ КОЛОДЫ
# ============================================================

def new_game():

    pairs = card_count // 2

    selected = random.sample(
        images,
        pairs
    )

    cards = selected * 2

    random.shuffle(cards)

    return cards


# ============================================================
# РЕКОРДЫ
# ============================================================

RECORD_FILE = os.path.join(
    IMAGE_FOLDER,
    "memory_record.json"
)


def load_records():

    if not os.path.exists(RECORD_FILE):

        return {}

    try:

        with open(
            RECORD_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except:

        return {}


def save_records(records):

    try:

        with open(
            RECORD_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                records,
                file,
                ensure_ascii=False,
                indent=4
            )

    except:

        pass


records = load_records()


# ============================================================
# СОСТОЯНИЕ ИГРЫ
# ============================================================

cards = []

opened = []

matched = set()

player = 0

scores = [0, 0]

show_wrong_until = 0

wrong_pair = []

game_finished = False

victory_time = 0

new_record = False

animation_type = None

animation_start = 0

animation_duration = 500

game_start_time = 0

timer_running = False

win_sound_played = False


# ============================================================
# ПЕРЕЗАПУСК
# ============================================================

def restart_game():

    global cards
    global opened
    global matched
    global player
    global scores
    global show_wrong_until
    global wrong_pair
    global game_finished
    global victory_time
    global new_record
    global animation_type
    global animation_start
    global game_start_time
    global timer_running
    global win_sound_played

    calculate_field()

    cards = new_game()

    opened = []

    matched = set()

    player = 0

    scores = [0, 0]

    show_wrong_until = 0

    wrong_pair = []

    game_finished = False

    victory_time = 0

    new_record = False

    animation_type = None

    animation_start = 0

    game_start_time = pygame.time.get_ticks()

    timer_running = False

    win_sound_played = False


restart_game()


# ============================================================
# КНОПКИ КОЛИЧЕСТВА
# ============================================================

button_gap = max(
    S(4),
    4
)

# ------------------------------------------------------------
# Пытаемся использовать базовую ширину 78
# ------------------------------------------------------------

button_width = S(78)

button_height = S(42)

# ------------------------------------------------------------
# Проверяем, помещается ли вся панель
# ------------------------------------------------------------

available_button_width = (
    WINDOW_WIDTH
    - S(250)
)

total_needed_width = (
    len(CARD_COUNTS) * button_width
    + (len(CARD_COUNTS) - 1) * button_gap
)

# ------------------------------------------------------------
# Если не помещается — уменьшаем кнопки
# ------------------------------------------------------------

if total_needed_width > available_button_width:

    button_width = (
        available_button_width
        - (
            len(CARD_COUNTS) - 1
        ) * button_gap
    ) // len(CARD_COUNTS)

# ------------------------------------------------------------
# Не даём кнопкам стать слишком маленькими
# ------------------------------------------------------------

button_width = max(
    45,
    button_width
)


# ============================================================
# ПОЗИЦИЯ КНОПОК
# ============================================================

total_buttons_width = (
    len(CARD_COUNTS) * button_width
    + (
        len(CARD_COUNTS) - 1
    ) * button_gap
)

# ------------------------------------------------------------
# Панель кнопок располагается справа
# ------------------------------------------------------------

buttons_start_x = (
    WINDOW_WIDTH
    - total_buttons_width
    - S(140)
)

# Если экран слишком узкий,
# начинаем панель раньше.

buttons_start_x = max(
    S(5),
    buttons_start_x
)


buttons = []

for i, count in enumerate(CARD_COUNTS):

    x = (
        buttons_start_x
        + i * (
            button_width
            + button_gap
        )
    )

    rect = pygame.Rect(
        x,
        S(30),
        button_width,
        button_height
    )

    buttons.append(
        (count, rect)
    )


# ============================================================
# КНОПКА ВЫХОДА
# ============================================================

exit_width = max(
    S(75),
    int(button_width * 1.05)
)

exit_height = button_height

exit_rect = pygame.Rect(
    WINDOW_WIDTH - exit_width - S(20),
    S(30),
    exit_width,
    exit_height
)


# ============================================================
# ФОРМАТ ТАЙМЕРА
# ============================================================

def format_time(milliseconds):

    seconds = milliseconds // 1000

    minutes = seconds // 60

    seconds = seconds % 60

    return f"{minutes:02d}:{seconds:02d}"


# ============================================================
# ПОИСК КАРТОЧКИ
# ============================================================

def get_card_index(
    mouse_x,
    mouse_y
):

    for index in range(card_count):

        row = index // COLS

        col = index % COLS

        x = (
            field_x
            + col * (
                CARD_SIZE + GAP
            )
        )

        y = (
            field_y
            + row * (
                CARD_SIZE + GAP
            )
        )

        rect = pygame.Rect(
            x,
            y,
            CARD_SIZE,
            CARD_SIZE
        )

        if rect.collidepoint(
            mouse_x,
            mouse_y
        ):

            return index

    return None


# ============================================================
# ПОБЕДА
# ============================================================

def finish_game():

    global game_finished
    global victory_time
    global new_record
    global win_sound_played

    game_finished = True

    victory_time = (
        pygame.time.get_ticks()
        - game_start_time
    )

    key = str(card_count)

    old_record = records.get(
        key
    )

    if old_record is None:

        new_record = True

        records[key] = victory_time

        save_records(
            records
        )

    elif victory_time < old_record:

        new_record = True

        records[key] = victory_time

        save_records(
            records
        )

    else:

        new_record = False

    if not win_sound_played:

        play_sound(
            sound_win
        )

        win_sound_played = True


# ============================================================
# ОСНОВНОЙ ЦИКЛ
# ============================================================

running = True

while running:

    now = pygame.time.get_ticks()


    # ========================================================
    # СОБЫТИЯ
    # ========================================================

    for event in pygame.event.get():

        # ----------------------------------------------------
        # ЗАКРЫТИЕ
        # ----------------------------------------------------

        if event.type == pygame.QUIT:

            running = False


        # ----------------------------------------------------
        # КЛАВИАТУРА
        # ----------------------------------------------------

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False

            if event.key == pygame.K_r:

                restart_game()


        # ----------------------------------------------------
        # МЫШЬ
        # ----------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos


            # =================================================
            # ВЫБОР КОЛИЧЕСТВА КАРТОЧЕК
            # =================================================

            selected_count = None

            for count, rect in buttons:

                if rect.collidepoint(
                    mouse_x,
                    mouse_y
                ):

                    selected_count = count

                    break


            if selected_count is not None:

                if selected_count != card_count:

                    card_count = selected_count

                    restart_game()

                continue


            # =================================================
            # ВЫХОД
            # =================================================

            if exit_rect.collidepoint(
                mouse_x,
                mouse_y
            ):

                running = False

                continue


            # =================================================
            # ПОБЕДА
            # =================================================

            if game_finished:

                restart_game()

                continue


            # =================================================
            # ОЖИДАНИЕ ПОСЛЕ ОШИБКИ
            # =================================================

            if now < show_wrong_until:

                continue


            # =================================================
            # ДВЕ КАРТЫ УЖЕ ОТКРЫТЫ
            # =================================================

            if len(opened) >= 2:

                continue


            # =================================================
            # ПОИСК КАРТОЧКИ
            # =================================================

            index = get_card_index(
                mouse_x,
                mouse_y
            )

            if index is None:

                continue


            if index in matched:

                continue


            if index in opened:

                continue


            # =================================================
            # ОТКРЫВАЕМ
            # =================================================

            opened.append(
                index
            )

            timer_running = True

            play_sound(
                sound_flip
            )


            # =================================================
            # ВТОРАЯ КАРТА
            # =================================================

            if len(opened) == 2:

                first = cards[
                    opened[0]
                ]

                second = cards[
                    opened[1]
                ]


                # =============================================
                # СОВПАДЕНИЕ
                # =============================================

                if first == second:

                    matched.add(
                        opened[0]
                    )

                    matched.add(
                        opened[1]
                    )

                    scores[player] += 1

                    animation_type = "match"

                    animation_start = now

                    play_sound(
                        sound_match
                    )

                    opened.clear()


                    # -----------------------------------------
                    # ПОБЕДА
                    # -----------------------------------------

                    if len(matched) == card_count:

                        finish_game()


                # =============================================
                # ОШИБКА
                # =============================================

                else:

                    wrong_pair = [
                        opened[0],
                        opened[1]
                    ]

                    # 450 мс
                    show_wrong_until = (
                        now + 450
                    )

                    animation_type = "wrong"

                    animation_start = now

                    play_sound(
                        sound_wrong
                    )


    # ========================================================
    # ЗАКРЫТИЕ НЕПРАВИЛЬНОЙ ПАРЫ
    # ========================================================

    if (
        len(opened) == 2
        and now >= show_wrong_until
        and not game_finished
    ):

        first = cards[
            opened[0]
        ]

        second = cards[
            opened[1]
        ]

        if first != second:

            opened.clear()

            wrong_pair = []

            player = 1 - player

            animation_type = None


    # ========================================================
    # ФОН
    # ========================================================

    screen.fill(
        (22, 25, 32)
    )


    # ========================================================
    # ЗАГОЛОВОК
    # ========================================================

    title = font_title.render(
        "MEMORY 2.1 — ИГРА ДЛЯ ДВОИХ",
        True,
        (255, 255, 255)
    )

    screen.blit(
        title,
        (
            S(20),
            S(12)
        )
    )


    # ========================================================
    # СЧЁТ
    # ========================================================

    player1 = font_score.render(
        f"Игрок 1: {scores[0]}",
        True,
        (80, 180, 255)
    )

    player2 = font_score.render(
        f"Игрок 2: {scores[1]}",
        True,
        (255, 120, 120)
    )

    screen.blit(
        player1,
        (
            S(20),
            S(62)
        )
    )

    screen.blit(
        player2,
        (
            S(190),
            S(62)
        )
    )


    # ========================================================
    # ТЕКУЩИЙ ИГРОК
    # ========================================================

    current = font_score.render(
        f"Ход игрока {player + 1}",
        True,
        (255, 220, 80)
    )

    screen.blit(
        current,
        (
            S(370),
            S(62)
        )
    )


    # ========================================================
    # ТАЙМЕР
    # ========================================================

    if game_finished:

        elapsed = victory_time

    else:

        elapsed = (
            now
            - game_start_time
        )

    timer_text = font_timer.render(
        "Время: "
        + format_time(
            elapsed
        ),
        True,
        (180, 220, 180)
    )

    screen.blit(
        timer_text,
        (
            S(590),
            S(65)
        )
    )


    # ========================================================
    # РЕКОРД
    # ========================================================

    record_key = str(
        card_count
    )

    if record_key in records:

        record_text = font_small.render(
            "Рекорд: "
            + format_time(
                records[record_key]
            ),
            True,
            (255, 210, 100)
        )

    else:

        record_text = font_small.render(
            "Рекорд: --:--",
            True,
            (180, 180, 180)
        )

    # --------------------------------------------------------
    # Если места достаточно — показываем рекорд отдельно
    # --------------------------------------------------------

    record_x = S(770)

    if WINDOW_WIDTH < S(1400):

        record_x = S(680)

    screen.blit(
        record_text,
        (
            record_x,
            S(68)
        )
    )


    # ========================================================
    # НАДПИСЬ КАРТОЧЕК
    # ========================================================

    cards_text = font_small.render(
        "КАРТОЧЕК:",
        True,
        (210, 210, 210)
    )

    # --------------------------------------------------------
    # Позиция зависит от ширины экрана
    # --------------------------------------------------------

    cards_label_x = (
        buttons_start_x
        - cards_text.get_width()
        - S(10)
    )

    # Если не помещается — ставим в начало
    if cards_label_x < S(5):

        cards_label_x = S(5)

    screen.blit(
        cards_text,
        (
            cards_label_x,
            S(39)
        )
    )


    # ========================================================
    # КНОПКИ КОЛИЧЕСТВА
    # ========================================================

    for count, rect in buttons:

        if count == card_count:

            color = (
                70,
                130,
                220
            )

        else:

            color = (
                55,
                65,
                80
            )


        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=S(8)
        )


        pygame.draw.rect(
            screen,
            (140, 150, 170),
            rect,
            2,
            border_radius=S(8)
        )


        text = font_small.render(
            str(count),
            True,
            (255, 255, 255)
        )


        screen.blit(
            text,
            (
                rect.centerx
                - text.get_width() // 2,

                rect.centery
                - text.get_height() // 2
            )
        )


    # ========================================================
    # КНОПКА ВЫХОДА
    # ========================================================

    pygame.draw.rect(
        screen,
        (110, 55, 55),
        exit_rect,
        border_radius=S(8)
    )


    exit_text = font_small.render(
        "ESC",
        True,
        (255, 255, 255)
    )


    screen.blit(
        exit_text,
        (
            exit_rect.centerx
            - exit_text.get_width() // 2,

            exit_rect.centery
            - exit_text.get_height() // 2
        )
    )


    # ========================================================
    # КАРТОЧКИ
    # ========================================================

    for index in range(card_count):

        row = index // COLS

        col = index % COLS

        base_x = (
            field_x
            + col * (
                CARD_SIZE + GAP
            )
        )

        base_y = (
            field_y
            + row * (
                CARD_SIZE + GAP
            )
        )

        x = base_x

        y = base_y

        draw_size = CARD_SIZE


        # ====================================================
        # АНИМАЦИЯ НЕСОВПАДЕНИЯ
        # ====================================================

        if (
            animation_type == "wrong"
            and index in wrong_pair
        ):

            animation_elapsed = (
                now
                - animation_start
            )

            if animation_elapsed < 450:

                shake = int(
                    math.sin(
                        animation_elapsed
                        * 0.06
                    )
                    * 3
                )

                x += shake


        # ====================================================
        # АНИМАЦИЯ СОВПАДЕНИЯ
        # ====================================================

        if (
            animation_type == "match"
            and index in matched
        ):

            animation_elapsed = (
                now
                - animation_start
            )

            if animation_elapsed < animation_duration:

                progress = (
                    animation_elapsed
                    / animation_duration
                )

                scale = (
                    1.0
                    + 0.12
                    * math.sin(
                        progress
                        * math.pi
                    )
                )

                draw_size = int(
                    CARD_SIZE
                    * scale
                )

                x -= (
                    draw_size
                    - CARD_SIZE
                ) // 2

                y -= (
                    draw_size
                    - CARD_SIZE
                ) // 2


        rect = pygame.Rect(
            x,
            y,
            draw_size,
            draw_size
        )


        # ====================================================
        # ОТКРЫТАЯ КАРТА
        # ====================================================

        if (
            index in opened
            or index in matched
        ):

            image = loaded_images[
                cards[index]
            ]

            image_scaled = pygame.transform.smoothscale(
                image,
                (
                    draw_size,
                    draw_size
                )
            )

            screen.blit(
                image_scaled,
                (
                    x,
                    y
                )
            )


            pygame.draw.rect(
                screen,
                (255, 255, 255),
                rect,
                2
            )


        # ====================================================
        # ЗАКРЫТАЯ КАРТА
        # ====================================================

        else:

            pygame.draw.rect(
                screen,
                (55, 75, 105),
                rect,
                border_radius=S(8)
            )


            pygame.draw.rect(
                screen,
                (110, 130, 160),
                rect,
                2,
                border_radius=S(8)
            )


            mark = font_card.render(
                "?",
                True,
                (210, 220, 235)
            )


            screen.blit(
                mark,
                (
                    x
                    + draw_size // 2
                    - mark.get_width() // 2,

                    y
                    + draw_size // 2
                    - mark.get_height() // 2
                )
            )


    # ========================================================
    # ОКОНЧАНИЕ АНИМАЦИИ СОВПАДЕНИЯ
    # ========================================================

    if animation_type == "match":

        if (
            now
            - animation_start
            >= animation_duration
        ):

            animation_type = None


    # ========================================================
    # ЭКРАН ПОБЕДЫ
    # ========================================================

    if game_finished:

        # ----------------------------------------------------
        # Затемнение
        # ----------------------------------------------------

        overlay = pygame.Surface(
            (
                WINDOW_WIDTH,
                WINDOW_HEIGHT
            )
        )

        overlay.set_alpha(
            205
        )

        overlay.fill(
            (0, 0, 0)
        )

        screen.blit(
            overlay,
            (0, 0)
        )


        # ----------------------------------------------------
        # Победитель
        # ----------------------------------------------------

        if scores[0] > scores[1]:

            winner = (
                "ПОБЕДИЛ ИГРОК 1!"
            )

        elif scores[1] > scores[0]:

            winner = (
                "ПОБЕДИЛ ИГРОК 2!"
            )

        else:

            winner = "НИЧЬЯ!"


        winner_text = font_winner.render(
            winner,
            True,
            (255, 255, 255)
        )


        screen.blit(
            winner_text,
            (
                WINDOW_WIDTH // 2
                - winner_text.get_width() // 2,

                WINDOW_HEIGHT // 2
                - S(150)
            )
        )


        # ----------------------------------------------------
        # Счёт
        # ----------------------------------------------------

        score_text = font_score.render(
            f"{scores[0]} : {scores[1]}",
            True,
            (255, 220, 80)
        )


        screen.blit(
            score_text,
            (
                WINDOW_WIDTH // 2
                - score_text.get_width() // 2,

                WINDOW_HEIGHT // 2
                - S(55)
            )
        )


        # ----------------------------------------------------
        # Время
        # ----------------------------------------------------

        final_time = font_score.render(
            "Время: "
            + format_time(
                victory_time
            ),
            True,
            (180, 220, 180)
        )


        screen.blit(
            final_time,
            (
                WINDOW_WIDTH // 2
                - final_time.get_width() // 2,

                WINDOW_HEIGHT // 2
            )
        )


        # ----------------------------------------------------
        # Новый рекорд
        # ----------------------------------------------------

        if new_record:

            record_text = font_big.render(
                "НОВЫЙ РЕКОРД!",
                True,
                (255, 215, 70)
            )

            screen.blit(
                record_text,
                (
                    WINDOW_WIDTH // 2
                    - record_text.get_width() // 2,

                    WINDOW_HEIGHT // 2
                    + S(60)
                )
            )


        # ----------------------------------------------------
        # Подсказка
        # ----------------------------------------------------

        restart_text = font_small.render(
            "Нажмите мышь или R для новой игры",
            True,
            (220, 220, 220)
        )


        screen.blit(
            restart_text,
            (
                WINDOW_WIDTH // 2
                - restart_text.get_width() // 2,

                WINDOW_HEIGHT - S(80)
            )
        )


    # ========================================================
    # ОБНОВЛЕНИЕ ЭКРАНА
    # ========================================================

    pygame.display.flip()

    clock.tick(60)


# ============================================================
# ВЫХОД
# ============================================================

pygame.quit()
sys.exit()