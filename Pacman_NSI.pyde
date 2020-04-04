#                                     Le Pacman 
#                        de Julien Goetghebeur et Evan Guyomarch
#
from random import choice

TAILLE_GRILLE = (84,90)
TAILLE_CASE = 9

with open("classement1.csv","r") as fichier :
    classement = []
    for ligne in fichier :
        l = ligne.split(',')
        l[-1] = l[-1].strip('\n')
        classement.append(l)

def nouvelle_grille():
    with open("grille.csv", "r") as file :
        plateau = []
        for ligne in file :
            l = ligne.split(';')
            for i in range(len(l)):
                l[i]=l[i].strip("\r\n")
            plateau.append(l)
    return plateau

affichage = 'accueil'
clic = ''
direction_possible = ["haut", "bas", "droite", "gauche"]
choix_nom = ""

le_plus_fort = 'fantome'
score = 0
grille = nouvelle_grille()
chrono = 0
nb_fantomes_mange = 0
nb_pieces_mange = 0
nb_pastilles_mange = 0
niveau = 1
partie_en_cour = False
compteur_fantome_mange = 0
prochain_virage = "aucun"
decompte = 4

font_ecriture = PFont()
font_titre = PFont()






def setup():
    global image_pause,regles2,compteur_image,image_pacman,image_blinky,image_pinky,image_inky,image_clyde,image_fantomePeur,Pacman,Blinky,Pinky,Inky,Clyde,fantomes,font_ecriture,font_titre,image_pacman_d,image_pacman_g,image_pacman_b,image_pacman_h,regles,logo
    
    size(TAILLE_GRILLE[0]*TAILLE_CASE+300,TAILLE_GRILLE[1]*TAILLE_CASE)
    frameRate(10)
    background(255)
    rectMode(CENTER)
    textAlign(CENTER)
    imageMode(CENTER)
    noStroke()
    image_pause = loadImage("pacman-sleep.gif")
    regles = loadImage("regle-pacman2.png")
    logo = loadImage("pacman-logo.jpg")
    image_pacman = loadImage("pacman.png")
    compteur_image = loadImage("compteur.png")
    regles2 = loadImage("regle-pacman3.png")
    
    font_ecriture = loadFont("04b30-48.vlw")
    font_titre = createFont("PAC-FONT.TTF",48)
    
    image_pacman_d = loadImage("pacmandroite.gif")
    image_pacman_g = loadImage("pacmangauche.gif")
    image_pacman_b = loadImage("pacmanbas.gif")
    image_pacman_h = loadImage("pacmanhaut.gif")
    
    image_blinky = loadImage("blinky.gif")
    image_pinky = loadImage("pinky.gif")
    image_inky = loadImage("inky.gif")
    image_clyde = loadImage("clyde.gif")
    image_fantomePeur = loadImage("fantome-peur.gif")
    
    Pacman = {"x" : 43, "y" : 67, "direction" : "haut", "vitesse" : 0, "vie" : 3, "vivant" : True, "image" : image_pacman_d }
    Blinky = {"x" : 37, "y" : 40, "direction" : "haut", "vitesse" : 1, "vivant" : True, "image" : image_blinky}
    Pinky = {"x" : 46, "y" : 40, "direction" : "haut", "vitesse" : 1, "vivant" : True, "image" : image_pinky}
    Inky = {"x" : 37, "y" : 43, "direction" : "haut", "vitesse" : 1, "vivant" : True, "image" : image_inky}
    Clyde = {"x" : 46, "y" : 43, "direction" : "haut", "vitesse" : 1, "vivant" : True, "image" : image_clyde}
    fantomes = [Blinky, Pinky, Inky, Clyde]
    
    

    
