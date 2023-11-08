

def divEntier(x: int, y: int) -> int:
    try:
        if x < y:
            return 0
    except ValueError:
            print("")
    except RecursionError:
            print ("y ne doit pas etre egal a 0 ou negatif")
    except TypeError:
            print ("y ou a n'est pas un nombre")
    else:
        x = x - y
        return divEntier(x, y) + 1



if __name__ == "__main__":
    divEntier("aa", 0)
    divEntier(25, 10)
