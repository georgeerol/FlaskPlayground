class Rectangle:
    def __init__(self, width, height):
        self._height = height
        self._width = width

    @property
    def area(self):
        return self._width * self._height

    def __str__(self):
        return 'Width: {}, height: {}'.format(self.width, self.height)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value


# Break liskov substitution
class Square(Rectangle):
    def __init__(self, size):
        Rectangle.__init__(self, size, size)

    @Rectangle.width.setter
    def width(self, value):
        _width = _height = value

    @Rectangle.height.setter
    def height(self, value):
        _width = _height = value


def use_it(rc):
    w = rc.width
    rc.height = 10  # unpleasant side effect
    expected = int(w * 10)
    print('Expected an area of {}, got {}'.format(expected, rc.area))


rc = Rectangle(2, 3)
use_it(rc)

sq = Square(5)
use_it(sq)
