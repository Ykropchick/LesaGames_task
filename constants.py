import pygame as pg

num_blocked_squares = 6 # кол-во заблокированых квадратов
num_free_squares = 4 # кол-во свободных квадратов
num_colored_squares = 15 # кол-во цветных квадратов
num_color = 3 # кол-во цветов

size_square = (80, 80)  # размер игрвого квадрата
num_row_squares = 5  # кол-во квадратов в одной строке
num_squares = 25  # кол-во всего квадратов
num_types_squares = 3  # кол-во типов квадратов

FPS = 60

font = pg.font.match_font("arial")

mainWindowWidth = num_row_squares * size_square[0] + size_square[0] # ширина игрового поля
mainWindowHeight = num_row_squares * size_square[1] + size_square[1] * 2 # выстоа игрового поля

square_types = {
    'lock': "black",  # залоченное поле, в которую нельзя переставить цветной квадрат
    'free': "white",  # свободное поел, куда можно поставить квадрат
    "colors": ["green", "purple", "brown"]  # цветные поля, которые надо премещать
}
