'''
Sommaire des fonctions pour les algos :
    - pour_y_voir_plus_clair(array)
    - carre(plateau, c)
    - test_danger(plateau, o, x, y)
    - prochaine_arete(o, x, y, Chaine)
    - longueur_chaine(coordo, Chaine)
    - random_arete_dispo(plateau)
    - colorie_chaine(clignote, coordo, Chai ne, couleur_bot)
    - bool_phase_finale(plateau)
    - fin_phase_finale(plateau)
    - nb_arete_chaine(coordo, Chaine)
    - bool_cycle_started(o, x, y, Chaine)
    - nb_cases_vide(Chaine)
    - best3_arete(arete1, arete2, arete3, chaine)
    - trouve_meilleure_arête(chaine)
    - rempli_ce_qui_doit_letre(plateau)
    - trouves_les_meilleurs_arêtes(chaine)
    - aretes_gagnantes(plateau)
    - arete_sure(chaine)
    - fonctions de la double case
        . tue_cycle(clignote, plateau, couleur_bot)
        . que_next1_next2(clignote, plateau, couleur_bot)
        . regle_double_case(clignote, plateau, couleur_bot)
    - coupe_chaine_2(plateau)
    - complète_chaine(coordo, Chaine)
    - arete_sure_existence(plateau)
    - test_grundy(plateau)
    - nombre_grundy(plateau)
    - sprague_grundy(clignote, plateau, c)
    - fonctions du minmax
        . coups_possibles(etat)
        . execute_coup(coup, etat)
        . fin_partie(etat)
        . actions_possibles(coup, etat)
        . execute_action(action, etat)
        . minmax(etat, joueur_maximisant)
        . coup_minmax(etat)
'''

from random import randint
from time import sleep
from copy import deepcopy
from .affichage import dim, draw_carre, draw_arete

time_activation = False
delay = 0.2


def pour_y_voir_plus_clair(array):
    """
    entrée :un tableau [H, V, C]
    effet :print l'état du jeu actuel dans le terminal
    sortie :()
    """
    H_xmax = len(array[0]) - 1
    H_ymax = len(array[0][0]) - 1
    V_xmax = len(array[1]) - 1

    for y in range(H_ymax):  # pour chaque ligne
        for x in range(H_xmax):  # on check chaque arête horizontale
            if array[0][x][y] != 0 :
                print("+--", end="")
            else :
                print("+  ", end="")

        if array[0][H_xmax][y] != 0 :
            print("+--+")
        else :
            print("+  +")

        for x in range(V_xmax):
            if array[1][x][y] != 0 :
                if array[2][x][y] == 1 :
                    print("|XX", end="")
                elif array[2][x][y] == 2 :
                    print("|..", end="")
                else :
                    print("|  ", end="")

            else :
                print("   ", end="")

        if array[1][V_xmax][y] != 0 :
            print("|")
        else :
            print("")
    for x in range(H_xmax):
        if array[0][x][H_ymax] != 0 :
            print("+--", end="")
        else :
            print("+  ", end="")

    if array[0][H_xmax][H_ymax] != 0 :
        print("+--+")
    else :
        print("+  +")


def carre(plateau, c):
    """
    entrée :le plateau sous forme [H, V, C], une couleur 'c'
    effet :colorie en 'c' les carrés pouvant être coloriés
    (ceux non coloriés et entourés de 4 arêtes)
            modifie le plateau en conséquence
    sortie :renvoie true s'il a effectué un coloriage et false sinon
    """
    dimension = dim(plateau)
    trouve = 0
    for i in range(dimension[0] - 1):
        for j in range(dimension[1] - 1):
            if (plateau[0][i][j] != 0 and plateau[0][i][j + 1] != 0):
                if (plateau[1][i + 1][j] != 0 and plateau[1][i][j] != 0):
                    if (plateau[2][i][j] == 0) :
                        if time_activation :
                            sleep((delay / 10))
                        draw_carre(plateau, i, j, c)
                        plateau[2][i][j] = 1
                        trouve = trouve + 1
    if trouve == 0 :
        return False
    else :
        return True


def test_danger(o, x, y, chaine):
    """
    entrée :le plateau sous forme [H, V, C],
    3 entiers o, x, y formant une coordonné d'arête
    effet :test si l'arête o, x, y ne donne aucun point à l'adversaire
    sortie :un booléen
    """
    trouve = 0
    dimension = dim(chaine)
    if o == 0 :
        chaine[0][x][y] = 1
        for i in range(dimension[0] - 1):
            for j in range(dimension[1] - 1):
                if (chaine[0][i][j] == 0 and chaine[0][i][j + 1] == 1):
                    if (chaine[1][i + 1][j] == 1 and chaine[1][i][j] == 1):
                        if (chaine[2][i][j] == 0):
                            trouve = trouve + 1
                elif (chaine[0][i][j] == 1 and chaine[0][i][j + 1] == 0):
                    if (chaine[1][i + 1][j] == 1 and chaine[1][i][j] == 1):
                        if (chaine[2][i][j] == 0):
                            trouve = trouve + 1
                elif (chaine[0][i][j] == 1 and chaine[0][i][j + 1] == 1):
                    if (chaine[1][i + 1][j] == 0 and chaine[1][i][j] == 1):
                        if (chaine[2][i][j] == 0):
                            trouve = trouve + 1
                elif (chaine[0][i][j] == 1 and chaine[0][i][j + 1] == 1):
                    if (chaine[1][i + 1][j] == 1 and chaine[1][i][j] == 0):
                        if (chaine[2][i][j] == 0):
                            trouve = trouve + 1
        chaine[0][x][y] = 0

    if o == 1 :
        chaine[1][x][y] = 1
        for i in range(dimension[0] - 1):
            for j in range(dimension[1] - 1):
                if (chaine[0][i][j] == 0 and chaine[0][i][j + 1] == 1):
                    if (chaine[1][i + 1][j] == 1 and chaine[1][i][j] == 1):
                        if (chaine[2][i][j] == 0):
                            trouve = trouve + 1
                elif (chaine[0][i][j] == 1 and chaine[0][i][j + 1] == 0):
                    if (chaine[1][i + 1][j] == 1 and chaine[1][i][j] == 1):
                        if (chaine[2][i][j] == 0):
                            trouve = trouve + 1
                elif (chaine[0][i][j] == 1 and chaine[0][i][j + 1] == 1):
                    if (chaine[1][i + 1][j] == 0 and chaine[1][i][j] == 1):
                        if (chaine[2][i][j] == 0):
                            trouve = trouve + 1
                elif (chaine[0][i][j] == 1 and chaine[0][i][j + 1] == 1):
                    if (chaine[1][i + 1][j] == 1 and chaine[1][i][j] == 0):
                        if (chaine[2][i][j] == 0):
                            trouve = trouve + 1
        chaine[1][x][y] = 0

    if trouve == 0 :
        return False
    else :
        return True


