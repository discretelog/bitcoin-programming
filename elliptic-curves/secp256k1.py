from finiteFields import FieldElement
from curves import Point

class S256Field(FieldElement):

    p = 2**256 - 2**32 - 977
    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=p)

    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)


class S256Point(Point):

    A = 0
    B = 7
    N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    def __init__(self, x, y, a=None, b=None):
        a, b = S256Filed(A), S256Filed(B)
        if type(x) == int:
            super.__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        #Infinity point
        else:
            super.__init__(x=x, y=y, a=a, b=b)

    def __rmul__(self, coefficient):
        coef = coefficient % N
        return super.__rmul__(coef)

    def verify(self, z, sig):
        s_inv = pow(sig.s, N - 2, N)
        u = z * s_inv % N
        v = sig.r * s_inv % N
        total = u * G + v * self
        return total.x.num == sig.r

G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)

class Signature:

    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return 'Signature({:x}{:x})',format(self.r, self.s)