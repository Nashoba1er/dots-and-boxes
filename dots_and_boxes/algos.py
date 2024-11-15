'''
Sommaire des algos :
    - définitions des constantes
    - robot0
    - robot1
    - algo1
    - algo2
    - algo3
    - algo4
'''

from pygame import *
from numpy import *
from copy import *
from time import *
from random import *
from fonctions_de_jeu import *

# les constantes pour les robots :
phase_finale = [False,False]
Turn = [0]

def robot0(clignote,plateau,couleur_bot):
    joue = 0
    [a,b] = dimension = dim(plateau)

    for _ in range (100):
            o = randint(0,1)
            if o == 0 :
                x = randint(0,a-2)
                y = randint(0,b-1)
                if (plateau[0][x][y] == 0 and joue == 0 ) :
                    if time_activation :
                        sleep(delay)
                    draw_arete(clignote,plateau,0,x,y,couleur_bot)
                    joue = joue + 1
                    plateau[0][x][y] = 1
            else :
                x = randint(0,a-1)
                y = randint(0,b-2)
                if (plateau[1][x][y] == 0 and joue == 0 ) :
                    if time_activation :
                        sleep(delay)
                    draw_arete(clignote,plateau,1,x,y,couleur_bot)
                    joue = joue + 1
                    plateau[1][x][y] = 1

    if joue == 0 :  # met une arête horizontale
        for i in range(a-1): 
            for j in range (b):
                if (plateau[0][i][j] == 0 and joue == 0) :
                    if time_activation :
                        sleep(delay)
                    draw_arete(clignote,plateau,0,i,j,couleur_bot)
                    joue = joue + 1
                    plateau[0][i][j] = 1
    if joue == 0 :  #trace une arête verticale
        for i in range(a): 
            for j in range (b-1):
                if (plateau[1][i][j] == 0 and joue == 0) :
                    if time_activation :
                        sleep(delay)
                    draw_arete(clignote,plateau,1,i,j,couleur_bot)
                    joue = joue + 1
                    plateau[1][i][j] = 1
    if not (carre(plateau,couleur_bot)) :
        Turn[0] = (Turn[0] + 1)%2

    display.flip()

def robot1(clignote,plateau,couleur_bot):
    joue = 0
    [a,b] = dimension = dim(plateau)

    ############# -- met une arête là où il peut gagner un point si il le peut -- #############
    for i in range(dimension[0]-1):
        for j in range(dimension[1]-1):
            if(plateau[0][i][j] == 0 and plateau[0][i][j+1]==1 and plateau[1][i+1][j] == 1 and plateau[1][i][j] == 1 and plateau[2][i][j] != 1) :
                if time_activation :
                    sleep(delay)
                draw_arete(clignote,plateau,0,i,j,couleur_bot)
                joue = joue + 1
                plateau[0][i][j] = 1

    if joue == 0 :  
        for i in range(dimension[0]-1):
            for j in range(dimension[1]-1):
                if(plateau[0][i][j] == 1 and plateau[0][i][j+1]==0 and plateau[1][i+1][j] == 1 and plateau[1][i][j] == 1 and plateau[2][i][j] != 1) :
                    if time_activation :
                        sleep(delay)
                    draw_arete(clignote,plateau,0,i,j+1,couleur_bot)
                    joue = joue + 1
                    plateau[0][i][j+1] = 1

    if joue == 0 :  
        for i in range(dimension[0]-1):
            for j in range(dimension[1]-1):
                if(plateau[0][i][j] == 1 and plateau[0][i][j+1]==1 and plateau[1][i+1][j] == 1 and plateau[1][i][j] == 0 and plateau[2][i][j] != 1) :
                    if time_activation :
                        sleep(delay)
                    draw_arete(clignote,plateau,1,i,j,couleur_bot)
                    joue = joue + 1
                    plateau[1][i][j] = 1

    if joue == 0 :  
        for i in range(dimension[0]-1):
            for j in range(dimension[1]-1):
                if(plateau[0][i][j] == 1 and plateau[0][i][j+1]==1 and plateau[1][i+1][j] == 0 and plateau[1][i][j] == 1 and plateau[2][i][j] != 1) :
                    if time_activation :
                        sleep(delay)
                    draw_arete(clignote,plateau,1,i+1,j,couleur_bot)
                    joue = joue + 1
                    plateau[1][i+1][j] = 1

    ############################################################################################

    if joue == 0 :  # met une arête horizontale
        for i in range(a-1): 
            for j in range (b):
                if (plateau[0][i][j] == 0 and joue == 0) :
                    if time_activation :
                        sleep(delay)
                    draw_arete(clignote,plateau,0,i,j,couleur_bot)
                    joue = joue + 1
                    plateau[0][i][j] = 1
    if joue == 0 :  #trace une arête verticale
        for i in range(a): 
            for j in range (b-1):
                if (plateau[1][i][j] == 0 and joue == 0) :
                    if time_activation :
                        sleep(delay)
                    draw_arete(clignote,plateau,1,i,j,couleur_bot)
                    joue = joue + 1
                    plateau[1][i][j] = 1
    if not (carre(plateau,couleur_bot)) :
        Turn[0] = (Turn[0] + 1)%2

    display.flip()
    
