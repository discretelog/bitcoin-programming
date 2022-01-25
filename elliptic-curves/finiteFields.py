from curves import Point
import unittest

class FieldElement:

    def __init__(self, num, prime):
        # We only want prime fields. Order is always -1 of the prime
        if num >= prime or num < 0:
            error = 'Num {} not in valid range'.format(num, prime-1)
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return 'FieldElement : {}({})'.format(self.prime, self.num)

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        if other is None:
            return False
        return not (self == other)

    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add numbers from different fields')
        result = (self.num + other.num) % self.prime
        return self.__class__(result, self.prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot sub numbers from different fields')
        result = (self.num - other.num) % self.prime
        return self.__class__(result, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot multiply numbers from different fields')
        result = (self.num * other.num) % self.prime
        return self.__class__(result, self.prime)

    # Exponent doesn't have to be from same field
    # a*(p-1) = 1 . Fermat Theorem trick to handle -ve exponents
    def __pow__(self, exponent):
        n = exponent
        while n < 0:
            n += self.prime - 1
        result = pow(self.num, n, self.prime)
        return self.__class__(result, self.prime)

    # Fermat's little theorem trick. division is mult. of inverse ie b ^ p-2
    # so a*(b**p-2)%p
    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot divide numbers from different fields')
        result = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
        return self.__class__(result, self.prime)


class FieldElementTest(unittest.TestCase):

    def test_eq(self):
        a = FieldElement(2, 31)
        b = FieldElement(2, 31)
        self.assertTrue(a == b)

    def test_ne(self):
        a = FieldElement(2, 31)
        b = FieldElement(2, 31)
        c = FieldElement(15, 31)
        self.assertEqual(a, b)
        self.assertTrue(a != c)
        self.assertFalse(a != b)

    def test_add(self):
        a = FieldElement(2, 31)
        b = FieldElement(15, 31)
        c = FieldElement(17, 31)
        self.assertEqual(a + b, c)
        a = FieldElement(17, 31)
        b = FieldElement(21, 31)
        self.assertEqual(a + b, FieldElement(7, 31))

    def test_sub(self):
        a = FieldElement(29, 31)
        b = FieldElement(4, 31)
        self.assertEqual(a - b, FieldElement(25, 31))
        a = FieldElement(15, 31)
        b = FieldElement(30, 31)
        self.assertEqual(a - b, FieldElement(16, 31))

    def test_mul(self):
        a = FieldElement(24, 31)
        b = FieldElement(19, 31)
        self.assertEqual(a * b, FieldElement(22, 31))

    def test_pow(self):
        a = FieldElement(17, 31)
        self.assertEqual(a**3, FieldElement(15, 31))
        a = FieldElement(5, 31)
        b = FieldElement(18, 31)
        self.assertEqual(a**5 * b, FieldElement(16, 31))

    def test_truediv(self):
        a = FieldElement(3, 31)
        b = FieldElement(24, 31)
        self.assertEqual(a / b, FieldElement(4, 31))
        a = FieldElement(17, 31)
        self.assertEqual(a**-3, FieldElement(29, 31))
        a = FieldElement(4, 31)
        b = FieldElement(11, 31)
        self.assertEqual(a**-4 * b, FieldElement(13, 31))


class EccTest(unittest.TestCase):

    def test_on_curve(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = ((192, 105), (17, 56), (1, 193))
        invalid_points = ((200, 119), (42, 99))
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            Point(x, y, a, b)

        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)


if __name__ == '__main__':
    unittest.main()