def draw():
    global affichage, grille,score, partie_en_cour, niveau, decompte
    
    if affichage == 'accueil' :
        clic = ecran_titre()
        if clic == 'JOUER':
            affichage = 'jeu'
        elif clic == 'QUITTER':
            exit()
            
    elif affichage == 'jeu':
        if Pacman["vivant"] :
            if la_grille_est_vide(grille) :
                initialisation_niveau()
                niveau += 1
            else :
                if partie_en_cour :
                    jeu()
                else :
                    if decompte != 4 and decompte != 0  :
                        attendre(1000)
                    compte_a_rebourd()
        else :
            if score > int(classement[4][2]) :
                affichage = 'record battu'
                attendre(500)
            else : 
                affichage = 'gameover'
    
    elif affichage == 'record battu':
        clic = ecran_record_battu()
        if clic == 'SUIVANT':
            record_battu()
            affichage = 'gameover'
            attendre(500)
            
    elif affichage == 'gameover':
        clic = ecran_fin()
        if clic == 'REJOUER':
            affichage = 'jeu'
            initialisation_debut()
        elif clic == 'QUITTER':
            exit()
    
    elif affichage == 'pause':
        clic = ecran_pause()
        if clic == 'REPRENDRE' :
            affichage = 'jeu'
        elif clic == 'QUITTER' :
            exit()




def jeu():
    global affichage  
    background(0)
    
    afficher_grille(grille)
    afficher_pacman(Pacman)
    afficher_fantomes(fantomes)  
    
    clic = afficher_bande()
    if clic == 'PAUSE':
        affichage = 'pause'
    elif clic == 'QUITTER':
        exit()
    
    
    for i in fantomes :
        if i["x"]-2 < Pacman["x"] < i["x"]+2 and i["y"]-2 < Pacman["y"] < i["y"]+2:
            collision(Pacman,i)
    
    choix_direction()
    avancer_personnage(Pacman)
    deplacement_fantomes()
    case_occupe()
    
    if chrono + 10000 <= millis():
        retour_a_la_normale()






def compte_a_rebourd():
    global decompte,partie_en_cour
    decompte -= 1
    background(0)
    afficher_grille(grille)
    afficher_pacman(Pacman)
    afficher_fantomes(fantomes)
    afficher_bande()
    fill(255,0,0)
    textSize(40)
    text(str(decompte),TAILLE_GRILLE[0]*TAILLE_CASE/2,TAILLE_GRILLE[1]*TAILLE_CASE/2)
    if decompte == 0:
        partie_en_cour = True

def attendre(nb) :
    temps1 = millis()
    while (millis() < temps1 + nb) :
        pass    

def la_grille_est_vide(grille) :
    """
    Verifie si il reste des pièces/pastilles sur la grille.
    """
    for i in range(len(grille)) :
        for j in grille[i]:
            if j == "1" or j == "5" :
                return False
    else :
        return True
        
def initialisation_debut() :
    """
    Réinitialise les variables nécessaires à une nouvelle partie.
    - met les scores et les compteur a zéro
    - fait respawn tout les personnages
    - remplace la grille
    """
    global le_plus_fort,score,chrono,nb_fantomes_mange, nb_pieces_mange,nb_pastilles_mange,Pacman,Blinky,Pinky,Inky,Clyde,grille,niveau,partie_en_cour,decompte
    le_plus_fort = "fantome"
    chrono = 0
    score = 0
    nb_fantomes_mange = 0
    nb_pieces_mange = 0
    nb_pastilles_mange = 0
    Pacman["vivant"] = True
    Pacman["vie"] = 3
    Pacman["x"] = 43
    Pacman["y"] = 67
    Blinky["x"] = 37
    Blinky["y"] = 40 
    Pinky["x"] = 46
    Pinky["y"] = 40
    Inky["x"] = 37
    Inky["y"] = 43
    Clyde["x"] = 46
    Clyde["y"] = 43
    grille = nouvelle_grille()
    niveau = 0
    Pacman["direction"] = "haut"
    partie_en_cour = False
    decompte = 4