def prochaine_arete(o, x, y, Chaine):
    """
    entrée : 3 entiers o, x, y formant une coordonné d'arête,
    le plateau sous forme [H, V, C]
    effet :trouve toutes le arêtes permettant de gagner un point
    après avoir joué l'arête (o, x, y)
    sortie :la liste des arêtes suivantes permettant de gagner
    un point sous forme [(o, x, y), ... ]
    avec potentiellement o = 2 si l'arête placée offre un carré directement.
    """
    Chaine[o][x][y] = 1
    dimension = dim(Chaine)
    list_res = []
    # print(o, x, y)
    if o == 0 :  # l'arête est horizontale
        if (y != 0):
            # elle n'est pas sur la ligne du haut :on teste le carré du dessus
            if ((Chaine[0][x][y - 1] == 0) and (Chaine[1][x][y - 1] == 1)):
                if ((Chaine[1][x + 1][y - 1] == 1) and (Chaine[2][x][y - 1] == 0)):
                    # ici l'arête horizontale du dessus
                    list_res.append((0, x, y - 1))
                    # print("on a trouvé au dessus en ", 0,",", x,",", y - 1)
            if ((Chaine[0][x][y - 1] == 1) and (Chaine[1][x][y - 1] == 0)):
                if ((Chaine[1][x + 1][y - 1] == 1) and (Chaine[2][x][y - 1] == 0)):
                    # ici l'arête verticale de gauche
                    list_res.append((1, x, y - 1))
                    # print("on a trouvé au dessus en ", 1,",", x,",", y - 1)
            if ((Chaine[0][x][y - 1] == 1) and (Chaine[1][x][y - 1] == 1)):
                if ((Chaine[1][x + 1][y - 1] == 0) and (Chaine[2][x][y - 1] == 0)):
                    # ici l'arête verticale de droite
                    list_res.append((1, x + 1, y - 1))
                    # print("on a trouvé au dessus en ", 1,",", x + 1,",", y - 1)
            if ((Chaine[0][x][y - 1] == 1) and (Chaine[1][x][y - 1] == 1)):
                if ((Chaine[1][x + 1][y - 1] == 1) and (Chaine[2][x][y - 1] == 0)):
                    list_res.append((2, x, y - 1))
                    # print("c'est la fin de la chaine de ce coté-ci ! (en haut)")

        if (y < dimension[1] - 1):
            # elle n'est pas sur la ligne du bas :on teste le carré du dessous
            if ((Chaine[0][x][y + 1] == 0) and (Chaine[1][x][y] == 1)):
                if ((Chaine[1][x + 1][y] == 1) and (Chaine[2][x][y] == 0)):
                    # ici l'arête horizontale du dessus
                    list_res.append((0, x, y + 1))
                    # print("on a trouvé en dessous en ", 0,",", x,",", y + 1)
            if ((Chaine[0][x][y + 1] == 1) and (Chaine[1][x][y] == 0)):
                if ((Chaine[1][x + 1][y] == 1) and (Chaine[2][x][y] == 0)):
                    # ici l'arête verticale de gauche
                    list_res.append((1, x, y))
                    # print("on a trouvé en dessous en ", 1,",", x,",", y)
            if ((Chaine[0][x][y + 1] == 1) and (Chaine[1][x][y] == 1)):
                if ((Chaine[1][x + 1][y] == 0) and (Chaine[2][x][y] == 0)):
                    # ici l'arête verticale de droite
                    list_res.append((1, x + 1, y))
                    # print("on a trouvé en dessous en ", 1,",", x + 1,",", y)
            if ((Chaine[0][x][y + 1] == 1) and (Chaine[1][x][y] == 1)):
                if ((Chaine[1][x + 1][y] == 1) and (Chaine[2][x][y] == 0)):
                    list_res.append((2, x, y))
                    # print("c'est la fin de la chaine de ce coté-ci ! (en bas)")

    else :  # l'arete est verticale
        if (x != 0):
            # elle n'est pas tout à gauche :on teste le carré de gauche
            if ((Chaine[0][x - 1][y] == 0) and (Chaine[0][x - 1][y + 1] == 1)):
                if ((Chaine[1][x - 1][y] == 1) and (Chaine[2][x - 1][y] == 0)):
                    # ici l'arête horizontale du dessus
                    list_res.append((0, x - 1, y))
                    # print("on a trouvé à gauche en ", 0,",", x - 1,",", y)
            if ((Chaine[0][x - 1][y] == 1) and (Chaine[0][x - 1][y + 1] == 0)):
                if ((Chaine[1][x - 1][y] == 1) and (Chaine[2][x - 1][y] == 0)):
                    # ici l'arête horizontale du dessous
                    list_res.append((0, x - 1, y + 1))
                    # print("on a trouvé à gauche en ", 0,",", x - 1,",", y + 1)
            if ((Chaine[0][x - 1][y] == 1) and (Chaine[0][x - 1][y + 1] == 1)):
                if ((Chaine[1][x - 1][y] == 0) and (Chaine[2][x - 1][y] == 0)):
                    # ici l'arête verticale de gauche
                    list_res.append((1, x - 1, y))
                    # print("on a trouvé à gauche en ", 1,",", x - 1,",", y)
            if ((Chaine[0][x - 1][y] == 1) and (Chaine[0][x - 1][y + 1] == 1)):
                if ((Chaine[1][x - 1][y] == 1) and (Chaine[2][x - 1][y] == 0)):
                    list_res.append((2, x - 1, y))
                    # print("c'est la fin de la chaine de ce coté-ci ! (à gauche)")

        if (x < dimension[0] - 1):
            # elle n'est pas tout à droite :on teste le carré de droite
            if ((Chaine[0][x][y] == 0) and (Chaine[0][x][y + 1] == 1)):
                if ((Chaine[1][x + 1][y] == 1) and (Chaine[2][x][y] == 0)):
                    # ici l'arête horizontale du dessus
                    list_res.append((0, x, y))
                    # print("on a trouvé à droite en ", 0,",", x,",", y)
            if ((Chaine[0][x][y] == 1) and (Chaine[0][x][y + 1] == 0)):
                if ((Chaine[1][x + 1][y] == 1) and (Chaine[2][x][y] == 0)):
                    # ici l'arête horizontale du dessous
                    list_res.append((0, x, y + 1))
                    # print("on a trouvé à droite en ", 0,",", x,",", y + 1)
            if ((Chaine[0][x][y] == 1) and (Chaine[0][x][y + 1] == 1)):
                if ((Chaine[1][x + 1][y] == 0) and (Chaine[2][x][y] == 0)):
                    # ici l'arête verticale de droite
                    list_res.append((1, x + 1, y))
                    # print("on a trouvé à droite en ", 1,",", x + 1,",", y)
            if ((Chaine[0][x][y] == 1) and (Chaine[0][x][y + 1] == 1)):
                if ((Chaine[1][x + 1][y] == 1) and (Chaine[2][x][y] == 0)):
                    list_res.append((2, x, y))
                    # print("c'est la fin de la chaine de ce coté-ci ! (à droite)")

    if list_res == []:
        return False
    else :
        return list_res


