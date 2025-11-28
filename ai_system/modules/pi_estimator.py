# ai_system/modules/pi_estimator.py
from decimal import Decimal, getcontext
import math

def _with_precision(prec):
    class CM:
        def __init__(self,p): self.p=p; self.old=getcontext().prec
        def __enter__(self): getcontext().prec=self.p
        def __exit__(self, a,b,c): getcontext().prec=self.old
    return CM(prec)

def pi_leibniz(n_terms=1000):
    acc=0.0
    for k in range(n_terms):
        acc += ((-1.0)**k)/(2*k+1)
    return 4.0*acc

def pi_nilakantha(n_terms=1000):
    from decimal import Decimal
    s=Decimal(3)
    with _with_precision(50):
        for k in range(1,n_terms+1):
            term = Decimal(4)/(Decimal(2*k)*Decimal(2*k+1)*Decimal(2*k+2))
            s = s + term if (k%2)==1 else s - term
    return +s

def _arctan_decimal(x, terms=100, prec=80):
    from decimal import Decimal
    x=Decimal(x)
    with _with_precision(prec):
        xpow=x
        s=x
        sign=-1
        for k in range(1,terms):
            denom = Decimal(2*k+1)
            xpow = xpow * (x*x)
            s += Decimal(sign)*(xpow/denom)
            sign *= -1
    return +s

def pi_machin(terms=50, prec=80):
    from decimal import Decimal
    with _with_precision(prec):
        a=_arctan_decimal(Decimal(1)/Decimal(5), terms=terms, prec=prec)
        b=_arctan_decimal(Decimal(1)/Decimal(239), terms=terms, prec=prec)
        pi = (Decimal(4)*a - b) * Decimal(4)
        return +pi

def pi_ramanujan(n_terms=3, prec=80):
    from decimal import Decimal
    with _with_precision(prec):
        factor = Decimal(2) * (Decimal(2).sqrt()) / Decimal(9801)
        s=Decimal(0)
        for k in range(n_terms):
            num = Decimal(math.factorial(4*k)) * Decimal(1103 + 26390*k)
            den = Decimal(math.factorial(k))**4 * (Decimal(396)**(4*k))
            s += num/den
        inv_pi = factor * s
        return + (Decimal(1)/inv_pi)

def estimate_pi(method="ramanujan", n=3, prec=80):
    method = method.lower()
    if method=="ramanujan": return pi_ramanujan(n_terms=n, prec=prec)
    if method=="machin": return pi_machin(terms=n, prec=prec)
    if method=="nilakantha": return pi_nilakantha(n_terms=n)
    if method=="leibniz": return pi_leibniz(n_terms=n)
    raise ValueError("unknown method")