def initialisation_niveau():
    """
    réinitialise les variables nécessaire à un nouveau niveau
    - les personnages retourne au positions de départ
    - la grille est remplacer
    """
    global le_plus_fort,chrono,Pacman,Blinky,Pinky,Inky,Clyde,grille
    Pacman["x"] = 43
    Pacman["y"] = 67
    Blinky["x"] = 37
    Blinky["y"] = 40 
    Pinky["x"] = 46
    Pinky["y"] = 40
    Inky["x"] = 37
    Inky["y"] = 43
    Clyde["x"] = 46
    Clyde["y"] = 43
    grille = nouvelle_grille()
    chrono = 0
    le_plus_fort = "fantome"
    Pacman["direction"] = "haut"

def record_battu():
    """
    Fonction appelé lorsque le joueur bat un record du classement.
    - détermine le record battu
    - modifie le classement et l'écrit sur le document : "classement1.csv"
    """
    global score,choix_nom,classement
    rang = -1
    for i in classement :
        if score > int(i[2]) :
            if rang == -1 :
                rang = int(i[0])
    for j in range(4,rang-1,-1):
        classement[j] = classement[j-1][:]
        classement[j][0] = j+1
    classement[rang-1][1] = choix_nom
    classement[rang-1][2] = score
    classement[rang-1][3] = niveau
    
    with open("classement1.csv","w") as fichier :
        for i in range(len(classement)):
            ligne = str(classement[i][0])
            for j in range(1,len(classement[i])):
                ligne = ligne + "," + str(classement[i][j])
            fichier.write(ligne+"\n")



#####################################PERSONNAGES#######################################################################################################################################################

def collision(pacman,fantome) :
    """
    Fonction qui est appelé lorsqu'il y a une collision entre un fantome et un pacman.
    - soit le pacman mange le fantome et il gagne des points
    - soit il meurt et tout les personnages respawn.
    """
    global le_plus_fort,score,compteur_fantome_mange,nb_fantomes_mange
    if le_plus_fort == "fantome" :
        pacman["vie"] -= 1
        pacman["x"] = 43
        pacman["y"] = 67
        pacman["direction"] = "haut"
        Blinky["x"] = 37
        Blinky["y"] = 40 
        Pinky["x"] = 46
        Pinky["y"] = 40
        Inky["x"] = 37
        Inky["y"] = 43
        Clyde["x"] = 46
        Clyde["y"] = 43
        if pacman["vie"] == 0 :
            pacman["vivant"] = False
         
    elif le_plus_fort == "pacman" :
        compteur_fantome_mange += 1
        nb_fantomes_mange += 1
        fantome["vivant"] = False
        fantome_respawn(fantome)
        score += (compteur_fantome_mange+1)*100
        

def avancer_personnage(perso) :
    """
    Fonction qui fait avancer le personnage.
    """
    if passe_tunel(perso):
        if perso["direction"] == "droite" :
            perso["x"] = 5
        elif perso["direction"] == "gauche" :
            perso["x"] = TAILLE_GRILLE[0]-5
        
    if est_bloque_front(perso) == False:
        if perso["direction"] == "haut":
            perso["y"] = perso["y"] - perso["vitesse"]
        elif perso["direction"] == "bas":
            perso["y"] = perso["y"] + perso["vitesse"]
        elif perso["direction"] == "droite":
            perso["x"] = perso["x"] + perso["vitesse"]    
        elif perso["direction"] == "gauche":
            perso["x"] = perso["x"] - perso["vitesse"]

def est_bloque_front(perso):
    """
    Détecte si il y a un mur devant le personnage.
    """
    if perso["direction"] == "haut" and est_bloque_up(perso) :
        return True
    elif perso["direction"] == "bas" and est_bloque_down(perso) :
        return True
    elif perso["direction"] == "droite" and est_bloque_right(perso) :
        return True
    elif perso["direction"] == "gauche" and est_bloque_left(perso) :
        return True
    else: 
        return False

