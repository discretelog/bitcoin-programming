
class Point:

    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b

        # infinity point
        if self.x is None and self.y is None:
            return
        if y ** 2 != (self.x ** 3 + self.a * self.x + self.b):
            raise ValueError('({} {}) is not a point on the curve'.
                format(self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and \
               self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError('Points {}, {} are not on the same curve'.format
                             (self, other))
        if self.x is None:
            return other
        if other.x is None:
            return self

        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, a, b)

        # x and y both are different. Reflect the point. Derived formulas
        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            # new point
            x = s ** 2 - self.x - other.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

        # When points are same. Tangent to curve , derived formulas
        if self == other:
            s = (3 * self.x**2 + self.a) / (2 * self.y)
            x = s ** 2 - 2 * self.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

        if self == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)


