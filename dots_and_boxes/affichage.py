"""
Sommaire des fonctions d'affichage :
    - définition des couleurs
    - définition de l'écran
    - le_plateau(dim_x, dim_y)
    - reset(color, dim_x, dim_y)
    - draw_arete(clignote, plateau, orientation, abscisse, ordonnee, couleur)
    - draw_carre(plateau, abscisse, ordonnee, couleur)
    - interaction avec le menu principal :
        . initialise_menu(screen, color)
        . bouton_main_menu(screen, coord, color_fond)
        . clic_bouton(coord)
    - interaction avec le menu des dimension :
        . dimension_menu(screen, color_fond)
        . bouton_dimension_menu(screen, coord, choix_x, choix_y, color_fond)
        . clic_bouton_dimension(coord, choix_x, choix_y)
    - interaction avec le menu des robots en pvr:
        . menu_robot(screen, color, color_fond)
        . bouton_menu_robots(screen, coord, color_fond)
        . clic_bouton_robot(coord)
    - interaction avec le menu des robots en rvr :
        . menu_robots_battle(screen, color_1, color_2, color_fond)
        . bouton_robots_battle(screen, coord, num_robot1, num_robot2, color_fond)
        . clic_robots_battle(screen, coord, num_robot1, num_robot2)
    - interaction avec le menu des couleurs :
        . menu_couleur(screen, color_fond)
        . bouton_menu_couleur(screen, coord, color_fond, choix_color_1)
        . clic_menu_couleur(coord, num_color_1, num_color_2)
        . attribue_color(
            color_fond,
            color_1,
            color_2,
            num_color_fond,
            num_color_1,
            num_color_2
        )
"""

from time import sleep

from logger import logger
from pygame import display, draw, font

# couleurs

BLACK = (0, 0, 0)
GRAY = (150, 127, 127)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)  # Bleu très clair
MAGENTA = (255, 0, 255)  # Violet pétant

PINK = (255, 0, 128)  # Rose
PINK2 = (255, 20, 147)  # Rose fluo
PINK3 = (255, 192, 203)

C1_GREEN = (204, 255, 204)  # Vert très clair
C1_BLUE = (153, 204, 255)  # Bleu ciel -> couleur de l'écran
bgColor = (127, 127, 255)  # Bleu sympa

VERT = (0, 200, 0)
JAUNE = YELLOW
ORANGE = (255, 130, 0)
ROUGE = RED
MARRON = (110, 42, 42)
NOIR = BLACK

CYAN = CYAN
ROSE_CLAIR = (255, 182, 193)
ROSE_FONCE = PINK
VIOLET_FONCE = (148, 0, 211)
BLEU = BLUE
BLEU_FONCE = (0, 0, 150)
GRIS_CLAIR = (200, 200, 200)
VERT_CLAIR = (150, 255, 150)

SAUGE_LOANN = (146, 166, 157)
ROSE_POUDREE = (204, 153, 159)
BLEU_JOLI = (169, 184, 204)


# définition de l'écran

size = width, height = 600, 600
screen = display.set_mode(size)

# affichage du menu :


def dim(plateau):
    """
    entrée : un plateau sous forme [H, V, C]
    effet : renvoie les dimensions du plateau
    sortie : tableau [dim_x, dim_y]
    """
    if plateau is None:
        logger.critical("Échec du démarrage du jeu, vérifiez la configuration.")
    return [len(plateau[1]), len(plateau[0][0])]


def le_plateau(dim_x, dim_y):
    """
    entrée : deux dimensions entières : dim_x, dim_y
    effet : affiche un plateau vide de dimension dim_x * dim_y
            et met les compteurs de point à 0
    sortie : ()
    """
    radius = 5
    if width / (dim_x + 1) < height / (dim_y + 1):
        interval = width / (dim_x + 1)
    else:
        interval = height / (dim_y + 1)

    if dim_x < dim_y:
        debuty = interval
        debutx = width / dim_x
    elif dim_y < dim_x:
        debutx = interval
        debuty = height / dim_y
    else:
        debutx = interval
        debuty = interval

    for i in range(dim_x):
        for j in range(dim_y):
            coordo = (debutx + i * interval, debuty + j * interval)
            draw.circle(screen, WHITE, coordo, radius, 0)


def reset(color, dim_x, dim_y):
    """
    entrée : une couleur de fond, la dimension du plateau
    effet : affiche à l'écran un plateau vide, et crée un tableau [H, V, C] rempli de 0
    sortie : un tableau [H, V, C]
    """
    # ensemble arêtes horizontales
    h = [[0 for _ in range(dim_y)] for _ in range(dim_x - 1)]

    # ensemble arêtes verticales
    v = [[0 for _ in range(dim_y - 1)] for _ in range(dim_x)]

    # ensemble cases
    c = [[0 for _ in range(dim_y - 1)] for _ in range(dim_x - 1)]

    screen.fill(color)

    le_plateau(dim_x, dim_y)

    display.flip()

    return [h, v, c]


def draw_arete(clignote, plateau, orientation, abscisse, ordonnee, couleur):
    """
    entrée :
        un booléen "clignote",
        un plateau sous forme [H, V, C],
        3 entiers o, x, y
        une couleur
    effet :
        dessine une arête de couleur 'couleur'
        et de coordonnées ('orientation','abcisse','ordonnee')
    sortie : ()
    """
    dim_x, dim_y = dim(plateau)

    if width / (dim_x + 1) < height / (dim_y + 1):
        interval = width / (dim_x + 1)
    else:
        interval = height / (dim_y + 1)

    if dim_x < dim_y:
        debuty = interval
        debutx = width / dim_x
    elif dim_y < dim_x:
        debutx = interval
        debuty = height / dim_y
    else:
        debutx = interval
        debuty = interval
    i = abscisse
    j = ordonnee
    if orientation == 0:  # arrête horizontale :
        draw.line(
            screen,
            couleur,
            (debutx + i * interval, debuty + j * interval),
            (debutx + (i + 1) * interval, debuty + j * interval),
            5,
        )
        if clignote:
            display.flip()
            for _ in range(3):
                sleep(0.1)
                draw.line(
                    screen,
                    WHITE,
                    (debutx + i * interval, debuty + j * interval),
                    (debutx + (i + 1) * interval, debuty + j * interval),
                    5,
                )
                display.flip()
                sleep(0.1)
                draw.line(
                    screen,
                    couleur,
                    (debutx + i * interval, debuty + j * interval),
                    (debutx + (i + 1) * interval, debuty + j * interval),
                    5,
                )
                display.flip()

    else:  # arrête verticale :
        draw.line(
            screen,
            couleur,
            (debutx + i * interval, debuty + j * interval),
            (debutx + i * interval, debuty + (j + 1) * interval),
            5,
        )
        if clignote:
            display.flip()
            for _ in range(3):
                sleep(0.1)
                draw.line(
                    screen,
                    WHITE,
                    (debutx + i * interval, debuty + j * interval),
                    (debutx + i * interval, debuty + (j + 1) * interval),
                    5,
                )
                display.flip()
                sleep(0.1)
                draw.line(
                    screen,
                    couleur,
                    (debutx + i * interval, debuty + j * interval),
                    (debutx + i * interval, debuty + (j + 1) * interval),
                    5,
                )
                display.flip()


