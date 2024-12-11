"""
Sommaire :
    # importation

    # interface de jeu et game loop :
        - fonction de clic
        - définition des variables de jeu
        - boucle de jeu :
            . boucle de menu
            . boucle de choix de dimension pour pvp
            . boucle de choix de niveau de robot pour pvr
            . boucle de choix de dimension pour pvr
            . boucle de choix de niveaux de robots pour rvr
            . boucle de choix de dimension pour rvr
            . boucle de choix des couleurs
            . boucle de partie :
                > boucle de jeu pvp
                > boucle de jeu pvr
                > boucle de jeu rvr

"""

import logging
from pygame import display, mixer, init, event
from pygame import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, KEYDOWN, K_m, K_r, K_p
from copy import deepcopy
from affichage import dim, draw_arete, width, height, initialise_menu, screen
from affichage import menu_robot, menu_couleur, menu_robots_battle, dimension_menu
from affichage import bouton_main_menu, bouton_dimension_menu, reset
from affichage import bouton_menu_couleur, bouton_menu_robots
from affichage import clic_bouton, clic_bouton_dimension, bouton_robots_battle
from affichage import clic_bouton_robot, clic_robots_battle, clic_menu_couleur
from affichage import bgColor, C1_BLUE, BLEU_FONCE, attribue_color
from fonctions_de_jeu import longueur_chaine, carre, nb_cases_vide
from algos import Turn, robot0, robot1, algo1, algo2, algo3, algo4

# Désactiver le mixer audio
mixer.quit()

init()

points_j1 = 0
points_j2 = 0


# minmax : (ces fonctions sont finalement inutilisées)
def coups_possibles(etat):
    """
    entrée : un plateau "etat" donné sous forme [H, V, C]
    effet : recense les arêtes des chaines de longueur <= 2
    sortie : liste des coups possibles. chaque coup est de la forme (o, x, y)
    """
    dimension = dim(etat)
    coups = []
    for i in range(dimension[0] - 1):
        for j in range(dimension[1]):
            if etat[0][i][j] == 0 and longueur_chaine([(0, i, j)],
                                                      deepcopy(etat)) <= 2 :
                coups.append((0, i, j))
    for i in range(dimension[0]):
        for j in range(dimension[1] - 1):
            if etat[1][i][j] == 0 and longueur_chaine([(1, i, j)],
                                                      deepcopy(etat)) <= 2 :
                coups.append((1, i, j))
    return coups


def execute_coup(coup, etat):
    """
    entrée : une arête sous forme (o, x, y) et un plateau "etat" sous forme [H, V, C]
    sortie : le nouvel état de l'environnement,
    le nombre de case gagné en jouant le coup
    """
    dimension = dim(etat)
    (o, x, y) = coup
    new_etat = deepcopy(etat)
    if new_etat[o][x][y] != 0 :
        return (etat, - dimension[0] * dimension[1])
    else :
        new_etat[o][x][y] = 1
        nb_case_prise = 0
        if o == 0 :
            # on teste le carré du dessus
            if y > 0 :
                # il y a dimension[1] lignes horizontales,
                # donc la dernière est à l'ordonnée y = dimension[1]
                if (new_etat[0][x][y - 1] != 0 and new_etat[1][x][y - 1] != 0):
                    if (new_etat[1][x + 1][y - 1] != 0 and new_etat[2][x][y - 1] == 0):
                        new_etat[2][x][y - 1] = 1
                        nb_case_prise += 1
            # on teste le carré du dessous
            if y < dimension[1] - 1 :
                if (new_etat[0][x][y + 1] != 0 and new_etat[1][x][y] != 0):
                    if (new_etat[1][x + 1][y] != 0 and new_etat[2][x][y] == 0):
                        new_etat[2][x][y] = 1
                        nb_case_prise += 1
        if o == 1 :
            # on teste le carré de gauche
            if x > 0 :
                if (new_etat[0][x - 1][y] != 0 and new_etat[0][x - 1][y + 1] != 0):
                    if (new_etat[1][x - 1][y] != 0 and new_etat[2][x - 1][y] == 0):
                        new_etat[2][x - 1][y] = 1
                        nb_case_prise += 1
            # on teste le carré de droite
            if x < dimension[0] - 1 :
                # il y a dimension[0] lignes verticales,
                # donc la dernière est à l'abscisse x = dimension[0]
                if (new_etat[0][x][y] != 0 and new_etat[0][x][y + 1] != 0):
                    if (new_etat[1][x + 1][y] != 0 and new_etat[2][x][y] == 0):
                        new_etat[2][x][y] = 1
                        nb_case_prise += 1

    return (new_etat, nb_case_prise)


