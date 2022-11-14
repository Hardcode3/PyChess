"""
@file point.py
@brief Contains the implementation of the class Point
"""


class Point:
    """
    Class Point handling a point instance that con be compared to other Point instances if needed
    """

    def __init__(self, x: int | float = 0, y: int | float = 0):
        self.x_, self.y_ = x, y

    @property
    def x(self):
        return self.x_

    @x.setter
    def x(self, new_x):
        self.x_ = new_x

    @property
    def y(self):
        return self.y_

    @y.setter
    def y(self, new_y):
        self.y_ = new_y

    def distance(self, other) -> int | float:
        return ((other.x_ ** 2 - self.x ** 2) + (other.y_ ** 2 - self.y ** 2)) ** .5

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        return f"Point ({self.x_}, {self.y_})"

    def __abs__(self):
        return Point(abs(self.x_), abs(self.x_))

    def __pos__(self):
        return Point(abs(self.x_), abs(self.y_))

    def __neg__(self):
        return Point(-abs(self.x_), -abs(self.y_))

    def __invert__(self):
        if self.x_ != 0 and self.y_ != 0:
            return Point(1 / self.x_, 1 / self.y_)
        print("Warning, encountered division by zero in Point.__invert__")

    def __eq__(self, other) -> bool:
        return self.x_ == other.x and self.y_ == other.y

    def __ne__(self, other) -> bool:
        return self.x_ != other.x_ and self.y_ != other.y_

    def __add__(self, other):
        return Point(self.x_ + other.x, self.y_ + other.y)

    def __radd__(self, other):
        return NotImplemented

    def __iadd__(self, other) -> None:
        self.x_ += other.x
        self.y_ += other.y

    def __sub__(self, other):
        return Point(self.x_ - other.x, self.y_ - other.y)

    def __rsub__(self, other):
        return NotImplemented

    def __isub__(self, other) -> None:
        self.x_ -= other.x
        self.y_ -= other.y

    def __mul__(self, other):
        return Point(self.x_ * other.x_, self.y_ * other.y_)

    def __rmul__(self, other):
        return NotImplemented

    def __imul__(self, other) -> None:
        self.x_ *= other.x_
        self.y_ *= other.y_

    def __matmul__(self, other):
        return NotImplemented

    def __rmatmul__(self, other):
        return NotImplemented

    def __imatmul__(self, other):
        return NotImplemented

    def __truediv__(self, other):
        return Point(self.x_ / other.x_, self.y_ / other.y_)

    def __rtruediv__(self, other):
        return NotImplemented

    def __itruediv__(self, other) -> None:
        self.x_ /= other.x_
        self.y_ /= other.y_

    def __floordiv__(self, other):
        return NotImplemented

    def __rfloordiv__(self, other):
        return NotImplemented

    def __ifloordiv__(self, other):
        return NotImplemented

    def __mod__(self, other):
        return NotImplemented

    def __rmod__(self, other):
        return NotImplemented

    def __imod__(self, other):
        return NotImplemented

    def __pow__(self, power, modulo=None):
        return NotImplemented

    def __rpow__(self, other):
        return NotImplemented

    def __ipow__(self, other):
        return NotImplemented

    def __rdivmod__(self, other):
        return NotImplemented

    def __lt__(self, other) -> bool:
        if self.x_ < other.x_ and self.y_ < other.y_:
            return True
        return False

    def __le__(self, other) -> bool:
        if self.x_ <= other.x_ and self.y_ <= other.y_:
            return True
        return False

    def __gt__(self, other) -> bool:
        if self.x_ > other.x_ and self.y_ > other.y_:
            return True
        return False

    def __ge__(self, other) -> bool:
        if self.x_ >= other.x_ and self.y_ >= other.y_:
            return True
        return False

    def __len__(self):
        return NotImplemented

    def __lshift__(self, other):
        return NotImplemented

    def __rlshift__(self, other):
        return NotImplemented

    def __ilshift__(self, other):
        return NotImplemented

    def __rshift__(self, other):
        return NotImplemented

    def __rrshift__(self, other):
        return NotImplemented

    def __irshift__(self, other):
        return NotImplemented

    def __and__(self, other):
        return NotImplemented

    def __rand__(self, other):
        return NotImplemented

    def __iand__(self, other):
        return NotImplemented

    def __or__(self, other):
        return NotImplemented

    def __ror__(self, other):
        return NotImplemented

    def __ior__(self, other):
        return NotImplemented

    def __xor__(self, other):
        return NotImplemented

    def __rxor__(self, other):
        return NotImplemented

    def __ixor__(self, other):
        return NotImplemented

    def __complex__(self):
        return NotImplemented

    def __int__(self):
        return NotImplemented

    def __float__(self):
        return NotImplemented

    def __index__(self):
        return NotImplemented

    def __round__(self, n: int = 1):
        if n < 0:
            n = -n
        self.x_ = round(self.x_, n)
        self.y_ = round(self.y_, n)

    def __trunc__(self):
        return NotImplemented

    def __floor__(self):
        return NotImplemented

    def __ceil__(self):
        return NotImplemented


def test_point():
    """
    @brief A simple unit test for Point class
    """
    p1 = Point(1, 1)
    p2 = Point(-1, -1)
    print(p1, p2)
    p1.__repr__()
    p2.__repr__()

    # todo verify distance formula
    if p2.distance(p1) == 8 ** .5 and p1.distance(p2) == 8 ** .5:
        pass
    else:
        print("-> Point : distance() not passed")
    if abs(p1) == p1 and abs(p2) == p1:
        pass
    else:
        print("-> Point : abs() not passed")
    if +p1 == p1 and +p2 == p1:
        pass
    else:
        print("-> Point : pos() not passed")
    if -p1 == p2 and -p2 == p1:
        pass
    else:
        print("-> Point : neg() not passed")
    if ~p1 == Point(1 / p1.x_, 1 / p1.y_) and ~p2 == Point(1 / p2.x_, 1 / p2.y_):
        pass
    else:
        print("-> Point : invert() not passed")
    if p1 == Point(1, 1):
        pass
    else:
        print("-> Point : equal() not passed")
    if p1 != p2:
        pass
    else:
        print("-> Point : not equal() not passed")
    if p1 + p2 == Point(0, 0):
        pass
    else:
        print("-> Point : add() not passed")
    

if __name__ == '__main__':
    test_point()