def longueur_chaine(coordo, Chaine):
    """
    entrée :une liste d'arêtes sous forme [(o, x, y),...]
    et un plateau sous forme [H, V, C]
    effet :compte récursivement la longueur de la chaine 'fermée' par (o, x, y)
    sortie :un entier donnant le nombre de carré contenus dans la chaine (sa longueur)
    -> ! le plateau passé en entrée est modifié
    -> une chaine 'fermée' est une chaine dont on peut gagner
    tous les carrés en un tour
    """
    res = 0
    # pour toutes les arêtes à tester(on parcours un tableau de 3-uplets
    for i in range(len(coordo)):
        (o, x, y) = coordo[i]  # on extrait le ie 3-uplet
        if Chaine[o][x][y] == 0 :  # si l'arête n'est pas prise ou déjà testée
            if o != 2 :
                # on récupère les arêtes intéressantes suivantes s'il y en a,
                # et oxy est considérée comme prise
                # print(coordo_next)
                coordo_next = prochaine_arete(o, x, y, Chaine)
                if coordo_next:
                    # pour_y_voir_plus_clair(Chaine)
                    res = res + longueur_chaine(coordo_next, Chaine)
            else :
                Chaine[2][x][y] = 1
                # pour_y_voir_plus_clair(Chaine)
                res = res + 1
                # print("on ajoute 1 à la longueur")
    return res


def random_arete_dispo(plateau):
    """
    entrée :un plateau sous forme [H, V, C]
    effet :trouve aléatoirement une arête disponible
    sortie :renvoie (o, x, y) une arête libre au pif et
    renvoie (- 1, 0, 0) s'il n'y en a plus
    """
    [a, b] = dim(plateau)
    for _ in range(100):
        o = randint(0, 1)
        if o == 0 :
            x = randint(0, a - 2)
            y = randint(0, b - 1)
            if (plateau[0][x][y] == 0) :
                return (0, x, y)
        else :
            x = randint(0, a - 1)
            y = randint(0, b - 2)
            if (plateau[1][x][y] == 0) :
                return (1, x, y)

    for i in range(a - 1):
        for j in range(b):
            if (plateau[0][i][j] == 0) :
                return (0, x, y)

    for i in range(a):
        for j in range(b - 1):
            if (plateau[1][i][j] == 0):
                return (0, x, y)
    return (- 1, 0, 0)


def colorie_chaine(clignote, coordo, Chaine, couleur_bot):
    """
    entrée :une arête sous forme (o, x, y),
    un plateau sous forme [H, V, C], une couleur
    effet :colorie entièrement (sur l'écran) la chaine fermée
    par l'arête (o, x, y), et modifie le plateau en conséquence
    sortie :()
    """
    # pour toutes les arêtes à tester (on parcours un tableau de 3-uplets)
    for i in range(len(coordo)):
        (o, x, y) = coordo[i]  # on extrait le ie 3-uplet
        if Chaine[o][x][y] == 0 :  # si l'arête n'est pas prise ou déjà testée
            if o != 2 :
                if time_activation :
                    sleep(delay)
                draw_arete(clignote, Chaine, o, x, y, couleur_bot)
                # on récupère les arêtes intéressantes suivantes s'il y en a,
                # et oxy est considérée comme prise
                coordo_next = prochaine_arete(o, x, y, Chaine)
                # print(coordo_next)
                if coordo_next:
                    # pour_y_voir_plus_clair(Chaine)
                    colorie_chaine(clignote, coordo_next, Chaine, couleur_bot)
            else :
                Chaine[2][x][y] = 1
                # pour_y_voir_plus_clair(Chaine)
                if time_activation :
                    sleep(delay)
                draw_carre(Chaine, x, y, couleur_bot)


def bool_phase_finale(plateau):
    """
    entrée :un plateau sous forme [H, V, C]
    effet :renvoie un booléen signifiant si le plateau vérifie
    la définition de phase finale
    sortie :un booléen

    définition phase finale :
        une fois les chaines ouvertes complétées (celle où on peut gagner des points)
        aucune arête sûre :où que l'on joue on va perdre /
        les chaines restantes sont de longueur au moins 3

    """

    [a, b] = dim(plateau)
    chaine = deepcopy(plateau)
    res = False

    arete = aretes_gagnantes(chaine)
    while (arete):
        (o, x, y) = arete
        long = longueur_chaine([arete], deepcopy(chaine))
        if long >= 2 :
            res = True
        chaine[o][x][y] = 1
        complète_chaine([arete], chaine)
        arete = aretes_gagnantes(chaine)

    for i in range(a - 1):
        for j in range(b):
            if (chaine[0][i][j] == 0 and not test_danger(0, i, j, chaine)) :
                res = False
                chaine[0][i][j] = 1
                # print("arête horizontale :", i, j)
                # pour_y_voir_plus_clair(chaine)
                chaine[0][i][j] = 1

    for i in range(a):
        for j in range(b - 1):
            if (chaine[1][i][j] == 0 and not test_danger(1, i, j, chaine)) :
                res = False
                chaine[1][i][j] = 1
                # print("arête verticale :", i, j)
                # pour_y_voir_plus_clair(chaine)
                chaine[1][i][j] = 1

    if res:
        meilleure_arete = trouve_meilleure_arête(chaine)
        # print("meilleure_arete c'est", meilleure_arete)
        if meilleure_arete[0] <= 2 :
            res = False

    return res


def fin_phase_finale(plateau):
    """
    entrée :un plateau sous forme [H, V, C]
    effet :détermine s'il reste une seule chaine à remplir
    sortie :True ssi le plateau est en fin de phase finale
    """
    plateau_test = deepcopy(plateau)
    dimension = dim(plateau)
    # on rempli tout ce qui doit l'être :
    joue = 1
    while joue != 0 :
        joue = 0
        for i in range(dimension[0] - 1):
            for j in range(dimension[1] - 1):
                if (plateau_test[0][i][j] == 0 and plateau_test[0][i][j + 1] == 1):
                    if (plateau_test[1][i + 1][j] == 1 and plateau_test[1][i][j] == 1):
                        if (plateau_test[2][i][j] == 0) :
                            joue = joue + 1
                            plateau_test[0][i][j] = 1
                            plateau_test[2][i][j] = 1

        for i in range(dimension[0] - 1):
            for j in range(dimension[1] - 1):
                if (plateau_test[0][i][j] == 1 and plateau_test[0][i][j + 1] == 0):
                    if (plateau_test[1][i + 1][j] == 1 and plateau_test[1][i][j] == 1):
                        if (plateau_test[2][i][j] == 0) :
                            joue = joue + 1
                            plateau_test[0][i][j + 1] = 1
                            plateau_test[2][i][j] = 1

        for i in range(dimension[0] - 1):
            for j in range(dimension[1] - 1):
                if (plateau_test[0][i][j] == 1 and plateau_test[0][i][j + 1] == 1):
                    if (plateau_test[1][i + 1][j] == 1 and plateau_test[1][i][j] == 0):
                        if (plateau_test[2][i][j] == 0):
                            joue = joue + 1
                            plateau_test[1][i][j] = 1
                            plateau_test[2][i][j] = 1

        for i in range(dimension[0] - 1):
            for j in range(dimension[1] - 1):
                if (plateau_test[0][i][j] == 1 and plateau_test[0][i][j + 1] == 1):
                    if (plateau_test[1][i + 1][j] == 0 and plateau_test[1][i][j] == 1):
                        if (plateau_test[2][i][j] == 0) :
                            joue = joue + 1
                            plateau_test[1][i + 1][j] = 1
                            plateau_test[2][i][j] = 1

    for i in range(dimension[0] - 1):
        for j in range(dimension[1] - 1):
            if (plateau_test[0][i][j] == 1 and plateau_test[0][i][j + 1] == 1):
                if (plateau_test[1][i + 1][j] == 1 and plateau_test[1][i][j] == 1):
                    if (plateau_test[2][i][j] == 0) :
                        plateau_test[2][i][j] = 1

    res = True
    for i in range(dimension[0] - 1):
        for j in range(dimension[1] - 1):
            if plateau_test[2][i][j] == 0 :
                res = False
    return res