def fin_partie(etat):
    """
    entrée : un plateau "etat" donné sous forme [H, V, C]
    sortie : un booléen valant true ssi la partie est finie
    """
    return coups_possibles(etat) == []


def actions_possibles(coup, etat):
    """
    entrée : un coup sous forme (o, x, y),
             un plateau "etat" donné sous forme [H, V, C]
    sortie : un tableau contenant toutes les actions possibles à partir du coup "coup".
    """
    (new_etat, nb_cases_remplies) = execute_coup(coup, etat)
    liste_actions = [[coup]]
    if nb_cases_remplies != 0 :  # si après avoir joué "coup" on peut rejouer
        liste_actions = []
        for coup_next in coups_possibles(new_etat):
            suite_coup_next = actions_possibles(coup_next, new_etat)
            for suite in suite_coup_next :
                liste_actions.append([coup] + suite)
    return liste_actions


def execute_action(action, etat):
    # Effectuer l'action sur l'etat et renvoyer le nouvel etat
    """
    entrée : une liste de coup et un plateau "etat" sous forme [H, V, C]
    effet : exécute la séquence de coups 'action' sur le plateau
    sortie : le nouvel état de l'environnement,
    le nombre de case gagné en jouant l'action
    """
    plateau = etat
    for coup in action :
        (new_etat, _) = execute_coup(coup, plateau)
        plateau = new_etat
    return plateau