def draw_carre(plateau, abscisse, ordonnee, couleur):
    """
    entrée : un plateau sous forme [H, V, C], 2 entiers x, y et une couleur
    effet : dessine une arête de couleur 'couleur'
    et de coordonnées ('orientation','abcisse','ordonnee')
            compte un point pour chaque case colorié au joueur de la couleur 'c'.
    sortie : ()
    """
    dim_x, dim_y = dim(plateau)

    if width / (dim_x + 1) < height / (dim_y + 1):
        interval = width / (dim_x + 1)
    else:
        interval = height / (dim_y + 1)

    if dim_x < dim_y:
        debuty = interval
        debutx = width / dim_x
    elif dim_y < dim_x:
        debutx = interval
        debuty = height / dim_y
    else:
        debutx = interval
        debuty = interval
    i = abscisse
    j = ordonnee
    draw.rect(
        screen,
        couleur,
        [debutx + i * interval, debuty + j * interval, interval, interval],
        0,
    )

    # if couleur == color_1 :
    #    points_j1 = points_j1  + 1
    # else :
    #    points_j2 = points_j2 + 1


# affiche et interagit avec l'interface main menu :
def initialise_menu(screen, color):
    """
    entrée : l'écran
    effet : affiche le menu principal, avec un fond de couleur 'color'
    sortie : ()
    """
    # Définition de la police et de la taille du texte
    police = font.Font(None, 30)

    # Définition du texte à afficher
    question1 = "Quel mode de jeux"
    question1_suite = "voulez-vous ?"
    pvp_texte = "Joueur VS joueur"
    pvr_texte = "Joueur VS  robot"
    rvr_texte = "Combat de robots"
    color_texte = "modification des couleurs"

    # Rendu du texte avec la police choisie
    question1_rendu = police.render(question1, True, (255, 255, 255))
    question1_suite_rendu = police.render(question1_suite, True, (255, 255, 255))
    pvp_texte_rendu = police.render(pvp_texte, True, (255, 255, 255))
    pvr_texte_rendu = police.render(pvr_texte, True, (255, 255, 255))
    rvr_texte_rendu = police.render(rvr_texte, True, (255, 255, 255))
    color_texte_rendu = police.render(color_texte, True, (255, 255, 255))

    # Positionnement du texte sur la fenêtre
    position_question1 = question1_rendu.get_rect(center=(300, 100))
    position_question1_suite = question1_suite_rendu.get_rect(center=(300, 130))
    position_pvp_text = pvp_texte_rendu.get_rect(center=(200, 250))
    position_pvr_text = pvr_texte_rendu.get_rect(center=(200, 350))
    position_rvr_text = rvr_texte_rendu.get_rect(center=(200, 450))
    position_color_text = color_texte_rendu.get_rect(center=(350, 550))

    # affichage
    screen.fill(color)
    screen.blit(question1_rendu, position_question1)  # texte début de question
    screen.blit(
        question1_suite_rendu, position_question1_suite
    )  # texte fin de question
    screen.blit(pvp_texte_rendu, position_pvp_text)  # texte pvp
    screen.blit(pvr_texte_rendu, position_pvr_text)  # texte pvr
    screen.blit(rvr_texte_rendu, position_rvr_text)  # texte rvr
    screen.blit(color_texte_rendu, position_color_text)  # texte color
    draw.circle(screen, WHITE, [400, 250], 10, 2)  # bouton pvp
    draw.circle(screen, WHITE, [400, 350], 10, 2)  # bouton pvr
    draw.circle(screen, WHITE, [400, 450], 10, 2)  # bouton rvr
    draw.circle(screen, WHITE, [150, 550], 10, 2)  # bouton color


def bouton_main_menu(screen, coord, color_fond):
    """
    entrée : l'écran, une coordonée [x, y]
    effet : colorie un bouton du menu principal si la coordonée lui correspond
    sortie : ()
    """
    ecart = 6
    if coord[0] <= 400 + ecart and coord[0] >= 400 - ecart:
        if coord[1] <= 250 + ecart and coord[1] >= 250 - ecart:
            draw.circle(screen, WHITE, [400, 250], 8)  # bouton pvp
        elif coord[1] <= 350 + ecart and coord[1] >= 350 - ecart:
            draw.circle(screen, WHITE, [400, 350], 8)  # bouton pvr
        elif coord[1] <= 450 + ecart and coord[1] >= 450 - ecart:
            draw.circle(screen, WHITE, [400, 450], 8)  # bouton rvr
        else:
            draw.circle(screen, color_fond, [400, 250], 8)  # bouton pvp
            draw.circle(screen, color_fond, [400, 350], 8)  # bouton pvr
            draw.circle(screen, color_fond, [400, 450], 8)  # bouton rvr
            draw.circle(screen, color_fond, [150, 550], 8)  # bouton color
    elif (
        coord[0] <= 150 + ecart
        and coord[0] >= 150 - ecart
        and coord[1] <= 550 + ecart
        and coord[1] >= 550 - ecart
    ):
        draw.circle(screen, WHITE, [150, 550], 8)  # bouton color
    else:
        draw.circle(screen, color_fond, [400, 250], 8)  # bouton pvp
        draw.circle(screen, color_fond, [400, 350], 8)  # bouton pvr
        draw.circle(screen, color_fond, [400, 450], 8)  # bouton rvr
        draw.circle(screen, color_fond, [150, 550], 8)  # bouton color


