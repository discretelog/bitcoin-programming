
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