def algo1(clignote,plateau,couleur_bot):
    #peut-on prendre un point ?")
    arete_gagnante = aretes_gagnantes(plateau)
    if arete_gagnante == False : 
        #NON on ne peut pas prendre de point") 
        #existe-t-il une arête sûre ?")
        sure_arete = arete_sure(plateau)
        # print(arete_sure(plateau))
        if sure_arete == False : 
            #NON il n'existe pas d'arête sûre")
            #on prend une arête au hasard ")
            (o,x,y) = random_arete_dispo(plateau)
            if time_activation :
                sleep(delay)
            if o != -1 :
                draw_arete(clignote,plateau,o,x,y,couleur_bot)
                plateau[o][x][y] = 1
        else :  
            #OUI il existe une arête sûre")
            #on la prend")
            (o,x,y) = sure_arete 
            if time_activation :
                sleep(delay)
            draw_arete(clignote,plateau,o,x,y,couleur_bot)
            plateau[o][x][y] = 1
    else : 
        #OUI on peut prendre un point")
        #on le prend")
        (o,x,y) = arete_gagnante
        if time_activation :
            sleep(delay)
        draw_arete(clignote,plateau,o,x,y,couleur_bot)
        plateau[o][x][y] = 1
    
    if not (carre(plateau,couleur_bot)) :
        Turn[0] = (Turn[0] + 1)%2
    # pour_y_voir_plus_clair(plateau)
    display.flip()

def algo2(clignote,plateau,couleur_bot):
    # pour_y_voir_plus_clair(plateau)
    #peut-on prendre un point ?")
    arete_gagnante = aretes_gagnantes(plateau)
    if arete_gagnante == False : 
        #NON on ne peut pas prendre de point") 
        #existe-t-il une arête sûre ?")
        sure_arete = arete_sure(plateau)
        # print(arete_sure(plateau))
        if sure_arete == False : 
            #NON il n'existe pas d'arête sûre")
            #on prend l'arête qui minimise les points donnés à l'adversaire")
            best_arrete = trouve_meilleure_arête(plateau)
            o = best_arrete[1]
            x = best_arrete[2]
            y = best_arrete[3]
            if time_activation :
                sleep(delay)
            draw_arete(clignote,plateau,o,x,y,couleur_bot)
            plateau[o][x][y] = 1
        else :  
            #OUI il existe une arête sûre")
            #on la prend")
            (o,x,y) = sure_arete 
            if time_activation :
                sleep(delay)
            draw_arete(clignote,plateau,o,x,y,couleur_bot)
            plateau[o][x][y] = 1
    else : 
        #OUI on peut prendre un point")
        #on le prend !")
        (o,x,y) = arete_gagnante
        if time_activation :
            sleep(delay)
        draw_arete(clignote,plateau,o,x,y,couleur_bot)
        plateau[o][x][y] = 1

    if not (carre(plateau,couleur_bot)) :
        Turn[0] = (Turn[0] + 1)%2
    # pour_y_voir_plus_clair(plateau)
    display.flip()

def algo3(clignote,plateau,couleur_bot):
    # pour_y_voir_plus_clair(plateau)
    #peut-on prendre un point ?")
    arete_gagnante = aretes_gagnantes(plateau)
    if arete_gagnante == False : 
        #NON on ne peut pas prendre de point") 
        #existe-t-il une arête sûre ?")
        sure_arete = arete_sure(plateau)
        # print(arete_sure(plateau))
        if sure_arete == False : 
            #NON il n'existe pas d'arête sûre")
            #on prend l'arête qui minimise les points donnés à l'adversaire")
            best_arrete = trouve_meilleure_arête(plateau)
            o = best_arrete[1]
            x = best_arrete[2]
            y = best_arrete[3]
            if time_activation :
                sleep(delay)
            draw_arete(clignote,plateau,o,x,y,couleur_bot)
            plateau[o][x][y] = 1
        else :  
            #OUI il existe une arête sûre")
            #on la prend")
            (o,x,y) = sure_arete 
            if time_activation :
                sleep(delay)
            draw_arete(clignote,plateau,o,x,y,couleur_bot)
            plateau[o][x][y] = 1
    else : 
        #OUI on peut prendre un point")
        #la chaine ouverte est-elle la dernière chaine ?")
        if fin_phase_finale(plateau):
            #OUI c'est donc la fin de la phase finale !")
            #On prend l'arete gagnante et en recommançant à jouer on terminera toutes les chaines")
            (o,x,y) = arete_gagnante
            if time_activation :
                sleep(delay)
            draw_arete(clignote,plateau,o,x,y,couleur_bot)
            plateau[o][x][y] = 1
        else :
            #NON ce n'est pas la fin de la phase finale")
            #somme-nous en phase finale ? (aucune arête sûre & que des chaines de longueur >= 3)")
            if bool_phase_finale(plateau) : 
                #OUI ! on est en phase finale")
                #avant tout, on teste qu'on n'est pas en train de se faire pieger par une règle de la double case...
                #est-ce un piège ?")
                (oo,ii,jj) = arete_gagnante
                plateau[oo][ii][jj] = 1
                pas_piege = aretes_gagnantes(plateau)
                if pas_piege == False : 
                    #c'est un piège !")
                    if time_activation :
                        sleep(delay)
                    draw_arete(clignote,plateau,oo,ii,jj,couleur_bot)
                    #on a joué de cette façon")
                else : 
                    # ce n'est pas un piège")
                    plateau[oo][ii][jj] = 0
                    #on fait la règle de la double case :")
                    regle_double_case(plateau,couleur_bot)
                    while carre(plateau,couleur_bot):
                        regle_double_case(plateau,couleur_bot)
            else : 
                #NON, on est pas en phase finale")
                #on prend l'arete gagnante")
                (o,x,y) = arete_gagnante
                if time_activation :
                    sleep(delay)
                draw_arete(clignote,plateau,o,x,y,couleur_bot)
                plateau[o][x][y] = 1
    
    if not (carre(plateau,couleur_bot)) :
        Turn[0] = (Turn[0] + 1)%2
    # pour_y_voir_plus_clair(plateau)
    display.flip()