def clic_bouton(coord):
    """
    entrée : l'écran, une coordonée [x, y]
    effet : retourne le bouton du menu principal selectionné (1, 2 ou 3),
      et 0 si aucun bouton n'est selectionné
    sortie : un entier entre 0 et 3 compris
    """
    ecart = 6
    if coord[0] <= 400 + ecart and coord[0] >= 400 - ecart:
        if coord[1] <= 250 + ecart and coord[1] >= 250 - ecart:
            return 1
        elif coord[1] <= 350 + ecart and coord[1] >= 350 - ecart:
            return 2
        elif coord[1] <= 450 + ecart and coord[1] >= 450 - ecart:
            return 3
    elif (
        coord[0] <= 150 + ecart
        and coord[0] >= 150 - ecart
        and coord[1] <= 550 + ecart
        and coord[1] >= 550 - ecart
    ):
        return 4
    else:
        return 0


# affiche et interagit avec l'interface de choix de dimension
def dimension_menu(screen, color_fond):
    """
    entrée : l'écran
    effet : affiche le menu de choix de dimension
    sortie : ()
    """
    # Définition de la police et de la taille du texte
    police = font.Font(None, 30)

    # Définition du texte à afficher
    question = "Quelles dimensions voulez-vous ?"
    dimension_x = "Nombre de colonnes"
    dimension_y = "Nombre de lignes"
    x2, x3, x4, x5 = "2", "3", "4", "5"
    x6, x7, x8, x9, x10 = "6", "7", "8", "9", "10"
    (
        y2,
        y3,
        y4,
        y5,
    ) = (
        "2",
        "3",
        "4",
        "5",
    )
    y6, y7, y8, y9, y10 = "6", "7", "8", "9", "10"

    # Rendu du texte avec la police choisie
    question_rendu = police.render(question, True, (255, 255, 255))
    dimension_x_rendu = police.render(dimension_x, True, (255, 255, 255))
    dimension_y_rendu = police.render(dimension_y, True, (255, 255, 255))
    x2_rendu = police.render(x2, True, (255, 255, 255))
    x3_rendu = police.render(x3, True, (255, 255, 255))
    x4_rendu = police.render(x4, True, (255, 255, 255))
    x5_rendu = police.render(x5, True, (255, 255, 255))
    x6_rendu = police.render(x6, True, (255, 255, 255))
    x7_rendu = police.render(x7, True, (255, 255, 255))
    x8_rendu = police.render(x8, True, (255, 255, 255))
    x9_rendu = police.render(x9, True, (255, 255, 255))
    x10_rendu = police.render(x10, True, (255, 255, 255))
    y2_rendu = police.render(y2, True, (255, 255, 255))
    y3_rendu = police.render(y3, True, (255, 255, 255))
    y4_rendu = police.render(y4, True, (255, 255, 255))
    y5_rendu = police.render(y5, True, (255, 255, 255))
    y6_rendu = police.render(y6, True, (255, 255, 255))
    y7_rendu = police.render(y7, True, (255, 255, 255))
    y8_rendu = police.render(y8, True, (255, 255, 255))
    y9_rendu = police.render(y9, True, (255, 255, 255))
    y10_rendu = police.render(y10, True, (255, 255, 255))

    # Positionnement du texte sur la fenêtre
    position_question = question_rendu.get_rect(center=(300, 75))
    position_dimension_x = dimension_x_rendu.get_rect(center=(150, 150))
    position_dimension_y = dimension_y_rendu.get_rect(center=(450, 150))
    position_x2 = x2_rendu.get_rect(center=(100, 200))
    position_x3 = x3_rendu.get_rect(center=(100, 240))
    position_x4 = x4_rendu.get_rect(center=(100, 280))
    position_x5 = x5_rendu.get_rect(center=(100, 320))
    position_x6 = x6_rendu.get_rect(center=(100, 360))
    position_x7 = x7_rendu.get_rect(center=(100, 400))
    position_x8 = x8_rendu.get_rect(center=(100, 440))
    position_x9 = x9_rendu.get_rect(center=(100, 480))
    position_x10 = x10_rendu.get_rect(center=(100, 520))
    position_y2 = y2_rendu.get_rect(center=(400, 200))
    position_y3 = y3_rendu.get_rect(center=(400, 240))
    position_y4 = y4_rendu.get_rect(center=(400, 280))
    position_y5 = y5_rendu.get_rect(center=(400, 320))
    position_y6 = y6_rendu.get_rect(center=(400, 360))
    position_y7 = y7_rendu.get_rect(center=(400, 400))
    position_y8 = y8_rendu.get_rect(center=(400, 440))
    position_y9 = y9_rendu.get_rect(center=(400, 480))
    position_y10 = y10_rendu.get_rect(center=(400, 520))

    # affichage
    screen.fill(color_fond)
    screen.blit(question_rendu, position_question)  # texte début de question
    screen.blit(dimension_x_rendu, position_dimension_x)  # texte pour les colonnes
    screen.blit(dimension_y_rendu, position_dimension_y)  # texte pour les lignes

    screen.blit(x2_rendu, position_x2)
    screen.blit(x3_rendu, position_x3)
    screen.blit(x4_rendu, position_x4)
    screen.blit(x5_rendu, position_x5)
    screen.blit(x6_rendu, position_x6)
    screen.blit(x7_rendu, position_x7)
    screen.blit(x8_rendu, position_x8)
    screen.blit(x9_rendu, position_x9)
    screen.blit(x10_rendu, position_x10)

    screen.blit(y2_rendu, position_y2)
    screen.blit(y3_rendu, position_y3)
    screen.blit(y4_rendu, position_y4)
    screen.blit(y5_rendu, position_y5)
    screen.blit(y6_rendu, position_y6)
    screen.blit(y7_rendu, position_y7)
    screen.blit(y8_rendu, position_y8)
    screen.blit(y9_rendu, position_y9)
    screen.blit(y10_rendu, position_y10)

    for i in range(9):
        draw.circle(screen, WHITE, [200, 200 + 40 * i], 8, 2)  # bouton x(i + 2)
        draw.circle(screen, WHITE, [500, 200 + 40 * i], 8, 2)  # bouton y(i  + 2)


