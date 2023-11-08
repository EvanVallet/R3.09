
def divEntier(x: int, y: int) -> int:
    if y == 0:
        raise ValueError("y = 0 donc impossible")
    if y <= 0 or x < 0:
        raise ValueError("x ou y negatif")
    if x < y:
        return 0

    else:
        x = x - y
        return divEntier(x, y) + 1


if __name__ == "__main__":
    flag = False
    while not flag:
        try:
            x = int(input('x ?'))
            y = int(input('y ?'))
        except ValueError:
            print('erreur de saisie')
        else:
            flag = True
    try:
        a=divEntier(x,y)
    except ValueError as err:
        print(err)
    else:
        print(a)