def nb_arete_chaine(coordo, Chaine):
    """
    entrée :un arête sous forme (o, x, y) un plateau sous forme [H, V, C]
    effet :compte le nombre d'arêtes dans la chaine 'fermée'
    par l'arête de coordonée coordo = (o, x, y)
    sortie :le nombre d'arêtes dans la chaine 'fermée'
    par l'arête de coordonée coordo
    -> une chaine 'fermée' est une chaine dont on peut gagner
    tous les carrés en un tour
    """
    res = 0
    for i in range(len(coordo)):
        # pour toutes les arêtes à tester (on parcours un tableau de 3-uplets)
        (o, x, y) = coordo[i]  # on extrait le ie 3-uplet
        if Chaine[o][x][y] == 0 :  # si l'arête n'est pas prise ou déjà testée
            if o != 2 :
                coordo_next = prochaine_arete(o, x, y, Chaine)
                # on récupère les arêtes intéressantes suivantes s'il y en a,
                # et oxy est considérée comme prise
                # print(coordo_next)
                if coordo_next:
                    res = res + 1
                    # pour_y_voir_plus_clair(Chaine)
                    res = res + nb_arete_chaine(coordo_next, Chaine)
            else :
                Chaine[2][x][y] = 1
                # pour_y_voir_plus_clair(Chaine)
    return res


def bool_cycle_started(o, x, y, Chaine):
    """
    entrée :o, x, y 3 entiers correspondant aux coordonnées d'une arête,
    un plateau sous forme [H, V, C]
    effet :renvoie vrai ssi la chaine 'fermée' par l'arête (o, x, y) est un cycle
    sortie :un booléen
    -> une chaine est 'fermée' si on peut gagner tous ses carrés en un tour
    -> un cycle est une chaine qui se referme sur elle-même
    """
    nb_arete = nb_arete_chaine([(o, x, y)], deepcopy(Chaine))
    long = longueur_chaine([(o, x, y)], deepcopy(Chaine))
    res = nb_arete - long
    return res != 0


def nb_cases_vide(Chaine):
    """
    entrée :un plateau sous forme [H, V, C]
    effet :compte le nombre de case non remplie du plateau
    sortie :un entier
    """
    res = 0
    dimension = dim(Chaine)
    for i in range(dimension[0] - 1):  # trace les carrés remplissant
        for j in range(dimension[1] - 1):
            if Chaine[2][i][j] == 0 :
                res = res + 1
    return res


def best3_arete(arete1, arete2, arete3, chaine):
    """
    entrée :trois arêtes différentes sous forme [o, x, y],
    un plateau sous forme [H, V, C]
    effet :trouve l'arête fermant la chaîne la plus courte
    sortie :renvoie le numéro (1, 2 ou 3) de l'arête ayant la chaine la plus courte
    """
    if bool_cycle_started(arete1[0], arete1[1], arete1[2], chaine):
        return 1
    elif bool_cycle_started(arete2[0], arete2[1], arete2[2], chaine):
        return 2
    elif bool_cycle_started(arete3[0], arete3[1], arete3[2], chaine):
        return 3
    else :
        long1 = longueur_chaine([(arete1[0], arete1[1], arete1[2])], deepcopy(chaine))
        long2 = longueur_chaine([(arete2[0], arete2[1], arete2[2])], deepcopy(chaine))
        long3 = longueur_chaine([(arete3[0], arete3[1], arete3[2])], deepcopy(chaine))
        if long1 > long2 and long3 > long2 :
            return 2
        elif long2 > long1 and long3 > long1 :
            return 1
        else :
            return 3


def trouve_meilleure_arête(chaine):
    """
    entrée :un plateau sous forme [H, V, C]
    effet :dans le cas où aucune arête n'est sûre,
    trouve la meilleure arête ie celle qui permet d'ouvrir la chaîne la moins grande
    sortie :un tableau [long, o, x, y] avec long la longueur de la chaine
    que ferme l'arête de coordonnées o, x, y
    """
    [a, b] = dim(chaine)
    meilleure_arete = [a * b, 0, 0, 0]

    for i in range(a):
        for j in range(b - 1):
            copy_chaine = deepcopy(chaine)
            if chaine[1][i][j] == 0 :
                long = longueur_chaine([(1, i, j)], copy_chaine)
                # pour_y_voir_plus_clair(chaine)
                if long:
                    if long < meilleure_arete[0] :
                        if long != 2 :
                            meilleure_arete = [long, 1, i, j]
                        else :
                            if (i != 0 and i != a - 1) :
                                meilleure_arete = [long, 1, i, j]
                else :
                    meilleure_arete = [0, 1, i, j]

    for i in range(a - 1):
        for j in range(b):
            copy_chaine = deepcopy(chaine)
            if chaine[0][i][j] == 0 :
                long = longueur_chaine([(0, i, j)], copy_chaine)
                # pour_y_voir_plus_clair(chaine)
                if long:
                    if long < meilleure_arete[0] :
                        if long != 2 :
                            meilleure_arete = [long, 0, i, j]
                        else :
                            if (j != 0 and j != b - 1) :
                                meilleure_arete = [long, 0, i, j]
                else :
                    meilleure_arete = [0, 0, i, j]

    return meilleure_arete


def trouves_les_meilleurs_arêtes(chaine):
    """
    entrée :un plateau sous forme [H, V, C]
    effet :renvoie la liste des arêtes non prises des chaînes
    de longueur inférieure ou égale à 2
    sortie :une liste sous forme [long, o, x, y]
    avec long la longueur de la chaine que ferme l'arête de coordonnées (o, x, y)
    """
    [a, b] = dim(chaine)
    meilleure_arete = []

    for i in range(a):
        for j in range(b - 1):
            copy_chaine = deepcopy(chaine)
            if chaine[1][i][j] == 0 :
                long = longueur_chaine([(1, i, j)], copy_chaine)
                # pour_y_voir_plus_clair(chaine)
                if long:
                    if long < 3 :
                        list.append(meilleure_arete, [long, 1, i, j])
                else :
                    list.append(meilleure_arete, [0, 1, i, j])

    for i in range(a - 1):
        for j in range(b):
            copy_chaine = deepcopy(chaine)
            if chaine[0][i][j] == 0 :
                long = longueur_chaine([(0, i, j)], copy_chaine)
                # pour_y_voir_plus_clair(chaine)
                if long:
                    if long < 3 :
                        list.append(meilleure_arete, [long, 0, i, j])
                else :
                    list.append(meilleure_arete, [0, 0, i, j])

    return meilleure_arete


