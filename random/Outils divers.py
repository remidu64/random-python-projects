from decimal import *
from numpy import *
from matplotlib import pyplot as plt
import sympy
from sympy import solve

x = 0
y = 0

X = sympy.symbols("x")





def GDC(x, y):
    x = Decimal(x)
    y = Decimal(y)

    if y == 0:  # algorithme d'Euclide
        return x

    r = int(x % y)
    return GDC(y, r)


def Fsimp(x, y):
    D = GDC(x, y)  # appel de GDC

    print(x / D, "/", y / D)


def conv2(n):
    res = ""
    while n > 0:  # divisions par 2 succesives
        res += str(n % 2)
        n //= 2

    res += "b0"
    res = res[::-1]  # inversion de la chaîne de caractere avec du slicing
    return res

def f(input,func):
    code = "x = " + input + "\n" + "x = " + func + "\n" + "print(x)"
    print(code)
    exec(compile(code,"Outils divers.py","exec"))

def graph(infbound, supbound,sy,prec):
    global y
    y = 0
    global x
    adaprec = prec * (supbound - infbound)
    print(adaprec)
    x = linspace(infbound, supbound,adaprec)

    ycode = "global y \n"+"y = " + input("équation -->")

    ycode = compile(ycode, "Outils divers.py", "exec")

    exec(ycode)

    plt.plot(x,y,sy)
    plt.show()



def a():
    x = 0
    while 1.3 * x < x + 10:
        print(1.3 * x)
        print(x + 10)
        print(x)
        x += 1
    return x

def angle_principal(nume, deno):
    r = nume % (deno)
    r2 = (nume - r) // (deno)
    if nume < 0:
        r -= deno
        r2 += 1
    print(f"({r} X pi / {deno}) + {r2} X 2 X pi")
