def bouton_dimension_menu(screen, coord, choix_x, choix_y, color_fond):
    """
    entrée : l'écran, une coordonée [x, y],
    deux entiers correspondant au choix actuels des dimensions
    effet : colorie un bouton du menu_dimension si la coordonée lui correspond
    sortie : ()
    """
    test = False
    for i in range(9):
        if (coord[0] <= 200 + 6) and (coord[0] >= 200 - 6):
            if (coord[1] <= 200 + 40 * i + 6) and (coord[1] >= 200 + 40 * i - 6):
                draw.circle(screen, WHITE, [200, 200 + 40 * i], 6)  # bouton x(i + 2)
                test = True
        if coord[0] <= 500 + 6 and coord[0] >= 500 - 6:
            if coord[1] <= 200 + 40 * i + 6 and coord[1] >= 200 + 40 * i - 6:
                draw.circle(screen, WHITE, [500, 200 + 40 * i], 6)  # bouton y(i + 2)
                test = True
    if not test:
        for i in range(9):
            if i + 2 != choix_x:
                draw.circle(
                    screen, color_fond, [200, 200 + 40 * i], 6
                )  # bouton x(i + 2)
            if i + 2 != choix_y:
                draw.circle(
                    screen, color_fond, [500, 200 + 40 * i], 6
                )  # bouton y(i + 2)


def clic_bouton_dimension(coord, choix_x, choix_y):
    """
    entrée : une coordonée [x, y], deux entiers correspondants aux choix actuels
    effet : retourne la modification des boutons du menu dimension selectionnés
    (entre 2 et 10)
    sortie : (choix_x, choix_y) modifiés
    """
    ecart = 10
    for i in range(9):
        if coord[1] <= 200 + 40 * i + ecart and coord[1] >= 200 + 40 * i - ecart:
            if coord[0] <= 200 + ecart and coord[0] >= 200 - ecart:
                choix_x = i + 2
        if coord[1] <= 200 + 40 * i + ecart and coord[1] >= 200 + 40 * i - ecart:
            if coord[0] <= 500 + ecart and coord[0] >= 500 - ecart:
                choix_y = i + 2
    return (choix_x, choix_y)


# affiche et interagit avec l'interface de choix de robot en mode pvr
def menu_robot(screen, color, color_fond):
    """
    entrée : l'écran, une couleur
    effet : affiche le menu de choix de niveau de robots,
    les écritures de la couleur 'color'
    sortie : ()
    """
    # Définition de la police et de la taille du texte
    police = font.Font(None, 30)

    # Définition du texte à afficher
    question = "Quel robot souhaitez-vous affronter ?"
    robot0 = "Robot niveau 0 "
    robot1 = "Robot niveau 1 "
    robot2 = "Robot niveau 2 "
    robot3 = "Robot niveau 3 "
    robot4 = "Robot niveau 4 "
    robot5 = "Robot niveau 5 "

    # Rendu du texte avec la police choisie
    question_rendu = police.render(question, True, (255, 255, 255))
    robot0_rendu = police.render(robot0, True, color)
    robot1_rendu = police.render(robot1, True, color)
    robot2_rendu = police.render(robot2, True, color)
    robot3_rendu = police.render(robot3, True, color)
    robot4_rendu = police.render(robot4, True, color)
    robot5_rendu = police.render(robot5, True, color)

    # Positionnement du texte sur la fenêtre
    position_question = question_rendu.get_rect(center=(300, 50))
    position_robot0 = robot0_rendu.get_rect(center=(200, 130))
    position_robot1 = robot1_rendu.get_rect(center=(200, 205))
    position_robot2 = robot2_rendu.get_rect(center=(200, 280))
    position_robot3 = robot3_rendu.get_rect(center=(200, 355))
    position_robot4 = robot4_rendu.get_rect(center=(200, 430))
    position_robot5 = robot5_rendu.get_rect(center=(200, 505))

    # affichage
    screen.fill(color_fond)
    screen.blit(question_rendu, position_question)  # texte début de question
    screen.blit(robot0_rendu, position_robot0)
    screen.blit(robot1_rendu, position_robot1)
    screen.blit(robot2_rendu, position_robot2)
    screen.blit(robot3_rendu, position_robot3)
    screen.blit(robot4_rendu, position_robot4)
    screen.blit(robot5_rendu, position_robot5)

    for i in range(6):
        draw.circle(screen, WHITE, [400, 130 + i * 75], 12, 2)  # bouton robot i


def bouton_menu_robots(screen, coord, color_fond):
    """
    entrée : l'écran, une coordonée [x, y],
    deux entiers correspondant au choix actuels des dimensions
    effet : colorie un bouton du menu_robots si la coordonée lui correspond
    sortie : ()
    """
    ecart = 7
    for i in range(6):
        if coord[0] <= 400 + ecart and coord[0] >= 400 - ecart:
            if coord[1] <= 130 + 75 * i + ecart and coord[1] >= 130 + 75 * i - ecart:
                draw.circle(screen, WHITE, [400, 130 + i * 75], 10)  # bouton robot i
        else:
            draw.circle(screen, color_fond, [400, 130 + i * 75], 10)  # bouton robot i


def clic_bouton_robot(coord):
    """
    entrée : une coordonée [x, y], deux entiers correspondants aux choix actuels
    effet : retourne le bouton du menu_robots selectionné (entre 1 et 5)
    , et 0 si aucun bouton n'est selectionné
    sortie : entier entre 1 et 5 compris
    """
    num = -1
    ecart = 10
    for i in range(6):
        if coord[0] <= 400 + ecart and coord[0] >= 400 - ecart:
            if coord[1] <= 130 + 75 * i + ecart and coord[1] >= 130 + 75 * i - ecart:
                num = i
    return num