def aretes_gagnantes(plateau):
    """
    entrée :un plateau sous forme [H, V, C]
    effet :renvoie une arête permettant de gagner des points et false sinon
    sortie :une arête sous forme (o, x, y) ou False
    """
    dimension = dim(plateau)
    for i in range(dimension[0] - 1):
        for j in range(dimension[1] - 1):
            if (plateau[0][i][j] == 0 and plateau[0][i][j + 1] == 1):
                if (plateau[1][i + 1][j] == 1 and plateau[1][i][j] == 1):
                    if (plateau[2][i][j] == 0) :
                        return (0, i, j)

    for i in range(dimension[0] - 1):
        for j in range(dimension[1] - 1):
            if (plateau[0][i][j] == 1 and plateau[0][i][j + 1] == 0):
                if (plateau[1][i + 1][j] == 1 and plateau[1][i][j] == 1):
                    if (plateau[2][i][j] == 0) :
                        return (0, i, j + 1)

    for i in range(dimension[0] - 1):
        for j in range(dimension[1] - 1):
            if (plateau[0][i][j] == 1 and plateau[0][i][j + 1] == 1):
                if (plateau[1][i + 1][j] == 1 and plateau[1][i][j] == 0):
                    if (plateau[2][i][j] == 0) :
                        return (1, i, j)

    for i in range(dimension[0] - 1):
        for j in range(dimension[1] - 1):
            if (plateau[0][i][j] == 1 and plateau[0][i][j + 1] == 1):
                if (plateau[1][i + 1][j] == 0 and plateau[1][i][j] == 1):
                    if (plateau[2][i][j] == 0) :
                        return (1, i + 1, j)

    return False


def arete_sure(chaine):
    """
    entrée :un plateau sous forme [H, V, C]
    effet :renvoie une arête au pif qui ne donne pas de point à l'adversaire,
    et false sinon
    sortie :une arête sous forme (o, x, y) ou False
    """
    [a, b] = dim(chaine)
    plateau = deepcopy(chaine)

    arete = aretes_gagnantes(plateau)
    while (arete):
        (o, x, y) = arete
        plateau[o][x][y] = 1
        complète_chaine([arete], plateau)
        arete = aretes_gagnantes(plateau)

    # renvoie une arête au pif qui ne présente aucun danger :
    for _ in range(100):
        o = randint(0, 1)
        if o == 0 :
            x = randint(0, a - 2)
            y = randint(0, b - 1)
            if (plateau[0][x][y] == 0 and not prochaine_arete(0, x, y, plateau)) :
                return (0, x, y)
        else :
            x = randint(0, a - 1)
            y = randint(0, b - 2)
            if (plateau[1][x][y] == 0 and not prochaine_arete(1, x, y, plateau)) :
                return (1, x, y)

    # met une arête horizontale si aucun danger
    for i in range(a - 1):
        for j in range(b):
            if (plateau[0][i][j] == 0 and not prochaine_arete(0, i, j, plateau)) :
                return (0, i, j)

    # trace une arête verticale si aucun danger
    for i in range(a):
        for j in range(b - 1):
            if (plateau[1][i][j] == 0 and not prochaine_arete(1, i, j, plateau)) :
                return (1, i, j)
    return False


def tue_cycle(clignote, plateau, couleur_bot):
    """
    entrée :un plateau sous forme [H, V, C], une couleur 'couleur_bot'
    effet :trouve et trace une arête qui gagne un point dans un cycle de longueur < 4
    sortie :renvoie vrai s'il parvient à le faire, et faux sinon
    """
    joue = 0
    dimension = dim(plateau)

    if joue == 0 :
        for i in range(dimension[0] - 1):
            for j in range(dimension[1] - 1):
                if (plateau[0][i][j] == 0 and plateau[0][i][j + 1] == 1):
                    if (plateau[1][i + 1][j] == 1 and plateau[1][i][j] == 1):
                        if (plateau[2][i][j] == 0) :
                            if bool_cycle_started(0, i, j, deepcopy(plateau)) :
                                if longueur_chaine([(0, i, j)], deepcopy(plateau)) < 4:
                                    # pour_y_voir_plus_clair(plateau)
                                    if time_activation :
                                        sleep(delay)
                                    draw_arete(clignote, plateau, 0, i, j, couleur_bot)
                                    joue = joue + 1
                                    plateau[0][i][j] = 1

    if joue == 0 :
        for i in range(dimension[0] - 1):
            for j in range(dimension[1] - 1):
                if (plateau[0][i][j] == 1 and plateau[0][i][j + 1] == 0):
                    if (plateau[1][i + 1][j] == 1 and plateau[1][i][j] == 1):
                        if (plateau[2][i][j] == 0) :
                            if bool_cycle_started(0, i, j + 1, deepcopy(plateau)) :
                                if longueur_chaine([(0, i, j + 1)],
                                                   deepcopy(plateau)) < 4:
                                    # pour_y_voir_plus_clair(plateau)
                                    if time_activation :
                                        sleep(delay)
                                    draw_arete(clignote, plateau, 0, i, j + 1,
                                               couleur_bot)
                                    joue = joue + 1
                                    plateau[0][i][j + 1] = 1

    if joue == 0 :
        for i in range(dimension[0] - 1):
            for j in range(dimension[1] - 1):
                if (plateau[0][i][j] == 1 and plateau[0][i][j + 1] == 1):
                    if (plateau[1][i + 1][j] == 1 and plateau[1][i][j] == 0):
                        if (plateau[2][i][j] == 0) :
                            if bool_cycle_started(1, i, j, deepcopy(plateau)) :
                                if longueur_chaine([(1, i, j)], deepcopy(plateau)) < 4:
                                    # pour_y_voir_plus_clair(plateau)
                                    if time_activation :
                                        sleep(delay)
                                    draw_arete(clignote, plateau, 1, i, j, couleur_bot)
                                    joue = joue + 1
                                    plateau[1][i][j] = 1

    if joue == 0 :
        for i in range(dimension[0] - 1):
            for j in range(dimension[1] - 1):
                if (plateau[0][i][j] == 1 and plateau[0][i][j + 1] == 1):
                    if (plateau[1][i + 1][j] == 0 and plateau[1][i][j] == 1):
                        if (plateau[2][i][j] == 0) :
                            if bool_cycle_started(1, i + 1, j, deepcopy(plateau)) :
                                if longueur_chaine([(1, i + 1, j)],
                                                   deepcopy(plateau)) < 4:
                                    # pour_y_voir_plus_clair(plateau)
                                    if time_activation :
                                        sleep(delay)
                                    draw_arete(clignote, plateau, 1, i + 1, j,
                                               couleur_bot)
                                    joue = joue + 1
                                    plateau[1][i + 1][j] = 1
    if joue == 0 :
        return False
    else :
        return True


