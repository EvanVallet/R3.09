

def divEntier(x: int, y: int) -> int:
    try:
        if x < y:
            return 0
    except ValueError as err:
            print("mettre un nombre")
    except RecursionError as err:
            print ("y ne doit pas etre egal a 0 ou negatif")
    else:
        x = x - y
        return divEntier(x, y) + 1

'''
divEntier("aa",0)
divEntier(25,10)
'''


def ouverture(fichier):
    try:
        fich = open(fichier,'r')
        lect = fich.read()
        print(lect)
    except FileNotFoundError:
        print ("le fichier ",fichier," n'existe pas")

    except PermissionError:
        print ("pas les droit pour ",fichier)
    finally:
        fich = "FIN"
        print(fich)


def ouvertureWhit(fichier):
    try:
        with open('fichier.txt', 'r') as f:
            for l in f:
                l = l.rstrip("\n\r")
    except FileNotFoundError:
        print("le fichier ", fichier, " n'existe pas")

    except PermissionError:
        print("pas les droit pour ", fichier)
    else:
        print(l)