# affiche et interagit avec l'interface de choix de robots en mode rvr
def menu_robots_battle(screen, color_1, color_2, color_fond):
    """
    entrée : l'écran, une couleur
    effet : affiche le menu de choix de niveau de robots,
    version bataille de robots, avec les écritures de la couleur 'color_1' et 'color_2'
    sortie : ()
    """
    # Définition de la police et de la taille du texte
    police = font.Font(None, 30)

    # Définition du texte à afficher
    question = "Quel robot affronte quel robot ?"
    robot0 = "Robot niveau 0 "
    robot1 = "Robot niveau 1 "
    robot2 = "Robot niveau 2 "
    robot3 = "Robot niveau 3 "
    robot4 = "Robot niveau 4 "
    robot5 = "Robot niveau 5 "

    # Rendu du texte avec la police choisie
    question_rendu = police.render(question, True, (255, 255, 255))
    robot0_rendu = police.render(robot0, True, color_1)
    robot1_rendu = police.render(robot1, True, color_1)
    robot2_rendu = police.render(robot2, True, color_1)
    robot3_rendu = police.render(robot3, True, color_1)
    robot4_rendu = police.render(robot4, True, color_1)
    robot5_rendu = police.render(robot5, True, color_1)
    robot0__rendu = police.render(robot0, True, color_2)
    robot1__rendu = police.render(robot1, True, color_2)
    robot2__rendu = police.render(robot2, True, color_2)
    robot3__rendu = police.render(robot3, True, color_2)
    robot4__rendu = police.render(robot4, True, color_2)
    robot5__rendu = police.render(robot5, True, color_2)

    # Positionnement du texte sur la fenêtre
    position_question = question_rendu.get_rect(center=(300, 50))
    position_robot01 = robot0_rendu.get_rect(center=(100, 130))
    position_robot11 = robot1_rendu.get_rect(center=(100, 205))
    position_robot21 = robot2_rendu.get_rect(center=(100, 280))
    position_robot31 = robot3_rendu.get_rect(center=(100, 355))
    position_robot41 = robot4_rendu.get_rect(center=(100, 430))
    position_robot51 = robot5_rendu.get_rect(center=(100, 505))
    position_robot02 = robot0__rendu.get_rect(center=(500, 130))
    position_robot12 = robot1__rendu.get_rect(center=(500, 205))
    position_robot22 = robot2__rendu.get_rect(center=(500, 280))
    position_robot32 = robot3__rendu.get_rect(center=(500, 355))
    position_robot42 = robot4__rendu.get_rect(center=(500, 430))
    position_robot52 = robot5__rendu.get_rect(center=(500, 505))

    # affichage
    screen.fill(color_fond)
    screen.blit(question_rendu, position_question)  # texte début de question

    screen.blit(robot0_rendu, position_robot01)
    screen.blit(robot1_rendu, position_robot11)
    screen.blit(robot2_rendu, position_robot21)
    screen.blit(robot3_rendu, position_robot31)
    screen.blit(robot4_rendu, position_robot41)
    screen.blit(robot5_rendu, position_robot51)

    screen.blit(robot0__rendu, position_robot02)
    screen.blit(robot1__rendu, position_robot12)
    screen.blit(robot2__rendu, position_robot22)
    screen.blit(robot3__rendu, position_robot32)
    screen.blit(robot4__rendu, position_robot42)
    screen.blit(robot5__rendu, position_robot52)

    for i in range(6):
        draw.circle(screen, WHITE, [250, 130 + i * 75], 12, 2)  # bouton robot i

    for i in range(6):
        draw.circle(screen, WHITE, [350, 130 + i * 75], 12, 2)  # bouton robot i


def bouton_robots_battle(screen, coord, num_robot1, num_robot2, color_fond):
    """
    entrée : l'écran, une coordonée [x, y], deux entiers correspondant au choix
    actuels des dimensions
    effet : colorie un bouton du menu_robots_battle si la coordonée lui correspond
    sortie : ()
    """
    ecart = 7
    for i in range(6):
        if coord[0] <= 250 + ecart and coord[0] >= 250 - ecart:
            if coord[1] <= 130 + 75 * i + ecart and coord[1] >= 130 + 75 * i - ecart:
                draw.circle(screen, WHITE, [250, 130 + i * 75], 10)  # bouton robot i
        elif i == num_robot1:
            draw.circle(screen, WHITE, [250, 130 + i * 75], 10)  # bouton robot i
        else:
            draw.circle(screen, color_fond, [250, 130 + i * 75], 10)  # bouton robot i

        if coord[0] <= 350 + ecart and coord[0] >= 350 - ecart:
            if coord[1] <= 130 + 75 * i + ecart and coord[1] >= 130 + 75 * i - ecart:
                draw.circle(screen, WHITE, [350, 130 + i * 75], 10)  # bouton robot i
            elif i == num_robot2:
                draw.circle(screen, WHITE, [350, 130 + i * 75], 10)  # bouton robot i
        else:
            draw.circle(screen, color_fond, [350, 130 + i * 75], 10)  # bouton robot i


def clic_robots_battle(screen, coord, num_robot1, num_robot2):
    """
    entrée : une coordonée [x, y], deux entiers correspondants aux choix actuels
    effet : retourne la modification des boutons du menu_robots_battle selectionnés
    (entre 2 et 10)
    sortie : (num_robot1, num_robot2) modifiés
    """
    ecart = 10
    for i in range(6):
        if coord[0] <= 250 + ecart and coord[0] >= 250 - ecart:
            if coord[1] <= 130 + 75 * i + ecart and coord[1] >= 130 + 75 * i - ecart:
                num_robot1 = i
        if coord[0] <= 350 + ecart and coord[0] >= 350 - ecart:
            if coord[1] <= 130 + 75 * i + ecart and coord[1] >= 130 + 75 * i - ecart:
                num_robot2 = i
    return (num_robot1, num_robot2)