def que_next1_next2(clignote, plateau, couleur_bot):
    """
    entrée :un plateau sous forme [H, V, C], une couleur 'couleur_bot' \n
    effet :trouve 2 arêtes gagnantes, et trace toutes les autres gagnantes \n
    sortie :renvoie (False, [- 1, - 1, - 1], [- 1, - 1, - 1])
    si il en a tracé au moins une, et (True, next_arete1, next_arete2) sinon \n
    ! l'algo peut très bien renvoyer (True, [- 1, - 1, - 1], [- 1, - 1, - 1])
    ou (True, next_arete1, [- 1, - 1, - 1]) si il y a moins de 2 arêtes gagnantes.
    """
    joue = 0
    dimension = dim(plateau)
    next_arete1 = [- 1, - 1, - 1]
    next_arete2 = [- 1, - 1, - 1]

    if joue == 0 :  # on check l'arête du dessus de chaque arête horizontale
        for i in range(dimension[0] - 1):
            for j in range(dimension[1] - 1):
                if (plateau[0][i][j] == 0 and plateau[0][i][j + 1] == 1):
                    if (plateau[1][i + 1][j] == 1 and plateau[1][i][j] == 1):
                        if (plateau[2][i][j] == 0) :
                            if next_arete1 == [- 1, - 1, - 1] :
                                next_arete1 = [0, i, j]
                            else :
                                if next_arete1 != [0, i, j] :
                                    if next_arete2 != [0, i, j] :
                                        next_arete2 = [0, i, j]
                                    else :
                                        next_arete3 = [0, i, j]
                                        best_arete = best3_arete(
                                            next_arete1, next_arete2,
                                            next_arete3, plateau)
                                        if best_arete == 3 :
                                            next_arete4 = next_arete3
                                        elif best_arete == 2 :
                                            next_arete4 = next_arete2
                                            next_arete2 = next_arete3
                                        else :
                                            next_arete4 = next_arete1
                                            next_arete1 = next_arete3
                                            if time_activation :
                                                sleep(delay)
                                            draw_arete(clignote, plateau,
                                                       next_arete4[0],
                                                       next_arete4[1],
                                                       next_arete4[2],
                                                       couleur_bot)
                                            if next_arete4[0] == 0 :
                                                plateau[0]
                                                [next_arete4[1]]
                                                [next_arete4[2]] = 1
                                            else :
                                                plateau[1]
                                                [next_arete4[1]]
                                                [next_arete4[2]] = 1
                                            joue = joue + 1

    if joue == 0 :  # on check l'arête du dessous
        for i in range(dimension[0] - 1):
            for j in range(dimension[1] - 1):
                if (plateau[0][i][j] == 1 and plateau[0][i][j + 1] == 0):
                    if (plateau[1][i + 1][j] == 1 and plateau[1][i][j] == 1):
                        if (plateau[2][i][j] == 0) :
                            if next_arete1 == [- 1, - 1, - 1] :
                                next_arete1 = [0, i, j + 1]
                            else :
                                if next_arete1 != [0, i, j + 1] :
                                    if next_arete2 != [0, i, j + 1] :
                                        next_arete2 = [0, i, j + 1]
                                    else :
                                        next_arete3 = [0, i, j + 1]
                                        best_arete = best3_arete(next_arete1,
                                                                 next_arete2,
                                                                 next_arete3,
                                                                 plateau)
                                        # disjonction de cas en cours d'écriture
                                        if best_arete == 3 :
                                            next_arete4 = next_arete3
                                        elif best_arete == 2 :
                                            next_arete4 = next_arete2
                                            next_arete2 = next_arete3
                                        else :
                                            next_arete4 = next_arete1
                                            next_arete1 = next_arete3
                                            if time_activation :
                                                sleep(delay)
                                            draw_arete(clignote, plateau,
                                                       next_arete4[0], next_arete4[1],
                                                       next_arete4[2], couleur_bot)
                                            if next_arete4[0] == 0 :
                                                plateau[0][next_arete4[1]]
                                                [next_arete4[2]] = 1
                                            else :
                                                plateau[1][next_arete4[1]]
                                                [next_arete4[2]] = 1

    if joue == 0 :  # on check l'arête de droite
        for i in range(dimension[0] - 1):
            for j in range(dimension[1] - 1):
                if (plateau[0][i][j] == 1 and plateau[0][i][j + 1] == 1):
                    if (plateau[1][i + 1][j] == 1 and plateau[1][i][j] == 0):
                        if (plateau[2][i][j] == 0) :
                            if next_arete1 == [- 1, - 1, - 1] :
                                next_arete1 = [1, i, j]
                            else :
                                if next_arete1 != [1, i, j] :
                                    if next_arete2 != [1, i, j] :
                                        next_arete2 = [1, i, j]
                                    else :
                                        next_arete3 = [1, i, j]
                                        best_arete = best3_arete(next_arete1,
                                                                 next_arete2,
                                                                 next_arete3,
                                                                 plateau)
                                        # disjonction de cas en cours d'écriture
                                        if best_arete == 3 :
                                            next_arete4 = next_arete3
                                        elif best_arete == 2 :
                                            next_arete4 = next_arete2
                                            next_arete2 = next_arete3
                                        else :
                                            next_arete4 = next_arete1
                                            next_arete1 = next_arete3
                                            if time_activation :
                                                sleep(delay)
                                            draw_arete(clignote, plateau,
                                                       next_arete4[0],
                                                       next_arete4[1],
                                                       next_arete4[2],
                                                       couleur_bot)
                                            if next_arete4[0] == 0 :
                                                plateau[0][next_arete4[1]]
                                                [next_arete4[2]] = 1
                                            else :
                                                plateau[1][next_arete4[1]]
                                                [next_arete4[2]] = 1

    if joue == 0 :  # on check l'arête du gauche
        for i in range(dimension[0] - 1):
            for j in range(dimension[1] - 1):
                if (plateau[0][i][j] == 1 and plateau[0][i][j + 1] == 1):
                    if (plateau[1][i + 1][j] == 0 and plateau[1][i][j] == 1):
                        if (plateau[2][i][j] == 0) :
                            if next_arete1 == [- 1, - 1, - 1] :
                                next_arete1 = [1, i + 1, j]
                            else :
                                if next_arete1 != [1, i + 1, j] :
                                    if next_arete2 != [1, i + 1, j] :
                                        next_arete2 = [1, i + 1, j]
                                    else :
                                        next_arete3 = [1, i + 1, j]
                                        best_arete = best3_arete(next_arete1,
                                                                 next_arete2,
                                                                 next_arete3,
                                                                 plateau)
                                        # disjonction de cas en cours d'écriture
                                        if best_arete == 3 :
                                            next_arete4 = next_arete3
                                        elif best_arete == 2 :
                                            next_arete4 = next_arete2
                                            next_arete2 = next_arete3
                                        else :
                                            next_arete4 = next_arete1
                                            next_arete1 = next_arete3
                                            if time_activation :
                                                sleep(delay)
                                            draw_arete(clignote, plateau,
                                                       next_arete4[0],
                                                       next_arete4[1],
                                                       next_arete4[2],
                                                       couleur_bot)
                                            if next_arete4[0] == 0 :
                                                plateau[0][next_arete4[1]]
                                                [next_arete4[2]] = 1
                                            else :
                                                plateau[1][next_arete4[1]]
                                                [next_arete4[2]] = 1

    if joue == 0 :
        return (True, next_arete1, next_arete2)
    else :
        return (False, [- 1, - 1, - 1], [- 1, - 1, - 1])