def algo4(clignote,plateau,c): 
    couleur_bot = c  
    # pour_y_voir_plus_clair(plateau)
    #peut-on prendre un point ?")
    arete_gagnante = aretes_gagnantes(plateau)
    if arete_gagnante == False : 
        #NON on ne peut pas prendre de point") 
        #existe-t-il une arête sûre ?")
        sure_arete = arete_sure(plateau)
        # print(arete_sure(plateau))
        if sure_arete == False : 
            #NON il n'existe pas d'arête sûre")
            #sommes-nous dans le cas de sprague-grundy ?")
            if test_grundy(plateau) == True :
                #-> sprague grundy
                #au tour de grundy !")
                sprague_grundy(clignote,plateau,c)
            else : 
                #on prend l'arête qui minimise les points donnés à l'adversaire")
                best_arrete = trouve_meilleure_arête(plateau)
                o = best_arrete[1]
                x = best_arrete[2]
                y = best_arrete[3]
                if time_activation :
                    sleep(delay)
                draw_arete(clignote,plateau,o,x,y,couleur_bot)
                plateau[o][x][y] = 1
        else :  
            #OUI il existe une arête sûre")
            #on la prend")
            (o,x,y) = sure_arete 
            if time_activation :
                sleep(delay)
            draw_arete(clignote,plateau,o,x,y,couleur_bot)
            plateau[o][x][y] = 1
    else : 
        #OUI on peut prendre un point")
        #la chaine ouverte est-elle la dernière chaine ?")
        if fin_phase_finale(plateau):
            #OUI c'est la fin de la phase finale !")
            #On prend l'arete gagnante et en recommançant à jouer on terminera toutes les chaines")
            (o,x,y) = arete_gagnante
            if time_activation :
                sleep(delay)
            draw_arete(clignote,plateau,o,x,y,couleur_bot)
            plateau[o][x][y] = 1
        else :
            #NON ce n'est pas la fin de la phase finale")
            #somme-nous en phase finale ? (aucune arête sûre & que des chaines de longueur >= 3)")
            if bool_phase_finale(plateau) : 
                #OUI ! on est en phase finale")
                #avant tout, on teste qu'on n'est pas en train de se faire pieger par une règle de la double case...
                #est-ce un piège ?")
                (oo,ii,jj) = arete_gagnante
                plateau[oo][ii][jj] = 1
                pas_piege = aretes_gagnantes(plateau)
                if pas_piege == False : 
                    #c'est un piège !")
                    if time_activation :
                        sleep(delay)
                    draw_arete(clignote,plateau,oo,ii,jj,couleur_bot)
                    #on a joué de cette façon")
                else : 
                    # ce n'est pas un piège")
                    plateau[oo][ii][jj] = 0
                    #on fait la règle de la double case :")
                    regle_double_case(plateau,c)
                    while carre(plateau,c):
                        regle_double_case(plateau,c)
            else : 
                #NON, on est pas en phase finale")
                #sommes-nous dans le cas de sprague-grundy ?")
                if test_grundy(plateau) == True :
                    #-> sprague grundy
                    #au tour de grundy !")
                    sprague_grundy(clignote,plateau,c)
                else : 
                    #on est pas dans un cas de jeu de Nim")
                    #on prend l'arete gagnante")
                    (o,x,y) = arete_gagnante
                    if time_activation :
                        sleep(delay)
                    draw_arete(clignote,plateau,o,x,y,couleur_bot)
                    plateau[o][x][y] = 1
    
    if not (carre(plateau,couleur_bot)) :
        Turn[0] = (Turn[0] + 1)%2
    # pour_y_voir_plus_clair(plateau)
    display.flip()
