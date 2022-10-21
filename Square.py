import pygame as pg
import constants


class Square(pg.sprite.Sprite):
    def __init__(self, x, y, _type, size=constants.size_square):
        pg.sprite.Sprite.__init__(self)

        # если это любой тип, кроме цветного, то срабатывает этот слчай и вытаскивает цвет
        if _type in constants.square_types:
            self.color = constants.square_types[_type]
            self.type = _type
        else:
            # если это тип цветной, то выбираеться этот случай
            self.color = _type
            self.type = "colors"

        # создаеться поверхность квадрата
        self.square_sur = pg.Surface(size)
        # краситься
        self.square_sur.fill(self.color)
        # делаться окантовка
        pg.draw.rect(self.square_sur, "gray", self.square_sur.get_rect(), 2)

        # self.type = _type

        self.image = self.square_sur
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.is_selected = False

    def set_position(self, coordinates):
        """
        изменяет координаты квадрата
        :param coordinates: tuple
        :return: None
        """
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
        return self.rect.x

    def get_position(self):
        """
        Возвращает текущие координаты квадрата
        :return: tuple
        """
        return self.rect.x, self.rect.y

    def selected(self):
        """
        выделяет квадрат красной окантовкой, что означает, что он выбранн
        :return: None
        """
        pg.draw.rect(self.square_sur, "red", self.square_sur.get_rect(), 5)
        self.is_selected = True

    def unselected(self):
        """
        выделяет квадрат серой окантовкой, что означет, что он не выбран
        :return: None
        """
        pg.draw.rect(self.square_sur, "gray", self.square_sur.get_rect(), 5)
        self.is_selected = False