def est_bloque_up(perso):
    """
    Détecte si il y a un mur au dessus du personnage.
    """
    if grille[perso["y"]-2][perso["x"]-1] ==  "10" or grille[perso["y"]-2][perso["x"]] ==  "10" or grille[perso["y"]-2][perso["x"]+1] ==  "10" :
        return True
    else :
        return False

def est_bloque_right(perso):
    """
    Détecte si il y a un mur a droite du personage
    """
    if grille[perso["y"]-1][perso["x"]+2] ==  "10" or grille[perso["y"]][perso["x"]+2] ==  "10" or grille[perso["y"]+1][perso["x"]+2] ==  "10" :
        return True
    else :
        return False

def est_bloque_left(perso):
    """
    Détecte si il y a un mur à gauche du personnage.
    """
    if grille[perso["y"]-1][perso["x"]-2] ==  "10" or grille[perso["y"]][perso["x"]-2] ==  "10" or grille[perso["y"]+1][perso["x"]-2] ==  "10":
        return True
    else :
        return False

def est_bloque_down(perso):
    """
    Détecte si il y a un mur en dessous du personnage.
    """
    if grille[perso["y"]+2][perso["x"]-1] ==  "10" or grille[perso["y"]+2][perso["x"]] ==  "10" or grille[perso["y"]+2][perso["x"]+1] ==  "10" :
        return True
    else :
        return False

def passe_tunel(perso):
    """
    Détecte si le pacman passe dans un tunel (sur les cotés de la grille)
    """
    if grille[perso["y"]][perso["x"]] == "2":
        return True
    else : 
        return False

#######PACMAN######

def choix_direction():  
    """
    Fonction qui permet au joueur de changer la direction du pacmen.
    - avec les flèches du clavier
    - enregistre la direction voulu puis regarde si le pacman peut tourner
    - sinon garde la direction en mémoire pour que le pacman tourne après ce qui permet de facilité la tâche au joueur.
    """
    global Pacman, prochain_virage,image_pacman_d,image_pacman_g,image_pacman_b,image_pacman_h
    if keyPressed :
        if key == CODED:
            Pacman["vitesse"] = 1
            if keyCode == RIGHT:
                prochain_virage = "droite"
            elif keyCode == LEFT :
                prochain_virage = "gauche"
            elif keyCode == UP :
                prochain_virage = "haut"
            elif keyCode == DOWN :
                prochain_virage = "bas"
    if prochain_virage == "droite" and est_bloque_right(Pacman) == False :
        Pacman["direction"] = "droite"
        Pacman["image"] = image_pacman_d
        prochain_virage = "aucun"
    elif prochain_virage == "gauche" and est_bloque_left(Pacman) == False :
        Pacman["direction"] = "gauche"
        Pacman["image"] = image_pacman_g
        prochain_virage = "aucun"
    elif prochain_virage == "haut" and est_bloque_up(Pacman) == False :
        Pacman["direction"] = "haut"
        Pacman["image"] = image_pacman_h
        prochain_virage = "aucun"
    elif prochain_virage == "bas" and est_bloque_down(Pacman) == False :
        Pacman["direction"] = "bas"
        Pacman["image"] = image_pacman_b
        prochain_virage = "aucun"

def case_occupe() : 
    """
    Fonction qui agit en fonction de la case sur laquelle se trouve le pacman
    - regarde si il est sur une pièce ou une pastille
    - si oui, augmente le score et le compteur
    - transforme la case en couloir vide
    """
    global grille,Pacman, score,nb_pieces_mange,nb_pastilles_mange
    if grille[Pacman["y"]][Pacman["x"]] == "1" :
        score += 25
        nb_pieces_mange += 1
        grille[Pacman["y"]][Pacman["x"]] = "0"

    elif grille[Pacman["y"]][Pacman["x"]] == "5" :
        score += 50 
        nb_pastilles_mange += 1
        pastille_mange() 
        grille[Pacman["y"]][Pacman["x"]] = "0"

