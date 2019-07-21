def interpol(xa, ya, xb, yb, x):
    #voor path x = tijd ya en yb = pos
    m = float(yb - ya)/float(xb - xa)
    q = ya - m*xa
    return m*x + q

if __name__ == '__main__':
    print(interpol(0, 0, 20, 1, 40))