def regle_double_case(clignote, plateau, couleur_bot):
    """
    entrée :un plateau sous forme [H, V, C], une couleur 'c' \n
    effet :trace les arêtes qui respectent la règle de la double case
    en prenant en compte le cas des cycles, et modifie le plateau en conséquence \n
    sortie :()
    """
    peut_jouer = True
    # on commence par éliminer les cycles de longueur < 4
    # :on ne peut pas appliquer la règle sur eux
    peut_jouer = not tue_cycle(clignote, plateau, couleur_bot)

    # on part à la recherche des arêtes gagnantes.
    # on fait en sorte d'en garder que 2.
    # si on trouve d'autres arêtes gagnantes que next_arete1 et next_arete2,
    # on trace celles-ci
    (peut_jouer, next_arete1, next_arete2) = que_next1_next2(clignote,
                                                             plateau, couleur_bot)

    if peut_jouer :  # règle de la double case
        if next_arete1 != [- 1, - 1, - 1]:
            # si on a trouvé une arête qui nous fait gagner un point
            if next_arete2 == [- 1, - 1, - 1] :
                # si on en a trouvé qu'une seule, on n'est pas dans un cycle.
                next_arete = next_arete1
            else :
                # si on en a trouvé une 2e,
                # on compare la longueur de leurs chaines respectives.
                long1 = longueur_chaine([(next_arete1[0], next_arete1[1],
                                          next_arete1[2])], deepcopy(plateau))
                long2 = longueur_chaine([(next_arete2[0], next_arete2[1],
                                          next_arete2[2])], deepcopy(plateau))

                if bool_cycle_started(next_arete1[0], next_arete1[1],
                                      next_arete1[2], plateau) and long1 == long2 :
                    next_arete = next_arete1
                    long = long1
                    while long > 4 :  # on va se ramener à un cycle de longeur = 4
                        draw_arete(clignote, plateau, next_arete[0],
                                   next_arete[1], next_arete[2], couleur_bot)
                        plateau[next_arete[0]][next_arete[1]][next_arete[2]] = 1

                        if carre(plateau, couleur_bot) :
                            # si l'arête que l'on vient de tracer
                            # nous fait bien gagner un point.
                            coordo = prochaine_arete(next_arete[0], next_arete[1],
                                                     next_arete[2], plateau)
                            prochaine_i = 0
                            if coordo :
                                (o, x, y) = coordo[0]  # on extrait le 1er 3-uplet
                                while (o == 2 and prochaine_i < len(coordo)):
                                    # le 1er 3-uplet qui est bien un arête (o != 2)
                                    (o, x, y) = coordo[prochaine_i]
                                    prochaine_i += 1
                                next_arete = [o, x, y]
                                # on modifie la valeur de next_arete
                                long = longueur_chaine([(next_arete[0],
                                                         next_arete[1],
                                                         next_arete[2])], deepcopy(
                                                             plateau))

                    # on a maintenant un cycle de longueur 4
                    coordo = prochaine_arete(next_arete[0], next_arete[1],
                                             next_arete[2], deepcopy(plateau))
                    (o, x, y) = coordo[0]
                    prochaine_i = 0
                    while (o == 2 and prochaine_i < len(coordo)):
                        (o, x, y) = coordo[prochaine_i]
                        # on extrait le 1er 3-uplet tq o != 2
                        prochaine_i += 1

                    if plateau[o][x][y] == 0 :
                        # si l'arête n'est pas prise ou déjà testée
                        # on effectue la technique sur un cycle
                        draw_arete(clignote, plateau, o, x, y, couleur_bot)
                        plateau[o][x][y] = 1
                        peut_jouer = False

                elif peut_jouer :
                    # on est pas dans le cas d'un cycle
                    # :on colorie la chaine la plus grande
                    if long1 > long2 :
                        next_arete = next_arete1
                        colorie_chaine(clignote,
                                       [(next_arete2[0],
                                         next_arete2[1],
                                         next_arete2[2])], plateau, couleur_bot)

                    else :
                        next_arete = next_arete2
                        colorie_chaine(clignote,
                                       [(next_arete1[0],
                                         next_arete1[1],
                                         next_arete1[2])], plateau, couleur_bot)

            if peut_jouer :
                # il ne reste plus qu'une arête gagnante,
                # on a réglé son compte à l'autre
                long = longueur_chaine([(next_arete[0], next_arete[1],
                                         next_arete[2])], deepcopy(plateau))

                if long != 2 :
                    draw_arete(clignote, plateau, next_arete[0], next_arete[1],
                               next_arete[2], couleur_bot)
                    plateau[next_arete[0]][next_arete[1]][next_arete[2]] = 1
                    peut_jouer = False

                else :
                    # bon ici on place une arête aux coordonnées d'après,
                    # obtenues à l'aide le la fonction prochaine_arête.
                    coordo = prochaine_arete(
                        next_arete[0],
                        next_arete[1],
                        next_arete[2],
                        deepcopy(plateau))
                    (o, x, y) = coordo[0]
                    prochaine_i = 0
                    while (o == 2 and prochaine_i < len(coordo)):
                        (o, x, y) = coordo[prochaine_i]
                        # on extrait le 1er 3-uplet tq o != 2
                        prochaine_i += 1

                    if plateau[o][x][y] == 0 :
                        # si l'arête n'est pas prise ou déjà testée
                        if time_activation :
                            sleep(delay)
                        draw_arete(clignote, plateau, o, x, y, couleur_bot)
                        plateau[o][x][y] = 1
                        peut_jouer = False


def coupe_chaine_2(plateau):
    """
    entrée :un plateau sous forme [H, V, C]
    effet :
        Si parmis les arêtes disponibles,
        une ferme une chaine de longueur exactement 2 en la coupant en 2,
        on renvoie celle-ci \n
        Sinon on renvoie l'arête qui ferme la plus petite chaine
    sortie :une arête sous forme (o, x, y)
    """
    liste_arete_en_jeu = trouves_les_meilleurs_arêtes(plateau)
    dimension = dim(plateau)
    res = (- 1, 0, 0)
    for tab in liste_arete_en_jeu :
        if tab[0] == 2 :
            if (tab[1] == 0 and tab[3] != dimension[1] - 1 and tab[3] != 0):
                if ((tab[2] == dimension[0] - 1 or tab[2] == 0)) :
                    res = (tab[1], tab[2], tab[3])
            else :
                if (tab[1] == 1 and tab[2] != dimension[0] - 1):
                    if (tab[2] != 0 and (tab[3] == dimension[1] - 1 or tab[3] == 0)) :
                        res = (tab[1], tab[2], tab[3])
    if res == (- 1, 0, 0) :
        tab = trouve_meilleure_arête(plateau)
        return (tab[1], tab[2], tab[3])
    else :
        return res


def complète_chaine(coordo, Chaine):
    """
    entrée :une arête sous forme (o, x, y) un plateau sous forme [H, V, C]
    effet :rempli la chaine fermée par l'arête passée en entrée,
    ie modifie le plateau en conséquence mais ne modifie pas l'écran
    sortie :()
    """
    for i in range(len(coordo)):
        # pour toutes les arêtes à tester(on parcours un tableau de 3-uplets)
        (o, x, y) = coordo[i]  # on extrait le ie 3-uplet
        if Chaine[o][x][y] == 0 :  # si l'arête n'est pas prise ou déjà testée
            if o != 2 :
                coordo_next = prochaine_arete(o, x, y, Chaine)
                # on récupère les arêtes intéressantes suivantes s'il y en a,
                # et oxy est considérée comme prise
                # print(coordo_next)
                if coordo_next :
                    complète_chaine(coordo_next, Chaine)
            else :
                Chaine[2][x][y] = 1