def pastille_mange() : 
    """
    Fonction qui est appelé lorsque le pacman mange une pastille.
    - le pacman devient le plus fort
    - les fantomes changent d'aparance
    - le compteur de fantome mangé est remis a 0 (est utilisé pour le nombre de point gagné)
    """
    global le_plus_fort,fantomes,chrono,image_fantomePeur,compteur_fantome_mange
    le_plus_fort = "pacman"
    compteur_fantome_mange = 0
    for i in fantomes :
        i["image"] = image_fantomePeur
    chrono = millis()

########FANTOMES#########

def retour_a_la_normale():
    """
    Fonction appelé lorsque la pastille ne fais plus d'effet.
    - les fantomes redeviennent les plus forts
    - et reprennent leurs aparances normales
    """
    global le_plus_fort ,image_clyde,image_inky,image_pinky,image_blinky
    le_plus_fort = "fantome"
    Blinky["image"] = image_blinky
    Pinky["image"] = image_pinky
    Inky["image"] = image_inky
    Clyde["image"] = image_clyde

def deplacement_fantomes():
    """
    Fonction qui fais s'occupe du déplacement des fantomes.
    - calcule le vecteur entre le fantome et le pacman
    - lorsque le fantome arrive a un carrefour, il choisi une direction
    - plus le fantome est proche du pacman, plus la probabilité qu'il choisisse sa direction est élevée :
        * entre 50 et 30 cases de distance -> 1 chance de plus d'aller vers le pacman
        * entre 30 et 20 -> 3 chances de plus
        * entre 20 et 10 -> 5 chances de plus 
        * moins de 10 -> 7 chances de plus
    """
    global fantomes,dir_poids,direction_possible
    for f in fantomes :
        direction_possible = ["haut", "bas", "droite", "gauche"]
        est_sur_carrefour = False
# Détecte si le fantome est sur un carrefour
        if f["direction"] == "droite" or f["direction"] == "gauche" :
            if est_bloque_up(f) == False or est_bloque_down(f) == False:
                est_sur_carrefour = True
        else : 
            if est_bloque_right(f) == False or est_bloque_left(f) == False :
                est_sur_carrefour = True
# Calcule le vecteur fantome->pacman
        if est_sur_carrefour == True :
            vers_pacman = (Pacman["x"] - f["x"],Pacman["y"] - f["y"])
# Si le pacman est à droite du fantome            
            if vers_pacman[0] > 0 :
                if 30 < vers_pacman[0] < 50 or 30 < vers_pacman[1] < 50 :
                    direction_possible.append("droite")
                elif 20 < vers_pacman[0] < 30 or 20 < vers_pacman[1] < 30 :
                    for i in range(3):
                        direction_possible.append("droite")
                elif 10 < vers_pacman[0] < 20 or 10 < vers_pacman[1] < 20 :
                    for i in range(5):
                        direction_possible.append("droite")
                elif vers_pacman[0] < 10 or vers_pacman[1] < 10 :
                    for i in range(7):
                        direction_possible.append("droite")
# Si le pacman est à gauche du fantome
            if vers_pacman[0] < 0 :
                if -50 < vers_pacman[0] < -30 or -50 < vers_pacman[1] < -30 :
                    direction_possible.append("gauche")
                elif -30 < vers_pacman[0] < -20 or -30 < vers_pacman[1] < -20 :
                    for i in range(3):
                        direction_possible.append("gauche")
                elif -20 < vers_pacman[0] < -10 or -20 < vers_pacman[1] < -10 :
                    for i in range(5):
                        direction_possible.append("gauche")
                elif -10 < vers_pacman[0] or -10 < vers_pacman[1] :
                    for i in range(7):
                        direction_possible.append("gauche")