# affiche et interagit avec l'interface de choix des couleurs
def menu_couleur(screen, color_fond):
    """
    entrée : l'écran, une couleur
    effet : affiche le menu de choix de couleurs,
    sortie : ()
    """
    # Définition de la police et de la taille du texte
    police = font.Font(None, 30)
    police2 = font.Font(None, 20)

    # Définition du texte à afficher
    question1 = "Quelle couleur de fond voulez-vous ?"
    question2 = "Quelle couleur pour le J1 et le J2"
    indication = "premier clic pour J1, second pour J2"

    # Rendu du texte avec la police choisie
    question1_rendu = police.render(question1, True, (255, 255, 255))
    question2_rendu = police.render(question2, True, (255, 255, 255))
    indication_rendu = police2.render(indication, True, (255, 255, 255))

    # Positionnement du texte sur la fenêtre
    position_question1 = question1_rendu.get_rect(center=(300, 50))
    position_question2 = question2_rendu.get_rect(center=(300, 200))
    position_indication = indication_rendu.get_rect(center=(300, 250))

    # affichage
    screen.fill(color_fond)
    screen.blit(question1_rendu, position_question1)  # texte début de question1
    screen.blit(question2_rendu, position_question2)  # texte début de question2
    screen.blit(indication_rendu, position_indication)  # texte d'indication

    nb_fonds = 5
    intervale = width / (nb_fonds + 2)
    coté_carré = 50

    # couleur fond
    draw.rect(
        screen, C1_BLUE, [intervale + coté_carré / 2, 100, coté_carré, coté_carré], 0
    )
    draw.rect(
        screen, PINK, [2 * intervale + coté_carré / 2, 100, coté_carré, coté_carré], 0
    )
    draw.rect(
        screen,
        GRIS_CLAIR,
        [3 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
        0,
    )
    draw.rect(
        screen,
        SAUGE_LOANN,
        [4 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
        0,
    )
    draw.rect(
        screen,
        ROSE_CLAIR,
        [5 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
        0,
    )

    if color_fond == C1_BLUE:
        draw.rect(
            screen, BLACK, [intervale + coté_carré / 2, 100, coté_carré, coté_carré], 2
        )
    elif color_fond == PINK:
        draw.rect(
            screen,
            BLACK,
            [2 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
            2,
        )
    elif color_fond == GRIS_CLAIR:
        draw.rect(
            screen,
            BLACK,
            [3 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
            2,
        )
    elif color_fond == SAUGE_LOANN:
        draw.rect(
            screen,
            BLACK,
            [4 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
            2,
        )
    elif color_fond == ROSE_CLAIR:
        draw.rect(
            screen,
            BLACK,
            [5 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
            2,
        )

    # couleur J1 :
    draw.rect(
        screen, VERT, [intervale + coté_carré / 2, 300, coté_carré, coté_carré], 0
    )
    draw.rect(
        screen,
        BLEU_JOLI,
        [2 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
        0,
    )
    draw.rect(
        screen, GRAY, [3 * intervale + coté_carré / 2, 300, coté_carré, coté_carré], 0
    )
    draw.rect(
        screen,
        bgColor,
        [4 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
        0,
    )
    draw.rect(
        screen, PINK2, [5 * intervale + coté_carré / 2, 300, coté_carré, coté_carré], 0
    )

    draw.rect(
        screen, ROSE_FONCE, [intervale + coté_carré / 2, 400, coté_carré, coté_carré], 0
    )
    draw.rect(
        screen,
        VIOLET_FONCE,
        [2 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
        0,
    )
    draw.rect(
        screen,
        ROSE_POUDREE,
        [3 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
        0,
    )
    draw.rect(
        screen, BLEU, [4 * intervale + coté_carré / 2, 400, coté_carré, coté_carré], 0
    )
    draw.rect(
        screen,
        BLEU_FONCE,
        [5 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
        0,
    )

    draw.rect(
        screen, JAUNE, [intervale + coté_carré / 2, 500, coté_carré, coté_carré], 0
    )
    draw.rect(
        screen, ORANGE, [2 * intervale + coté_carré / 2, 500, coté_carré, coté_carré], 0
    )
    draw.rect(
        screen, ROUGE, [3 * intervale + coté_carré / 2, 500, coté_carré, coté_carré], 0
    )
    draw.rect(
        screen, MARRON, [4 * intervale + coté_carré / 2, 500, coté_carré, coté_carré], 0
    )
    draw.rect(
        screen, BLACK, [5 * intervale + coté_carré / 2, 500, coté_carré, coté_carré], 0
    )


def bouton_menu_couleur(screen, coord, color_fond, choix_color_1):
    """
    entrée : l'écran, une coordonée [x, y],
    deux entiers correspondant au choix actuels des dimensions
    effet : colorie un bouton du menu_bouton si la coordonée lui correspond
    sortie : ()
    """
    nb_color_par_ligne = 5
    intervale = width / (nb_color_par_ligne + 2)
    coté_carré = 50
    ecart = 25
    num = 0
    num_col = -1

    if color_fond == C1_BLUE:
        num_color_fond = 1
    elif color_fond == PINK:
        num_color_fond = 2
    elif color_fond == GRIS_CLAIR:
        num_color_fond = 3
    elif color_fond == SAUGE_LOANN:
        num_color_fond = 4
    elif color_fond == ROSE_CLAIR:
        num_color_fond = 5

    if coord[1] <= 100 + coté_carré / 2 + ecart:
        if coord[1] >= 100 + coté_carré / 2 - ecart:
            for i in range(1, 6):
                if coord[0] <= i * intervale + coté_carré + ecart:
                    if coord[0] >= i * intervale + coté_carré - ecart:
                        draw.rect(
                            screen,
                            WHITE,
                            [
                                i * intervale + coté_carré / 2,
                                100,
                                coté_carré,
                                coté_carré,
                            ],
                            2,
                        )
                        num = i

        if num != 1:
            draw.rect(
                screen,
                C1_BLUE,
                [intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                0,
            )
        if num != 2:
            draw.rect(
                screen,
                PINK,
                [2 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                0,
            )
        if num != 3:
            draw.rect(
                screen,
                GRIS_CLAIR,
                [3 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                0,
            )
        if num != 4:
            draw.rect(
                screen,
                SAUGE_LOANN,
                [4 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                0,
            )
        if num != 5:
            draw.rect(
                screen,
                ROSE_CLAIR,
                [5 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                0,
            )
        if num != num_color_fond:
            if color_fond == C1_BLUE:
                draw.rect(
                    screen,
                    BLACK,
                    [intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                    2,
                )
            elif color_fond == PINK:
                draw.rect(
                    screen,
                    BLACK,
                    [2 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                    2,
                )
            elif color_fond == GRIS_CLAIR:
                draw.rect(
                    screen,
                    BLACK,
                    [3 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                    2,
                )
            elif color_fond == SAUGE_LOANN:
                draw.rect(
                    screen,
                    BLACK,
                    [4 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                    2,
                )
            elif color_fond == ROSE_CLAIR:
                draw.rect(
                    screen,
                    BLACK,
                    [5 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                    2,
                )
    else:
        draw.rect(
            screen,
            C1_BLUE,
            [intervale + coté_carré / 2, 100, coté_carré, coté_carré],
            0,
        )
        draw.rect(
            screen,
            PINK,
            [2 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
            0,
        )
        draw.rect(
            screen,
            GRIS_CLAIR,
            [3 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
            0,
        )
        draw.rect(
            screen,
            SAUGE_LOANN,
            [4 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
            0,
        )
        draw.rect(
            screen,
            ROSE_CLAIR,
            [5 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
            0,
        )
        if color_fond == C1_BLUE:
            draw.rect(
                screen,
                BLACK,
                [intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                2,
            )
        elif color_fond == PINK:
            draw.rect(
                screen,
                BLACK,
                [2 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                2,
            )
        elif color_fond == GRIS_CLAIR:
            draw.rect(
                screen,
                BLACK,
                [3 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                2,
            )
        elif color_fond == SAUGE_LOANN:
            draw.rect(
                screen,
                BLACK,
                [4 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                2,
            )
        elif color_fond == ROSE_CLAIR:
            draw.rect(
                screen,
                BLACK,
                [5 * intervale + coté_carré / 2, 100, coté_carré, coté_carré],
                2,
            )

    if coord[1] <= 300 + coté_carré / 2 + ecart:
        if coord[1] >= 300 + coté_carré / 2 - ecart:
            for i in range(1, 6):
                if coord[0] <= i * intervale + coté_carré + ecart:
                    if coord[0] >= i * intervale + coté_carré - ecart:
                        draw.rect(
                            screen,
                            WHITE,
                            [
                                i * intervale + coté_carré / 2,
                                300,
                                coté_carré,
                                coté_carré,
                            ],
                            2,
                        )
                        num_col = i
            if num_col != 1:
                draw.rect(
                    screen,
                    VERT,
                    [intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                    0,
                )
            if num_col != 2:
                draw.rect(
                    screen,
                    BLEU_JOLI,
                    [2 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                    0,
                )
            if num_col != 3:
                draw.rect(
                    screen,
                    GRAY,
                    [3 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                    0,
                )
            if num_col != 4:
                draw.rect(
                    screen,
                    bgColor,
                    [4 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                    0,
                )
            if num_col != 5:
                draw.rect(
                    screen,
                    PINK2,
                    [5 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                    0,
                )

    elif (
        coord[1] <= 400 + coté_carré / 2 + ecart
        and coord[1] >= 400 + coté_carré / 2 - ecart
    ):
        for i in range(1, 6):
            if coord[0] <= i * intervale + coté_carré + ecart:
                if coord[0] >= i * intervale + coté_carré - ecart:
                    draw.rect(
                        screen,
                        WHITE,
                        [i * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                        2,
                    )
                    num_col = i + 5
        if num_col != 6:
            draw.rect(
                screen,
                ROSE_FONCE,
                [intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                0,
            )
        if num_col != 7:
            draw.rect(
                screen,
                VIOLET_FONCE,
                [2 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                0,
            )
        if num_col != 8:
            draw.rect(
                screen,
                ROSE_POUDREE,
                [3 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                0,
            )
        if num_col != 9:
            draw.rect(
                screen,
                BLEU,
                [4 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                0,
            )
        if num_col != 10:
            draw.rect(
                screen,
                BLEU_FONCE,
                [5 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                0,
            )

    elif (
        coord[1] <= 500 + coté_carré / 2 + ecart
        and coord[1] >= 500 + coté_carré / 2 - ecart
    ):
        for i in range(1, 6):
            if coord[0] <= i * intervale + coté_carré + ecart:
                if coord[0] >= i * intervale + coté_carré - ecart:
                    draw.rect(
                        screen,
                        WHITE,
                        [i * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                        2,
                    )
                    num_col = i + 10
        if num_col != 11:
            draw.rect(
                screen,
                JAUNE,
                [intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                0,
            )
        if num_col != 12:
            draw.rect(
                screen,
                ORANGE,
                [2 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                0,
            )
        if num_col != 13:
            draw.rect(
                screen,
                ROUGE,
                [3 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                0,
            )
        if num_col != 14:
            draw.rect(
                screen,
                MARRON,
                [4 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                0,
            )
        if num_col != 15:
            draw.rect(
                screen,
                BLACK,
                [5 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                0,
            )

    else:
        draw.rect(
            screen, VERT, [intervale + coté_carré / 2, 300, coté_carré, coté_carré], 0
        )
        draw.rect(
            screen,
            BLEU_JOLI,
            [2 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
            0,
        )
        draw.rect(
            screen,
            GRAY,
            [3 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
            0,
        )
        draw.rect(
            screen,
            bgColor,
            [4 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
            0,
        )
        draw.rect(
            screen,
            PINK2,
            [5 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
            0,
        )

        draw.rect(
            screen,
            ROSE_FONCE,
            [intervale + coté_carré / 2, 400, coté_carré, coté_carré],
            0,
        )
        draw.rect(
            screen,
            VIOLET_FONCE,
            [2 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
            0,
        )
        draw.rect(
            screen,
            ROSE_POUDREE,
            [3 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
            0,
        )
        draw.rect(
            screen,
            BLEU,
            [4 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
            0,
        )
        draw.rect(
            screen,
            BLEU_FONCE,
            [5 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
            0,
        )

        draw.rect(
            screen, JAUNE, [intervale + coté_carré / 2, 500, coté_carré, coté_carré], 0
        )
        draw.rect(
            screen,
            ORANGE,
            [2 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
            0,
        )
        draw.rect(
            screen,
            ROUGE,
            [3 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
            0,
        )
        draw.rect(
            screen,
            MARRON,
            [4 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
            0,
        )
        draw.rect(
            screen,
            BLACK,
            [5 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
            0,
        )

    if choix_color_1 != -1:
        if choix_color_1 == 1:
            draw.rect(
                screen,
                WHITE,
                [1 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                2,
            )
            if num_col == 1:
                draw.rect(
                    screen,
                    BLACK,
                    [1 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                    2,
                )
        if choix_color_1 == 2:
            draw.rect(
                screen,
                WHITE,
                [2 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                2,
            )
            if num_col == 2:
                draw.rect(
                    screen,
                    BLACK,
                    [2 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                    2,
                )
        if choix_color_1 == 3:
            draw.rect(
                screen,
                WHITE,
                [3 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                2,
            )
            if num_col == 3:
                draw.rect(
                    screen,
                    BLACK,
                    [3 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                    2,
                )
        if choix_color_1 == 4:
            draw.rect(
                screen,
                WHITE,
                [4 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                2,
            )
            if num_col == 4:
                draw.rect(
                    screen,
                    BLACK,
                    [4 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                    2,
                )
        if choix_color_1 == 5:
            draw.rect(
                screen,
                WHITE,
                [5 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                2,
            )
            if num_col == 5:
                draw.rect(
                    screen,
                    BLACK,
                    [5 * intervale + coté_carré / 2, 300, coté_carré, coté_carré],
                    2,
                )
        if choix_color_1 == 6:
            draw.rect(
                screen,
                WHITE,
                [1 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                2,
            )
            if num_col == 6:
                draw.rect(
                    screen,
                    BLACK,
                    [1 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                    2,
                )
        if choix_color_1 == 7:
            draw.rect(
                screen,
                WHITE,
                [2 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                2,
            )
            if num_col == 7:
                draw.rect(
                    screen,
                    BLACK,
                    [2 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                    2,
                )
        if choix_color_1 == 8:
            draw.rect(
                screen,
                WHITE,
                [3 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                2,
            )
            if num_col == 8:
                draw.rect(
                    screen,
                    BLACK,
                    [3 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                    2,
                )
        if choix_color_1 == 9:
            draw.rect(
                screen,
                WHITE,
                [4 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                2,
            )
            if num_col == 9:
                draw.rect(
                    screen,
                    BLACK,
                    [4 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                    2,
                )
        if choix_color_1 == 10:
            draw.rect(
                screen,
                WHITE,
                [5 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                2,
            )
            if num_col == 10:
                draw.rect(
                    screen,
                    BLACK,
                    [5 * intervale + coté_carré / 2, 400, coté_carré, coté_carré],
                    2,
                )
        if choix_color_1 == 11:
            draw.rect(
                screen,
                WHITE,
                [1 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                2,
            )
            if num_col == 11:
                draw.rect(
                    screen,
                    BLACK,
                    [2 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                    2,
                )
        if choix_color_1 == 12:
            draw.rect(
                screen,
                WHITE,
                [2 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                2,
            )
            if num_col == 12:
                draw.rect(
                    screen,
                    BLACK,
                    [2 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                    2,
                )
        if choix_color_1 == 13:
            draw.rect(
                screen,
                WHITE,
                [3 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                2,
            )
            if num_col == 14:
                draw.rect(
                    screen,
                    BLACK,
                    [14 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                    2,
                )
        if choix_color_1 == 14:
            draw.rect(
                screen,
                WHITE,
                [4 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                2,
            )
            if num_col == 14:
                draw.rect(
                    screen,
                    BLACK,
                    [4 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                    2,
                )
        if choix_color_1 == 15:
            draw.rect(
                screen,
                WHITE,
                [5 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                2,
            )
            if num_col == 15:
                draw.rect(
                    screen,
                    BLACK,
                    [5 * intervale + coté_carré / 2, 500, coté_carré, coté_carré],
                    2,
                )

    display.flip()


def clic_menu_couleur(coord, num_color_1, num_color_2):
    """
    entrée : une coordonée [x, y], deux entiers correspondants
    aux choix de couleur actuels
    effet : retourne la modification des boutons du menu_couleur
    selectionnés (entre 1 et 15)
    sortie : (num_color_1, num_color_2) modifiés
    """
    nb_color_par_ligne = 5
    intervale = width / (nb_color_par_ligne + 2)
    coté_carré = 50
    ecart = 25
    num = -1
    num_col = -1

    if coord[1] <= 100 + coté_carré / 2 + ecart:
        if coord[1] >= 100 + coté_carré / 2 - ecart:
            for i in range(1, 6):
                if coord[0] <= i * intervale + coté_carré + ecart:
                    if coord[0] >= i * intervale + coté_carré - ecart:
                        num = i

    if coord[1] <= 300 + coté_carré / 2 + ecart:
        if coord[1] >= 300 + coté_carré / 2 - ecart:
            for i in range(1, 6):
                if coord[0] <= i * intervale + coté_carré + ecart:
                    if coord[0] >= i * intervale + coté_carré - ecart:
                        num_col = i

    elif (
        coord[1] <= 400 + coté_carré / 2 + ecart
        and coord[1] >= 400 + coté_carré / 2 - ecart
    ):
        for i in range(1, 6):
            if coord[0] <= i * intervale + coté_carré + ecart:
                if coord[0] >= i * intervale + coté_carré - ecart:
                    num_col = i + 5

    elif coord[1] <= 500 + coté_carré / 2 + ecart:
        if coord[1] >= 500 + coté_carré / 2 - ecart:
            for i in range(1, 6):
                if coord[0] <= i * intervale + coté_carré + ecart:
                    if coord[0] >= i * intervale + coté_carré - ecart:
                        num_col = i + 10

    if num_color_1 == -1:
        num_color_1 = num_col
    elif num_color_1 == num_col:
        num_color_1 = -1
    else:
        num_color_2 = num_col
    return (num, num_color_1, num_color_2)


def attribue_color(
    color_fond, color_1, color_2, num_color_fond, num_color_1, num_color_2
):
    """
    entrée : la couleur du fond, la couleur du j1 et j2,
    leur numéros respectifs choisis
    effet : modifie (color_fond, color_1, color_2) en fonction des nouveaux choix
    sortie : renvoie (color_fond, color_1, color_2) modifié
    """
    if num_color_fond != -1:
        if num_color_fond == 1:
            color_fond = C1_BLUE
        elif num_color_fond == 2:
            color_fond = PINK
        elif num_color_fond == 3:
            color_fond = GRIS_CLAIR
        elif num_color_fond == 4:
            color_fond = SAUGE_LOANN
        elif num_color_fond == 5:
            color_fond = ROSE_CLAIR

    if num_color_1 != -1:
        if num_color_1 == 1:
            color_1 = VERT
        elif num_color_1 == 2:
            color_1 = BLEU_JOLI
        elif num_color_1 == 3:
            color_1 = GRAY
        elif num_color_1 == 4:
            color_1 = bgColor
        elif num_color_1 == 5:
            color_1 = PINK2
        elif num_color_1 == 6:
            color_1 = ROSE_FONCE
        elif num_color_1 == 7:
            color_1 = VIOLET_FONCE
        elif num_color_1 == 8:
            color_1 = ROSE_POUDREE
        elif num_color_1 == 9:
            color_1 = BLUE
        elif num_color_1 == 10:
            color_1 = BLEU_FONCE
        elif num_color_1 == 11:
            color_1 = JAUNE
        elif num_color_1 == 12:
            color_1 = ORANGE
        elif num_color_1 == 13:
            color_1 = ROUGE
        elif num_color_1 == 14:
            color_1 = MARRON
        elif num_color_1 == 15:
            color_1 = BLACK

    if num_color_2 != -1:
        if num_color_2 == 1:
            color_2 = VERT
        elif num_color_2 == 2:
            color_2 = BLEU_JOLI
        elif num_color_2 == 3:
            color_2 = GRAY
        elif num_color_2 == 4:
            color_2 = bgColor
        elif num_color_2 == 5:
            color_2 = PINK2
        elif num_color_2 == 6:
            color_2 = ROSE_FONCE
        elif num_color_2 == 7:
            color_2 = VIOLET_FONCE
        elif num_color_2 == 8:
            color_2 = ROSE_POUDREE
        elif num_color_2 == 9:
            color_2 = BLUE
        elif num_color_2 == 10:
            color_2 = BLEU_FONCE
        elif num_color_2 == 11:
            color_2 = JAUNE
        elif num_color_2 == 12:
            color_2 = ORANGE
        elif num_color_2 == 13:
            color_2 = ROUGE
        elif num_color_2 == 14:
            color_2 = MARRON
        elif num_color_2 == 15:
            color_2 = BLACK

    return (color_fond, color_1, color_2)