def arete_sure_existence(plateau):
    """
    entrée :un plateau sous forme [H, V, C]
    effet :renvoie True ssi il existe une arête sûre
    (une arête qui ne donne pas de points à l'adversaire)
    sortie :un booléen
    """
    [a, b] = dim(plateau)
    chaine = deepcopy(plateau)

    arete = aretes_gagnantes(chaine)
    while (arete):
        (o, x, y) = arete
        chaine[o][x][y] = 1
        complète_chaine([arete], chaine)
        arete = aretes_gagnantes(chaine)

    res = False

    for i in range(a - 1):
        for j in range(b):
            if (chaine[0][i][j] == 0 and not test_danger(0, i, j, chaine)) :
                res = True

    for i in range(a):
        for j in range(b - 1):
            if (chaine[1][i][j] == 0 and not test_danger(1, i, j, chaine)) :
                res = True

    return res


def test_grundy(plateau):
    """
    entrée :un plateau sous forme [H, V, C]
    effet :determine si on peut appliquer le théorème de sprague-grundy
    sur le plateau donné
    sortie :un booléen
    """
    chaine = deepcopy(plateau)
    return (not arete_sure_existence(chaine)) and (not bool_phase_finale(plateau))


def nombre_grundy(plateau):
    """
    entrée :un plateau sous forme [H, V, C]
    effet :calcul le nombre de grundy
    sortie :renvoie cet entier

    explication calcul du nombre de grundy :
        congruence du nombre de chaines de longueur < 3 modulo 2 :
            s'il vaut 1 :c'est gagnant pour celui qui va joueur
            sinon s'il vaut 0 :c'est plutôt perdant pour celui qui va jouer
        calcul en pratique :
             pour chaque arête interessante (d'une chaine de longueur < 3),
             complète la chaine et ajoute 1
    """
    liste_arete_en_jeu = trouves_les_meilleurs_arêtes(plateau)
    chaine = deepcopy(plateau)
    nb_grundy = 0
    arete_gagnante = aretes_gagnantes(chaine)
    while (arete_gagnante):
        complète_chaine([arete_gagnante], chaine)
        arete_gagnante = aretes_gagnantes(chaine)
    for tab in liste_arete_en_jeu:
        if chaine[tab[1]][tab[2]][tab[3]] == 0 :
            complète_chaine([(tab[1], tab[2], tab[3])], chaine)
            nb_grundy = nb_grundy + 1
            # pour_y_voir_plus_clair(chaine)
    return nb_grundy % 2


def sprague_grundy(clignote, plateau, c):
    """
    entrée :un plateau sous forme [H, V, C], une couleur c
    effet :effectue un tour de jeu de l'algo 5,
    dans le cas où on peut appliquer le théorème de sprague-grundy
    sortie :()

    explication aglo reposant sur sprague grundy :
        si on ne peut pas prendre de point :
            on calcule le nombre de grundy sur ce plateau :
                s'il vaut 1 :le joueur qui doit jouer gagne (ici nous) :
                    combien la longueur de la chaine minimale vaut-elle ?
                        si elle vaut 1 :
                        on prend l'arête correspondante
                        si elle vaut 2 :
                        on prend une arête qui coupe en 2 une chaine de 2
                s'il vaut 0 :le joueur qui doit jouer perd (ici nous) :
                    on prend une arête d'une chaine de longueur 1,
                    en espérant que le joueur adverse ouvre une chaine de 2
                    sans la couper en 2
         si on peut prendre un point :
             si la chaine ouverte est de longueur 1, on a pas de choix:
                on prend ce point et on relance l'algo
                sur le plateau modifié en conséquence
             sinon la chaine ouverte est de longueur 2,
             on a le choix de prendre un point où de le laisser à l'adversaire:
                on calcule le nombre de grundy si les 2 cases sont prises :
                    s'il vaut 1 :ie le joueur qui doit jouer gagne :
                        on prend les deux arêtes. tip :prendre l'arête gagnante.
                    sinon s'il vaut 0 :le joueur qui doit jouer perd :
                        on prend l'arête de la règle de la double case.
    """
    couleur_bot = c
    arete_gagnante = aretes_gagnantes(plateau)
    # peut-on prendre un point ?
    if not arete_gagnante:  # NON on ne peut pas prendre de point
        # déjà, sommes-nous bien dans les conditions ?
        tab = trouve_meilleure_arête(plateau)
        # print("la meilleure arête est", tab)
        if tab[0] > 2 :  # NON la stratégie ne s'applique pas ici
            (o, x, y) = (tab[1], tab[2], tab[3])
            if time_activation :
                sleep(delay)
            draw_arete(clignote, plateau, o, x, y, couleur_bot)
            plateau[o][x][y] = 1
        else :
            nb_grundy = nombre_grundy(plateau)
            # print("nombre de grundy vaut ", nb_grundy)
            if nb_grundy == 1 :  # s'il vaut 1
                # quelle est la longueur de la chaine la plus petite ?
                best_arrete = trouve_meilleure_arête(plateau)
                if best_arrete[0] == 1 :
                    (o, x, y) = (best_arrete[1], best_arrete[2], best_arrete[3])
                    if time_activation :
                        sleep(delay)
                    draw_arete(clignote, plateau, o, x, y, couleur_bot)
                    plateau[o][x][y] = 1
                else :  # cette longueur vaut 2
                    # on coupe une chaine de 2 en 2
                    (o, x, y) = coupe_chaine_2(plateau)
                    if time_activation :
                        sleep(delay)
                    draw_arete(clignote, plateau, o, x, y, couleur_bot)
                    plateau[o][x][y] = 1
            else :  # s'il vaut 0
                # on joue sur une chaine de longueur 1
                best_arrete = trouve_meilleure_arête(plateau)
                o = best_arrete[1]
                x = best_arrete[2]
                y = best_arrete[3]
                if time_activation :
                    sleep(delay)
                draw_arete(clignote, plateau, o, x, y, couleur_bot)
                plateau[o][x][y] = 1
    else :  # OUI on peut prendre un point
        # la longueur de la chaine ouverte est-elle 2 ?
        long = longueur_chaine([arete_gagnante], deepcopy(plateau))
        # print("la longueur de l'arête considérée est", long)
        if long == 1:  # NON elle vaut 1
            # on prend l'arête gagnante et on rejoue
            (o, x, y) = arete_gagnante
            if time_activation :
                sleep(delay)
            draw_arete(clignote, plateau, o, x, y, couleur_bot)
            plateau[o][x][y] = 1
            carre(plateau, c)
            sprague_grundy(clignote, plateau, c)
        else :  # OUI elle est de longueur 2 !
            # on calcule le nb de grundy
            nb_grundy = nombre_grundy(plateau)
            # print("nombre de grundy vaut ", nb_grundy)
            if nb_grundy == 1 :  # si il vaut 1 (on va gagner)
                # on prend le point et on rejoue
                (o, x, y) = arete_gagnante
                if time_activation :
                    sleep(delay)
                draw_arete(clignote, plateau, o, x, y, couleur_bot)
                plateau[o][x][y] = 1
                sprague_grundy(clignote, plateau, c)
            else :  # si il vaut 0 :
                regle_double_case(clignote, plateau, c)
