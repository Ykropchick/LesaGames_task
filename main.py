import pygame as pg
import constants
from Square import Square
import random
from collections import Counter


pg.init()
screen = pg.display.set_mode((constants.mainWindowWidth, constants.mainWindowHeight))



def init_field() -> list[list]:
    """
     Инициализирует игровое поле и координаты квадратов, заполненное free квадратами
    """
    field = []
    for i in range(constants.num_row_squares):
        for j in range(1, constants.num_row_squares + 1):
            field.append([constants.size_square[0] // 2 + (i * constants.size_square[0]), (j * constants.size_square[1] + constants.size_square[1] // 2) , "free", (j, i)])
    return field


def blocked_column(column: list) -> bool:
    """
     Пороверяет нет заполнена ли вся колонка заблоченнами квадратами
    """
    if column.count("lock") == constants.num_row_squares:
        return False
    return True


def set_locked_squares(field : list[list]) -> None:
    """
    Инициализирует заблокированными квадратами
    """
    num_blocked_columns = constants.num_row_squares - constants.num_types_squares
    valid_x = []
    valid_y = [i for i in range(1, constants.num_row_squares + 1)]
    blocked_squares = 0
    # выбирает допустимые x, проверяя, чтобы остались достаточное кол-во места для каждого квадрата
    while num_blocked_columns != len(valid_x):
        x = random.randint(0, constants.num_row_squares - 1)
        if all([i not in valid_x for i in [x + 1, x, x - 1]]):
            valid_x.append(x)

    num_row_blocked = {}

    while blocked_squares != constants.num_blocked_squares:

        x = random.choice(valid_y)
        y = random.choice(valid_x)

        if x not in num_row_blocked:
            num_row_blocked[x] = 1
        else:
            num_row_blocked[x] += 1

        if num_row_blocked[x] >= 5:
            continue

        for cell in field:
            if (x, y) in cell and cell[2] != "lock":
                cell[2] = "lock"
                blocked_squares += 1
    return valid_x


def set_colored_square(field: list[list]) -> None:
    """
    Инициализирует цветными квадратами
    """
    num_each_color = constants.num_colored_squares // constants.num_color

    for color in constants.square_types['colors']:
        shaded_color = 0
        while shaded_color != num_each_color:
            square = random.choice(field)
            if square[2] == "free":
                square[2] = color
                shaded_color += 1



def set_upper_square(valid_x, valid_colors):
    """
    Создает верхние квадраты, которые обзоначают какой надо цвет собрать
    """
    pg.draw.line(screen, "red", (0, constants.size_square[0] * 1.5 - 2), (constants.mainWindowWidth, constants.size_square[1] * 1.5 - 2), 5)

    color = 0

    for i in valid_x:
        pg.draw.rect(screen, valid_colors[color], (constants.size_square[0] // 2 + constants.size_square[0] * i, constants.size_square[1] // 2 - 3, constants.size_square[0], constants.size_square[1]))
        color += 1






def start_game() -> tuple:
    """
    Инициализирует sprite.Group, так же выбирает какая клетка будет selected, клетка всегда цветная
    """
    squares = pg.sprite.Group()

    for i in range(constants.num_squares):
        squares.add(Square(*field[i][0:3]))

    while(True):
        square = random.choice(squares.sprites())
        index_selected = 0
        if square.type == "colors":
            square.selected()
            index_selected = squares.sprites().index(square)
            break
        else:
            continue
    return squares, index_selected


def swap_squares(square_1: Square, square_2: Square) -> None:
    """
    Меняет квадраты, путем переписывания squares
    """
    pos_1, pos_2 = square_1.get_position(), square_2.get_position()
    square_1.set_position(pos_2)
    square_2.set_position(pos_1)


def move_square(sprites: list, index_selected: int, direction: int) -> int:
    """
     Перемещает квадрат,
     direction это чилсо на какую клетку надо переместить
     возвращает индекс выделенной клетки
    """
    swap_squares(sprites[index_selected], sprites[index_selected + direction])
    # путем свапа мы сохрянаеи правильный порядок
    sprites[index_selected], sprites[index_selected + direction] = \
        sprites[index_selected + direction], sprites[index_selected]

    # переписываем squares
    squares.empty()
    squares.add(sprites)

    index_selected = index_selected + direction

    return index_selected


def draw_text(surface, text, size, x, y):
    font = pg.font.Font(constants.font, size)
    text_surface = font.render(text, True, "yellow")
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)
    pg.display.update()



def draw_game_over_screen():
    screen.fill("purple")
    draw_text(screen, "You win :)", constants.mainWindowWidth // 15, constants.mainWindowWidth // 2, constants.mainWindowHeight // 2)
    draw_text(screen, "Press Escape to restart", constants.mainWindowWidth // 15, constants.mainWindowWidth // 2, constants.mainWindowHeight // 2 + constants.mainWindowHeight // 20)
    pg.display.update()
    waiting = True
    while waiting:
        clock.tick(constants.FPS)
        for _event in pg.event.get():
            if _event.type == pg.QUIT:
                pg.quit()
            if _event.type == pg.KEYDOWN:
                if _event.key == pg.K_RETURN:
                    waiting = False





def is_win(sprites):
    completed_columns = []
    for x in opened_x:
        column = sprites[x*5:x*5 + 5]
        types = [cell.color for cell in column]
        if len(set(types)) == 1:
            completed_columns.append(True)
        else:
            completed_columns.append(False)
    return True if all(completed_columns) else False





field = init_field()
blocked_x = set_locked_squares(field)
set_colored_square(field)
opened_x = [x for x in range(constants.num_row_squares) if x not in blocked_x]
random.shuffle(opened_x)
valid_colors = constants.square_types["colors"]
random.shuffle(valid_colors)
set_upper_square(opened_x, valid_colors)
squares, index_selected = start_game()
ready_move = False
clock = pg.time.Clock()

count = 0
while True:
    clock.tick(constants.FPS)

    if is_win(squares.sprites()):
        draw_game_over_screen()
        field = init_field()
        blocked_x = set_locked_squares(field)
        set_colored_square(field)
        opened_x = [x for x in range(constants.num_row_squares) if x not in blocked_x]
        random.shuffle(opened_x)
        valid_colors = constants.square_types["colors"]
        random.shuffle(valid_colors)
        set_upper_square(opened_x, valid_colors)
        squares, index_selected = start_game()
        ready_move = False

    for event in pg.event.get():
        if count == 0:
            count += 1
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN and squares.sprites()[index_selected].type == "colors":
                ready_move = False if ready_move else True
            # смена место клеток. Был нажат enter
            if ready_move:
                # переводит Group в list
                sprites = squares.sprites()
                # перемещение квадрата навверх так же проверка на выход за границы, сначала нужна проверка,
                # чтобы не обращался по индексу по не сущ элементу массива
                if event.key == pg.K_UP and 0 <= index_selected - 1 <= 24 and sprites[index_selected].type == "colors" and sprites[index_selected - 1].type == "free":
                    cur_sprites = squares.sprites()

                    index_selected = move_square(cur_sprites, index_selected, -1)

                # перемещение квадрата вниз так же проверка на выход за границы, сначала нужна проверка,
                # чтобы не обращался по индексу по не сущ элементу массива
                if event.key == pg.K_DOWN and 0 <= index_selected + 1 <= 24 and sprites[index_selected].type == "colors" and sprites[index_selected + 1].type == "free":

                    cur_sprites = squares.sprites()

                    index_selected = move_square(cur_sprites, index_selected, 1)

                # перемещение квадрата вправо, так же проверка на выход за границы, сначала нужна проверка,
                # чтобы не обращался по индексу по не сущ элементу массива
                if event.key == pg.K_RIGHT and 0 <= index_selected + 5 <= 24  and sprites[index_selected].type == "colors" \
                        and sprites[index_selected + 5].type == "free":
                    cur_sprites = squares.sprites()

                    index_selected = move_square(cur_sprites, index_selected, 5)

                # перемещение квадрата влево так же проверка на выход за границы, сначала нужна проверка,
                # чтобы не обращался по индексу по не сущ элементу массива
                if event.key == pg.K_LEFT and 0 <= index_selected - 5 <= 24 and sprites[index_selected].type == "colors" and sprites[index_selected - 5].type == "free":
                    cur_sprites = squares.sprites()

                    index_selected = move_square(cur_sprites, index_selected, -5)




            # смена выбранной клетки. не был нажат enter
            else:
                match event.key:
                    case pg.K_UP:
                        try:
                            if not(0 <= index_selected - 1 <= 24):
                                continue
                            squares.sprites()[index_selected - 1].selected()
                            squares.sprites()[index_selected].unselected()
                            index_selected -= 1
                        except IndexError as e:
                            pass
                    case pg.K_DOWN:
                        try:
                            if not(0 <= index_selected + 1 <= 24):
                                continue
                            squares.sprites()[index_selected + 1].selected()
                            squares.sprites()[index_selected].unselected()
                            index_selected += 1
                        except IndexError as e:
                            pass

                    case pg.K_RIGHT:
                        try:
                            if not(0 <= index_selected + 1 <= 24):
                                continue
                            squares.sprites()[index_selected + 5].selected()
                            squares.sprites()[index_selected].unselected()
                            index_selected += 5
                        except IndexError as e:
                            pass
                    case pg.K_LEFT:
                        try:
                            if not(0 <= index_selected - 5 <= 24):
                                continue
                            squares.sprites()[index_selected - 5].selected()
                            squares.sprites()[index_selected].unselected()
                            index_selected -= 5
                        except IndexError as e:
                            pass





    squares.update()
    screen.fill("yellow")
    set_upper_square(opened_x, valid_colors)
    squares.draw(screen)
    pg.display.update()