# Si le pacman est en dessous du fantome
            if vers_pacman[1] > 0 :
                if 30 < vers_pacman[0] < 50 or 30 < vers_pacman[1] < 50 :
                    direction_possible.append("bas")
                elif 20 < vers_pacman[0] < 30 or 20 < vers_pacman[1] < 30 :
                    for i in range(3):
                        direction_possible.append("bas")
                elif 10 < vers_pacman[0] < 20 or 10 < vers_pacman[1] < 20 :
                    for i in range(5):
                        direction_possible.append("bas")
                elif vers_pacman[0] < 10 or vers_pacman[1] < 10 :
                    for i in range(7):
                        direction_possible.append("bas")
# Si le pacman est au dessus du fantome
            if vers_pacman[1] < 0 :
                if -50 < vers_pacman[0] < -30 or -50 < vers_pacman[1] < -30 :
                    direction_possible.append("haut")
                elif -30 < vers_pacman[0] < -20 or -30 < vers_pacman[1] < -20 :
                    for i in range(3):
                        direction_possible.append("haut")
                elif -20 < vers_pacman[0] < -10 or -20 < vers_pacman[1] < -10 :
                    for i in range(5):
                        direction_possible.append("haut")
                elif -10 < vers_pacman[0] or -10 < vers_pacman[1] :
                    for i in range(7):
                        direction_possible.append("haut")    
            f["direction"] = choice(direction_possible)    
        while est_bloque_front(f):
            f["direction"] = choice(direction_possible)
        avancer_personnage(f)

def fantome_respawn(f) :
    """
    Fonction qui ramène le fantome au coordonnées de départ (40,40).
    """
    f["x"] = 40
    f["y"] = 40
    f["vivant"] = True



#####################################INTERFACE##GRAPHIQUE##################################################################################################################################################

def afficher_grille(grille):
    """
    Fonction qui affiche la grille
    """
    pastille = []
    for i in range(len(grille)) :
        for j in range(len(grille[i])):
            x = j
            y = i
            if grille[i][j] == "10":
                afficher_mur(x,y)
            elif grille[i][j] == "1":
                afficher_piece(x,y)
            elif grille[i][j] == "0" or grille[i][j] == "2" :
                afficher_couloir(x,y)
            elif grille[i][j] == "5":
                pastille.append((x,y))
# pour que les pastilles s'affiche en dernier, pour pas être recouvert par les autres cases--> le rond est plus grand que une case, ce qui n'est pas le cas de la pièce        
    for coord in pastille :
        afficher_pastille(coord[0],coord[1]) 
    
def afficher_mur(x,y):
    """
    Affiche un carré noir pour représenter un mur.
    """
    fill(0)
    square(x*TAILLE_CASE+TAILLE_CASE/2,y*TAILLE_CASE+TAILLE_CASE/2,TAILLE_CASE)
    
def afficher_couloir(x,y):
    """
    Affiche un carré bleu pour représenter un couloir vide.
    """
    fill(20,0,255)
    square(x*TAILLE_CASE+TAILLE_CASE/2,y*TAILLE_CASE+TAILLE_CASE/2,TAILLE_CASE)
    
def afficher_piece(x,y):
    """
    Affiche un carré bleu avec un rond blanc dessus pour représenter un couloir avec une pièce.
    """
    afficher_couloir(x,y)
    noStroke()
    fill(255)
    circle(x*TAILLE_CASE+TAILLE_CASE/2,y*TAILLE_CASE+TAILLE_CASE/2,9)

def afficher_pastille(x,y):
    """
    Affiche un carré bleu avec un rond orange pour représenter un couloir avec une pastille.
    """
    afficher_couloir(x,y)
    noStroke()
    fill(255,130,0)
    circle(x*TAILLE_CASE+TAILLE_CASE/2,y*TAILLE_CASE+TAILLE_CASE/2,15)

def afficher_pacman(p):
    """
    Affiche l'image pacman.
    """
    image(p["image"],p["x"]*TAILLE_CASE+TAILLE_CASE/2,p["y"]*TAILLE_CASE+TAILLE_CASE/2)

def afficher_fantomes(f):
    """
    Affiche l'image correspondante à chaque fantôme.
    """
    for i in f :
        image(i["image"],i["x"]*TAILLE_CASE+TAILLE_CASE/2,i["y"]*TAILLE_CASE+TAILLE_CASE/2)