def minmax(etat, joueur_maximisant):
    if fin_partie(etat) and joueur_maximisant:
        return 1
    elif fin_partie(etat) and not joueur_maximisant :
        return -1
    else :
        if joueur_maximisant:
            max_eval = 1
            for action in actions_possibles(etat):
                new_etat = execute_action(action, etat)
                eval = minmax(new_etat, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = -1
            for action in actions_possibles(etat):
                new_etat = execute_action(action, etat)
                eval = minmax(new_etat, True)
                min_eval = min(min_eval, eval)
            return min_eval


def coup_minmax(etat):
    """
    entrée : un plateau 'etat'
    effet : donne le meilleur coup pour ce plateau
    sortie : un coup sous forme (o, x, y)
    """
    etat_initial = etat  # état initial du jeu
    best_action = None
    best_eval = -1

    for action in actions_possibles(etat_initial):
        new_etat = execute_action(action, etat_initial)
        eval = minmax(new_etat, False)

        if eval > best_eval:
            best_eval = eval
            best_action = action
    if best_action is None :
        return False
    else :
        return best_action[0]


# la boucle de jeu
# fonction clic :
def clic_arete(plateau, coord, bouton):
    """
    entrée :
        plateau sous forme [H, V, C],
        les coordonnées du clic sous forme [x, y],
        le bouton avec lequel on effectue le clic
    effet :
        si les coordonnées sont correctes :
            modifie le plateau,
            dessine une arête à l'endroit cliqué, de la couleur associée au bouton
        sinon : ne fais rien
    sortie : ()
    """
    [dim_x, dim_y] = dim(plateau)
    if bouton == 1 :
        couleur = color_1
    else :
        couleur = color_2

    if width / (dim_x + 1) < height / (dim_y + 1) :
        interval = width / (dim_x + 1)
    else :
        interval = height / (dim_y + 1)

    if dim_x < dim_y :
        debuty = interval
        debutx = width / dim_x
    elif dim_y < dim_x :
        debutx = interval
        debuty = height / dim_y
    else :
        debutx = interval
        debuty = interval

    testh = 0

    for i in range(dim_x):
        if (coord[0] >= debutx + 0.25 * interval + i * interval):
            if (coord[0] <= debutx + 0.25 * interval + (i + 0.5) * interval):
                testh = testh + 1
                arete_abscisse = i
    for j in range(dim_y):
        if (coord[1] >= debuty - 0.25 * interval + j * interval):
            if (coord[1] <= debuty - 0.25 * interval + (j + 0.5) * interval):
                testh = testh + 1
                arete_ordonee = j

    if testh == 2:
        if arete_abscisse <= dim_x - 2 :
            if plateau[0][arete_abscisse][arete_ordonee] == 0  :
                draw_arete(False, plateau, 0, arete_abscisse, arete_ordonee, couleur)
                plateau[0][arete_abscisse][arete_ordonee] = 1
                if not carre(plateau, couleur) :
                    Turn[0] = (Turn[0] + 1) % 2

    testv = 0

    for i in range(dim_x):
        if (coord[0] >= debutx - 0.25 * interval + i * interval):
            if (coord[0] <= debutx - 0.25 * interval + (i + 0.5) * interval) :
                testv = testv + 1
                arete_abscisse_v = i

    for j in range(dim_y):
        if coord[1] >= debuty + 0.25 * interval + j * interval:
            if coord[1] <= debuty + 0.25 * interval + (j + 0.5) * interval :
                testv = testv + 1
                arete_ordonee_v = j

    if testv == 2:
        if arete_ordonee_v <= dim_y - 2 :
            if plateau[1][arete_abscisse_v][arete_ordonee_v] == 0  :
                draw_arete(False, plateau, 1, arete_abscisse_v, arete_ordonee_v,
                           couleur)
                plateau[1][arete_abscisse_v][arete_ordonee_v] = 1
                if not carre(plateau, couleur) :
                    Turn[0] = (Turn[0] + 1) % 2

    display.flip()


# couleur de base :
color_fond = C1_BLUE
color_1 = bgColor  # couleur du J1
color_2 = BLEU_FONCE  # couleur du J2

display.set_caption('Modélisation affrontement candidats')

display.update()

initialise_menu(screen, color_fond)

# variables globales
run = True
joue = False
pvp = False
pvr = False
rvr = False
robot_activation = False
dimension = [0, 0]
nb_colonne = dimension[0] - 1
nb_ligne = dimension[1] - 1
choix_x = 0
choix_y = 0
mode_pvp = False
mode_pvr = False
mode_rvr = False
menu_color = False
num_robot1, num_robot2 = -1, -1
choix_color_fond, choix_color_1, choix_color_2 = -1, -1, -1
pause = False
tour_num = 0
clignote = False

if not run:
    logging.error("Impossible de lancer le jeu")

logging.info("Début de l'exécution de la boucle de jeu")
while run:
    # boucle de menu :
    for pyEvent in event.get():
        if pyEvent.type == MOUSEMOTION:
            bouton_main_menu(screen, pyEvent.pos, color_fond)
        if pyEvent.type == MOUSEBUTTONDOWN:
            choix = clic_bouton(pyEvent.pos)
            if choix != 0 :
                if choix == 1:
                    pvp = True
                    dimension_menu(screen, color_fond)
                elif choix == 2 :
                    pvr = True
                    clignote = True
                    menu_robot(screen, color_2, color_fond)
                elif choix == 3 :
                    rvr = True
                    menu_robots_battle(screen, color_1, color_2, color_fond)
                elif choix == 4:
                    menu_color = True
                    menu_couleur(screen, color_fond)
        if pyEvent.type == QUIT:
            run = False
            joue = False

    # boucles de choix :
    logging.debug("Début de l'exécution de la boucle de choix")
    while pvp :
        for pyEvent in event.get():
            if pyEvent.type == QUIT:
                pvp = False
                run = False
                joue = False
            if pyEvent.type == KEYDOWN and pyEvent.key == K_m :
                initialise_menu(screen, color_fond)
                pvp = False
            if pyEvent.type == MOUSEMOTION:
                bouton_dimension_menu(screen, pyEvent.pos, choix_x, choix_y,
                                      color_fond)
            if pyEvent.type == MOUSEBUTTONDOWN:
                (choix_x, choix_y) = clic_bouton_dimension(pyEvent.pos, choix_x,
                                                           choix_y)
                if choix_x != 0 and choix_y != 0 :
                    pvp = False
                    plateau = reset(color_fond, choix_x + 1, choix_y + 1)
                    dimension = [choix_x + 1, choix_y + 1]
                    choix_x, choix_y = 0, 0
                    joue = True
                    mode_pvp = True
        display.flip()

    logging.info("Début de l'exécution de la boucle de choix")
    while pvr :
        for pyEvent in event.get():
            if pyEvent.type == QUIT:
                pvr = False
                run = False
                joue = False
            if pyEvent.type == KEYDOWN and pyEvent.key == K_m :
                initialise_menu(screen, color_fond)
                pvr = False
                clignote = False
            if pyEvent.type == MOUSEMOTION:
                bouton_menu_robots(screen, pyEvent.pos, color_fond)
            if pyEvent.type == MOUSEBUTTONDOWN:
                num_robot = clic_bouton_robot(pyEvent.pos)
                if num_robot != -1 :
                    dimension_boucle = True
                    dimension_menu(screen, color_fond)
                    display.flip()

                    # boucle de dimension
                    logging.info(
                        "Début de l'exécution de la boucle de choix des dimensions")
                    while dimension_boucle :
                        for pyEvent in event.get():
                            if pyEvent.type == QUIT:
                                dimension_boucle = False
                                pvr = False
                                run = False
                                joue = False
                            if pyEvent.type == KEYDOWN and pyEvent.key == K_m :
                                initialise_menu(screen, color_fond)
                                dimension_boucle = False
                                pvr = False
                                clignote = False
                            if pyEvent.type == MOUSEMOTION:
                                bouton_dimension_menu(screen, pyEvent.pos,
                                                      choix_x, choix_y, color_fond)
                            if pyEvent.type == MOUSEBUTTONDOWN:
                                (choix_x, choix_y) = clic_bouton_dimension(
                                    pyEvent.pos, choix_x, choix_y)
                                if choix_x != 0 and choix_y != 0 :
                                    dimension_boucle = False
                                    pvr = False
                                    plateau = reset(color_fond, choix_x + 1,
                                                    choix_y + 1)
                                    dimension = [choix_x + 1, choix_y + 1]
                                    choix_x, choix_y = 0, 0
                                    joue = True
                                    mode_pvr = True
                        display.flip()
        display.flip()

    logging.info("Début de l'exécution de la boucle de choix")
    while rvr :
        for pyEvent in event.get():
            if pyEvent.type == QUIT:
                rvr = False
                run = False
                joue = False
            if pyEvent.type == KEYDOWN and pyEvent.key == K_m :
                initialise_menu(screen, color_fond)
                rvr = False
            if pyEvent.type == MOUSEMOTION:
                bouton_robots_battle(
                    screen, pyEvent.pos, num_robot1, num_robot2, color_fond)
            if pyEvent.type == MOUSEBUTTONDOWN:
                (num_robot1, num_robot2) = clic_robots_battle(
                    screen, pyEvent.pos, num_robot1, num_robot2)
                if num_robot1 != -1 and num_robot2 != -1 :
                    dimension_boucle = True
                    clignote = False
                    dimension_menu(screen, color_fond)
                    display.flip()

                    # boucle de dimension
                    logging.info(
                        "Début de l'exécution de la boucle de choix des dimensions")
                    while dimension_boucle :
                        for pyEvent in event.get():
                            if pyEvent.type == QUIT:
                                dimension_boucle = False
                                rvr = False
                                run = False
                                joue = False
                            if pyEvent.type == KEYDOWN and pyEvent.key == K_m :
                                initialise_menu(screen, color_fond)
                                dimension_boucle = False
                                rvr = False
                                logging.warning(
                                    "L'utilisateur n'a pas sélectionné de dimension",
                                    "il revient au menu")
                            if pyEvent.type == MOUSEMOTION:
                                bouton_dimension_menu(
                                    screen, pyEvent.pos, choix_x, choix_y, color_fond)
                            if pyEvent.type == MOUSEBUTTONDOWN:
                                (choix_x, choix_y) = clic_bouton_dimension(
                                    pyEvent.pos, choix_x, choix_y)
                                if choix_x != 0 and choix_y != 0 :
                                    dimension_boucle = False
                                    rvr = False
                                    plateau = reset(
                                        color_fond, choix_x + 1, choix_y + 1)
                                    dimension = [choix_x + 1, choix_y + 1]
                                    choix_x, choix_y = 0, 0
                                    joue = True
                                    mode_rvr = True
                        display.flip()
        display.flip()

    logging.info("Début de l'exécution de la boucle de choix des couleurs")
    while menu_color :
        for pyEvent in event.get():
            if pyEvent.type == QUIT:
                menu_color = False
                run = False
                joue = False
            if pyEvent.type == KEYDOWN and pyEvent.key == K_m :
                initialise_menu(screen, color_fond)
                menu_color = False
                logging.warning(
                    "L'utilisateur n'a pas sélectionné de couleur",
                    "la couleur par défaut sera utilisée.")
            if pyEvent.type == MOUSEMOTION:
                bouton_menu_couleur(screen, pyEvent.pos, color_fond, choix_color_1)
            if pyEvent.type == MOUSEBUTTONDOWN:
                (choix_color_fond, choix_color_1, choix_color_2) = clic_menu_couleur(
                    pyEvent.pos, choix_color_1, choix_color_2)
                if choix_color_1 != -1:
                    if choix_color_2 != -1 or choix_color_fond != -1  :
                        menu_color = False
                        (color_fond, color_1, color_2) = attribue_color(
                            color_fond, color_1, color_2, choix_color_fond,
                            choix_color_1, choix_color_2)
                        choix_color_fond, choix_color_1, choix_color_2 = -1, -1, -1
                        initialise_menu(screen, color_fond)
        display.flip()

    # boucle de partie :
    logging.info("Début de l'exécution de la boucle de la partie")
    while joue :
        if mode_pvp :
            for pyEvent in event.get():
                if pyEvent.type == QUIT:
                    run = False
                    joue = False
                if pyEvent.type == KEYDOWN and pyEvent.key == K_r :
                    plateau = reset(color_fond, dimension[0], dimension[1])
                    Turn[0] = 0
                if pyEvent.type == MOUSEBUTTONDOWN:
                    clic_arete(plateau, pyEvent.pos, pyEvent.button)

                if pyEvent.type == KEYDOWN and pyEvent.key == K_m :
                    initialise_menu(screen, color_fond)
                    joue = False
                    mode_pvp = False

        if mode_pvr :
            for pyEvent in event.get():
                if pyEvent.type == QUIT:
                    run = False
                    joue = False
                if pyEvent.type == MOUSEBUTTONDOWN:
                    clic_arete(plateau, pyEvent.pos, pyEvent.button)
                    while Turn[0] == 1 and not pause:
                        if num_robot == 0 :
                            robot0(clignote, plateau, color_2)
                        if num_robot == 1 :
                            robot1(clignote, plateau, color_2)
                        if num_robot == 2:
                            algo1(clignote, plateau, color_2)
                        if num_robot == 3:
                            algo2(clignote, plateau, color_2)
                        if num_robot == 4 :
                            algo3(clignote, plateau, color_2)
                        if num_robot == 5:
                            algo4(clignote, plateau, color_2)
                    # (avancement, tour_num) = coup(2, avancement, tour_num, plateau)
                if pyEvent.type == KEYDOWN and pyEvent.key == K_p :
                    pause = not pause

                if pyEvent.type == KEYDOWN and pyEvent.key == K_r :
                    plateau = reset(color_fond, dimension[0], dimension[1])
                    Turn[0] = 0
                if pyEvent.type == KEYDOWN and pyEvent.key == K_m :
                    Turn[0] = 0
                    initialise_menu(screen, color_fond)
                    joue = False
                    mode_pvr = False
                    num_robot = -1

        if mode_rvr :
            for pyEvent in event.get():
                if pyEvent.type == QUIT:
                    run = False
                    joue = False
                if pyEvent.type == KEYDOWN and pyEvent.key == K_m :
                    initialise_menu(screen, color_fond)
                    joue = False
                    Turn[0] = 0
                    mode_pvp, mode_pvr, mode_rvr = False, False, False
                    num_robot1, num_robot2 = -1, -1
                if pyEvent.type == KEYDOWN and pyEvent.key == K_r :
                    plateau = reset(color_fond, dimension[0], dimension[1])
                    Turn[0] = 0
                if pyEvent.type == KEYDOWN and pyEvent.key == K_p :
                    pause = not pause
                if pyEvent.type == MOUSEBUTTONDOWN:
                    clic_arete(plateau, pyEvent.pos, pyEvent.button)

            if nb_cases_vide(plateau) > 0 :
                while Turn[0] == 1 and nb_cases_vide(plateau) > 0 and not pause:
                    if num_robot1 == 0 :
                        robot0(clignote, plateau, color_1)
                    if num_robot1 == 1 :
                        robot1(clignote, plateau, color_1)
                    if num_robot1 == 2:
                        algo1(clignote, plateau, color_1)
                    if num_robot1 == 3:
                        algo2(clignote, plateau, color_1)
                    if num_robot1 == 4 :
                        algo3(clignote, plateau, color_1)
                    if num_robot1 == 5:
                        algo4(clignote, plateau, color_1)
                while Turn[0] != 1 and nb_cases_vide(plateau) > 0 and not pause :
                    if num_robot2 == 0 :
                        robot0(clignote, plateau, color_2)
                    if num_robot2 == 1 :
                        robot1(clignote, plateau, color_2)
                    if num_robot2 == 2:
                        algo1(clignote, plateau, color_2)
                    if num_robot2 == 3:
                        algo2(clignote, plateau, color_2)
                    if num_robot2 == 4 :
                        algo3(clignote, plateau, color_2)
                    if num_robot2 == 5:
                        algo4(clignote, plateau, color_2)
        display.flip()
    display.flip()


quit()
