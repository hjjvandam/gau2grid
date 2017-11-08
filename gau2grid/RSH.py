import numpy as np

# Arbitrary precision math with 100 decimal places
import mpmath
mpmath.mp.dps = 100

def quanta_to_string(lx, ly, lz):
    """Pretty print monomials with quanta lx, ly, lz."""
    string = ""
    if lx:
        string += 'x'
    if lx > 1:
        string += '^{}'.format(lx)
    if ly:
        string += 'y'
    if ly > 1:
        string += '^{}'.format(ly)
    if lz:
        string += 'z'
    if lz > 1:
        string += '^{}'.format(lz)
    return string


def cart_to_RSH(l):
    """
    Generates a coefficients [ coef, x power, y power, z power ] for each component of
    a regular solid harmonic (in terms of raw Cartesians) with angular momentum l.

    See eq. 23 of ACS, F. C. Pickard, H. F. Schaefer and B. R. Brooks, JCP, 140, 184101 (2014)
    """

    terms = {}
    for m in range(l + 1):
        thisterm = {}
        # p1 = mpmath.sqrt(mpmath.fac(l - m / mpmath.fac(l + m))) * (mpmath.fac(m) / (2**l))
        p1 = mpmath.sqrt((mpmath.fac(l - m)) / (mpmath.fac(l + m))) * ((mpmath.fac(m)) / (2**l))
        if m:
            p1 *= mpmath.sqrt(2.0)
        # Loop over cartesian components
        for lz in range(l + 1):
            for ly in range(l - lz + 1):
                lx = l - ly - lz
                xyz = lx, ly, lz
                j = int((lx + ly - m) / 2)
                if ((lx + ly - m) % 2 == 1 or j < 0):
                    continue
                p2 = mpmath.mpf(0)
                for i in range(int((l - m) / 2) + 1):
                    if i >= j:
                        p2 += (-1)**i * mpmath.fac(2 * l - 2 * i) / (
                            mpmath.fac(l - i) * mpmath.fac(i - j) * mpmath.fac(l - m - 2 * i))
                p3 = mpmath.mpf(0)
                for k in range(j + 1):
                    if j >= k and lx >= 2 * k and m + 2 * k >= lx:
                        p3 += (-1)**k / (
                            mpmath.fac(j - k) * mpmath.fac(k) * mpmath.fac(lx - 2 * k) * mpmath.fac(m - lx + 2 * k))
                p = p1 * p2 * p3
                # print(p)
                if xyz not in thisterm:
                    thisterm[xyz] = [mpmath.mpf(0.0), mpmath.mpf(0.0)]

                if (m - lx) % 2:
                    # imaginary
                    sign = mpmath.mpf(-1.0) ** mpmath.mpf((m - lx - 1) / 2.0)
                    thisterm[xyz][1] += sign * p
                else:
                    # real
                    sign = mpmath.mpf(-1.0) ** mpmath.mpf((m - lx) / 2.0)
                    thisterm[xyz][0] += sign * p

        tmp_R = []
        tmp_I = []
        for k, v in thisterm.items():
            if v[0] > 0:
                tmp_R.append((k, v[0]))
            if v[1] > 0:
                tmp_I.append((k, v[1]))

        if m == 0:
            name_R = "R_%d%d" % (l, m)
            terms[name_R] = tmp_R
        else:
            name_R = "R_%d%dc" % (l, m)
            name_I = "R_%d%ds" % (l, m)
            terms[name_R] = tmp_R
            terms[name_I] = tmp_I

    # for k, v in terms.items():
    #     print(k, v)

    return terms