def bouton(x,y,largeur,hauteur,texte,couleur,couleur2):
    """
    Fonction qui affiche un bouton qui change de couleur quand la souris passe dessus.
    x,y : coordonnées du bouton
    largeur,hauteur : dimension du bouton
    couleur : couleur du bouton quand la souris passe dessus
    couleur2 : couleur du bouton
    """
    textSize(30)
    if  x - largeur/2 < mouseX < x + largeur/2 and  y-hauteur/2 < mouseY < y + hauteur/2 :
        fill (couleur[0],couleur[1],couleur[2])
        rect(x,y,largeur,hauteur,20)
        fill(0,0,0)
        text(texte,x,y+hauteur*0.28)
        if mousePressed :
            return True
    else:
        fill (couleur2[0],couleur2[1],couleur2[2])
        rect(x,y,largeur,hauteur,20)
        fill(0,0,0)
        text(texte,x,y+hauteur*0.28)
    return False

def afficher_bande():
    """
    Fonction qui affiche le bandeau qui se trouve sur le côté de la fenêtre.
    - bouton QUITTER et PAUSE
    - indique le score et les détails
    - indique le nombre de vies restantes
    - les règles
    """
    global score,classement,image_pacman,compteur_image,regles2
    textAlign(LEFT)
    clic = ''
# Score
    fill(255)
    textSize(30)
    text("score : "+ str(score) ,TAILLE_GRILLE[0]*TAILLE_CASE-10,50)
    # details des scores : nombres de piece , de pastille, et de fantomes mangé + nb de vies restantes + niveaux
    image(compteur_image,TAILLE_GRILLE[0]*TAILLE_CASE+150,height/3+100,300,400)
    textSize(24)
    text(str(nb_pastilles_mange),TAILLE_GRILLE[0]*TAILLE_CASE+125,height/3-47)
    text(str(nb_pieces_mange),TAILLE_GRILLE[0]*TAILLE_CASE+125,height/3-7)
    text(str(nb_fantomes_mange),TAILLE_GRILLE[0]*TAILLE_CASE+125,height/3+33)
# nb de vie restante représenté par des icons pacman
    for i in range(1,Pacman["vie"]+1):
        image(image_pacman,TAILLE_GRILLE[0]*TAILLE_CASE+(i*40),150,32,32)
# Règles
    image(regles2,TAILLE_GRILLE[0]*TAILLE_CASE+150,width/2+50,300,400)
    textAlign(CENTER)
# Boutons
    if bouton(TAILLE_GRILLE[0]*TAILLE_CASE+150,height-145,250,50,"PAUSE",[100,100,255],[0,0,255]):
        clic = 'PAUSE'
    if bouton(TAILLE_GRILLE[0]*TAILLE_CASE+150,height-75,250,50,"QUITTER",[255,100,100],[255,0,0]):
        clic = 'QUITTER'
    return clic

def ecran_titre():
    global classement,font_titre,font_ecriture,regles,logo
    """
    Affiche l'écran d'accueil du jeu.
    -Propose de jouer ou de quitter
    -Affiche le classement 
    -affiche les règles
    """
    background(0)
    clic = ''
# Titre
    textFont(font_titre)
    textSize(90)
    fill(255,255,0)
    text("pac-man",width/2,180)
    textFont(font_ecriture)
# Boutons
    stroke(0,232,36)
    if bouton(200,height-100,220,60,'JOUER',[100,232,132],[0,232,36]):
        clic = 'JOUER'
    stroke(255,0,0)
    if bouton(480,height-100,220,60,'QUITTER',[255,100,100],[255,0,0]):
        clic = 'QUITTER'
# tableau des score
    textAlign(LEFT)
    rectMode(CORNER)
    fill(255)
    for i in range(len(classement)) :
        text(classement[i][0],width/2-50,height/2+i*50)# numéro
        text(classement[i][1],width/2,height/2+i*50)# prénom
        text(classement[i][2],width/2+250,height/2+i*50)# score
        text(classement[i][3],width/2+450,height/2+i*50)# niveau
    textAlign(CENTER)
    rectMode(CENTER)
# règles
    image(regles,220,height/2+30,330,400)
#logo
    image(logo,width/2,height/2-90,300,100)
    
    return clic

def ecran_pause():
    """
    Fonction qui affiche un écran de pause sur la grille de jeu.
    - boutons QUITTER et CONTINUER
    """
    global clic,image_pause
    fill(50,115,185)
    stroke(20)
    rect(width/2-150,height/2,400,400,30)
    noStroke()
    image(image_pause,width/2-100,height/3+105,200,130)
    fill(255,0,0)
    textSize(50)
    text("PAUSE",width/2-150,height/2-120,)
    if bouton(width/2-150,height/2+70,270,60,'REPRENDRE',[100,232,132],[0,232,36]):
        clic = 'REPRENDRE'
        return clic
    if bouton(width/2-150,height/2+150,270,60,'QUITTER',[242,93,93],[255,0,0]):
        exit()

def ecran_fin() :
    """
    Fonction qui affiche un écran de fin de partie.
    - Affiche le score
    - affiche le classement
    - boutons QUITTER et REJOUER
    """
    global classement,font_ecriture
    textFont(font_ecriture)
    background(0)
    clic = ''
    textSize(90)
    fill(255)
    text("GAME OVER",width/2,180)
# Boutons
    stroke(0,232,36)
    if bouton(200,height-100,220,60,'REJOUER',[100,232,132],[0,232,36]):
        clic = 'REJOUER'
    stroke(255,0,0)
    if bouton(480,height-100,220,60,'QUITTER',[255,100,100],[255,0,0]):
        clic = 'QUITTER'
# tableau des score
    textAlign(LEFT)
    fill(0)
    stroke(0)
    fill(20,0,255)
    rect(width/2,height/2+50,600,350,30)
    fill(255,255,20)
    text("tableau des scores",width/2-190,height/2-150)
    for i in range(len(classement)) :
        fill(255)
        text(classement[i][0],width/2-270,height/2-70+i*65)# numéro
        text(classement[i][1],width/2-220,height/2-70+i*65)# prénom
        text(classement[i][2],width/2+60,height/2-70+i*65)# score
        text(classement[i][3],width/2+260,height/2-70+i*65)# niveau
    textAlign(CENTER)
    rectMode(CENTER)
    noStroke()
    return clic

def ecran_record_battu():
    """
    Fonction qui affiche l'écran de record battu.
    - permet d'entrer son nom pour le sauvegarder dans le classement
    - bouton SUIVANT
    """
    global score,classement,choix_nom,font_ecriture
    background(0)
# Écritures
    textFont(font_ecriture)
    textSize(80)
    fill(255,255,0)
    text("RECORD BATTU !!", width/2, 180)
    textSize(40)
    fill(255)
    text("score : " + str(score),width/2,height/3+50)
    textSize(30)
    text("Entrez votre nom\npour enregistrer votre score",width/2,height/2)
    #text("pour enregistrer votre score.",width/2,height/2+50)
# Case pour entrer le nom
    noFill()
    stroke(255)
    rect(width/2,height/3*2,500,50,7)
    textAlign(LEFT)
    textSize(22)
    text("Nom : " ,width/2-240,height/3*2+10)
    text(choix_nom,width/2-150,height/3*2+10)
    textAlign(CENTER)
    attendre(80)
    if keyPressed :
        if key == '\x08' :
            choix_nom = choix_nom[:-1]
        else :
            choix_nom += key
# Bouton
    clic = ''
    if bouton(width-200,height-100,220,60,"SUIVANT",[100,232,132],[0,232,36]) :
        clic = 'SUIVANT'
        
    return clic
        
