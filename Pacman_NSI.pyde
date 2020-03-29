#                                     Le Pacman 
#                        de Julien Goetghebeur et Evan Guyomarch
#
#  version 1.0   -->  jeu basique

from random import choice


TAILLE_GRILLE = (84,90)
TAILLE_CASE = 9

with open("classement1.csv","r") as fichier :
    classement = []
    for ligne in fichier :
        l = ligne.split(';')
        l[0] = l[0].strip('\xef\xbb\xbf')
        l[-1] = l[-1].strip('\n\r')
        classement.append(l)
with open("grille.csv", "r") as file :
    plateau = []
    for ligne in file :
        l = ligne.split(';')
        for i in range(len(l)):
            l[i]=l[i].strip("\r\n")
        plateau.append(l)

affichage = 'record battu'
clic = ''

le_plus_fort = 'fantome'
score = 0
grille = plateau
chrono = 0
direction_possible = ["haut", "bas", "droite", "gauche"]
dir_poids = [1,1,1,1]
nb_fantomes_mange = 0
nb_pieces_mange = 0
nb_pastilles_mange = 0


def setup():
    global image_pacman,image_blinky,image_pinky,image_inky,image_clyde,image_fantomePeur,Pacman,Blinky,Pinky,Inky,Clyde,fantomes
    size(TAILLE_GRILLE[0]*TAILLE_CASE+300,TAILLE_GRILLE[1]*TAILLE_CASE)
    frameRate(10)
    background(255)
    rectMode(CENTER)
    textAlign(CENTER)
    imageMode(CENTER)
    noStroke()
    
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
    global affichage,grille
    
    if affichage == 'accueil' :
        clic = ecran_titre()
        if clic == 'JOUER':
            affichage = 'jeu'
        elif clic == 'QUITTER':
            exit()
            
    elif affichage == 'jeu':
        if Pacman["vivant"] :
            if la_grille_est_vide(grille) :
                affichage = 'terminer'
            else :
                jeu()
        else :
            if score > classement[4][2] :
                affichage == 'record battu'
            else : 
                affichage = 'gameover'
    
    elif affichage == 'record battu':
        clic = ecran_record_battu()
        if clic == 'SUIVANT':
            record_battu()
            affichage = 'gameover'
            
    elif affichage == 'gameover':
        clic = ecran_fin()
        if clic == 'REJOUER':
            affichage = 'jeu'
            init()
            score = 0
            nb_fantomes_mange = 0
            nb_pieces_mange = 0
            nb_pastilles_mange = 0
        elif clic == 'QUITTER':
            exit()
    
    elif affichage == 'pause':
        clic = ecran_pause()
        if clic == 'REPRENDRE' :
            affichage = 'jeu'
    
    elif affichage == 'terminer'   :
        affichage = 'jeu'
        init()


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
    

# def attendre() :
#     temps1 = millis()
#     while (millis() < temps1 + 200) :
#         pass    

def la_grille_est_vide(grille) :
    for i in range(len(grille)) :
        for j in grille[i]:
            if j == "1" or j == "5" :
                return False
    else :
        return True
        
def init() :
    global le_plus_fort,score,pacman_a_gagner,chrono,nb_fantomes_mange, nb_pieces_mange,nb_pastilles_mange,pacman_est_vivant,Pacman,Blinky,Pinky,Inky,Clyde
    le_plus_fort = "fantome"
    chrono = 0
    
    pacman_est_vivant = True
    Pacman["x"] = 43
    Pacman["y"] = 67
    Blinky["x"] = 40
    Blinky["y"] = 40 
    Pinky["x"] = 43
    Pinky["y"] = 40
    Inky["x"] = 40
    Inky["y"] = 43
    Clyde["x"] = 43
    Clyde["y"] = 43
    grille = plateau

def record_battu():
    global score,nom,classement
    for i in classment :
        if score > i[2] :
            rang = i[0]
    classement[rang-1][1] = nom
    classement[rang-1][2] = score

# faire les écrans ( mort/record battu/pause)

# faire avancer les fantomes  /  detecter un carrefour puis choisir une direction avec probabilité plus élever d'aller vers le pacman --> calculer le vecteur  JULIEN

# faire le classement et les scores --> presque fini il manque un ecran de record battu ou on peut rentrer son nom pour le sauvgarder dans le classement --> a prendre sur mon snake JULIEN

# faire un sorte de "hitbox" pour les perso pour ameliorer collision()  EVAN



#####################################PERSONNAGES#######################################################################################################################################################

def collision(pacman,fantome) :
    global le_plus_fort,score,nb_fantomes_mange
    if le_plus_fort == "fantome" :
        pacman["vie"] -= 1
        if pacman["vie"] == 0 :
            pacman["vivant"] = False
         
    elif le_plus_fort == "pacman" :
        fantome["vivant"] = False
        fantome_respawn(fantome)
        score += 200
        nb_fantomes_mange += 1

def avancer_personnage(perso) :
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
    if grille[perso["y"]-2][perso["x"]-1] ==  "10" or grille[perso["y"]-2][perso["x"]] ==  "10" or grille[perso["y"]-2][perso["x"]+1] ==  "10" :
        return True
    else :
        return False

def est_bloque_right(perso):
    if grille[perso["y"]-1][perso["x"]+2] ==  "10" or grille[perso["y"]][perso["x"]+2] ==  "10" or grille[perso["y"]+1][perso["x"]+2] ==  "10" :
        return True
    else :
        return False

def est_bloque_left(perso):
    if grille[perso["y"]-1][perso["x"]-2] ==  "10" or grille[perso["y"]][perso["x"]-2] ==  "10" or grille[perso["y"]+1][perso["x"]-2] ==  "10":
        return True
    else :
        return False

def est_bloque_down(perso):
    if grille[perso["y"]+2][perso["x"]-1] ==  "10" or grille[perso["y"]+2][perso["x"]] ==  "10" or grille[perso["y"]+2][perso["x"]+1] ==  "10" :
        return True
    else :
        return False

def passe_tunel(perso):
    if grille[perso["y"]][perso["x"]] == "2":
        return True
    else : 
        return False

#######PACMAN######

def choix_direction():  
    global Pacman
    if keyPressed :
        if key == CODED:
            Pacman["vitesse"] = 1
            if keyCode == RIGHT:
                if est_bloque_right(Pacman) == False :
                    Pacman["direction"] = "droite"
                    Pacman["image"] = loadImage("pacmandroite.gif")
            elif keyCode == LEFT :
                if est_bloque_left(Pacman) == False :
                    Pacman["direction"] = "gauche"
                    Pacman["image"] = loadImage("pacmangauche.gif")
            elif keyCode == UP :
                if est_bloque_up(Pacman) == False :
                    Pacman["direction"] = "haut"
                    Pacman["image"] = loadImage("pacmanhaut.gif")
            elif keyCode == DOWN :
                if est_bloque_down(Pacman) == False :
                    Pacman["direction"] = "bas"
                    Pacman["image"] = loadImage("pacmanbas.gif")

def case_occupe() : 
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

    elif grille[Pacman["y"]][Pacman["x"]] == "0":
        pass

def pastille_mange() : 
    global le_plus_fort,Pacman,fantomes,chrono
    le_plus_fort = "pacman"
    for i in fantomes :
        i["image"] = image_fantomePeur
    #     i["vitesse"] = 0.5                
    # Pacman["vitesse"] = 1.5
    chrono = millis()

########FANTOMES#########

def retour_a_la_normale():
    global le_plus_fort 
    le_plus_fort = "fantome"
    Blinky["image"] = image_blinky
    Pinky["image"] = image_pinky
    Inky["image"] = image_inky
    Clyde["image"] = image_clyde

def deplacement_fantomes():
    global fantomes,dir_poids,direction_possible
    for f in fantomes :
        direction_possible = ["haut", "bas", "droite", "gauche"]
        est_sur_carrefour = False
        
        if f["direction"] == "droite" or f["direction"] == "gauche" :
            if est_bloque_up(f) == False or est_bloque_down(f) == False:
                est_sur_carrefour = True
        else : 
            if est_bloque_right(f) == False or est_bloque_left(f) == False :
                est_sur_carrefour = True
        
        if est_sur_carrefour == True :
            vers_pacman = (Pacman["x"] - f["x"],Pacman["y"] - f["y"])
            # dir_poids = [1,1,1,1]
            if vers_pacman[0] > 0 :
                if vers_pacman[0] < 20 or vers_pacman[1] < 20 :
                    # dir_poids[2] += 2
                    direction_possible.append("droite")
                elif vers_pacman[0] < 10 or vers_pacman[1] < 10 :
                    direction_possible.append("droite")
                    direction_possible.append("droite")
            elif vers_pacman[0] < 0 :
                if vers_pacman[0] < 20 or vers_pacman[1] < 20 :
                    # dir_poids[3] += 2
                    direction_possible.append("gauche")
                elif vers_pacman[0] < 10 or vers_pacman[1] < 10 :
                    direction_possible.append("gauche")
                    direction_possible.append("gauche")
            if vers_pacman[1] > 0 :
                if vers_pacman[0] < 20 or vers_pacman[1] < 20 :
                    # dir_poids[1] += 2
                    direction_possible.append("bas")
                elif vers_pacman[0] < 10 or vers_pacman[1] < 10 :
                    direction_possible.append("bas")
                    direction_possible.append("bas")
            elif vers_pacman[1] < 0 :
                if vers_pacman[0] < 20 or vers_pacman[1] < 20 :
                    # dir_poids[0] += 2
                    direction_possible.append("haut")
                elif vers_pacman[0] < 10 or vers_pacman[1] < 10 :
                    direction_possible.append("haut")
                    direction_possible.append("haut")
                    
            f["direction"] = choice(direction_possible)    
            # f["direction"] = choices(direction_possible, weights = dir_poids, k= 1)
        while est_bloque_front(f):
            # f["direction"] = choices(direction_possible, weights = dir_poids, k= 1)
            f["direction"] = choice(direction_possible)
            
        avancer_personnage(f)

def fantome_respawn(fant) :
    fant["x"] = 40
    fant["y"] = 40
    fant["vivant"] = True



#####################################INTERFACE##GRAPHIQUE##################################################################################################################################################

def afficher_grille(grille):
    """
    Fonction qui affiche la grille et les personnages.
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
                
    for coord in pastille :
        afficher_pastille(coord[0],coord[1]) # pour que les pastilles s'affiche en dernier pour pas etre recouvert par les autres cases
    
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
    Affiche un carré bleu avec un rond bleu dessus pour représenter un couloir avec une pièce.
    """
    afficher_couloir(x,y)
    noStroke()
    fill(255)
    circle(x*TAILLE_CASE+TAILLE_CASE/2,y*TAILLE_CASE+TAILLE_CASE/2,9)

def afficher_pastille(x,y):
    """
    Affiche un carré bleu avec un rand orange pour représenter un couloir avec une pastille.
    """
    afficher_couloir(x,y)
    noStroke()
    fill(255,130,0)
    circle(x*TAILLE_CASE+TAILLE_CASE/2,y*TAILLE_CASE+TAILLE_CASE/2,15)

def afficher_pacman(p):
    """
    Affiche l'image pacman (ou rond jaune).
    """
    image(p["image"],p["x"]*TAILLE_CASE+TAILLE_CASE/2,p["y"]*TAILLE_CASE+TAILLE_CASE/2)
    # fill(255,255,0)
    # circle(p["x"]*TAILLE_CASE+TAILLE_CASE/2,p["y"]*TAILLE_CASE+TAILLE_CASE/2,22)

def afficher_fantomes(f):
    """
    Affiche l'image correspondante a chaque fantôme (ou rond rouge).
    """
    for i in f :
        image(i["image"],i["x"]*TAILLE_CASE+TAILLE_CASE/2,i["y"]*TAILLE_CASE+TAILLE_CASE/2)
        # fill(255,0,0)
        # circle(i["x"]*TAILLE_CASE+TAILLE_CASE/2,i["y"]*TAILLE_CASE+TAILLE_CASE/2,22)

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
    global score,classement
    textAlign(LEFT)
    clic = ''
    fill(255)
    textSize(32)
    text("score : "+ str(score) ,TAILLE_GRILLE[0]*TAILLE_CASE,50)
    # details des scores : nombres de piece , de pastille, et de fantomes mangé + nb de vies restantes + niveaux
    compteur_image = loadImage("compteur.png")
    image(compteur_image,TAILLE_GRILLE[0]*TAILLE_CASE+150,height/3+100,300,400)
    textSize(24)
    text(str(nb_pastilles_mange),TAILLE_GRILLE[0]*TAILLE_CASE+125,height/3-47)
    text(str(nb_pieces_mange),TAILLE_GRILLE[0]*TAILLE_CASE+125,height/3-7)
    text(str(nb_fantomes_mange),TAILLE_GRILLE[0]*TAILLE_CASE+125,height/3+33)
    regles2 = loadImage("regle-pacman3.png")
    image(regles2,TAILLE_GRILLE[0]*TAILLE_CASE+150,width/2+50,300,400)
    textAlign(CENTER)
    if bouton(TAILLE_GRILLE[0]*TAILLE_CASE+150,height-145,250,50,"PAUSE",[100,100,255],[0,0,255]):
        clic = 'PAUSE'
    if bouton(TAILLE_GRILLE[0]*TAILLE_CASE+150,height-75,250,50,"QUITTER",[255,100,100],[255,0,0]):
        clic = 'QUITTER'
    return clic

def ecran_titre():#    a ajouter :  fond  /  police 
    global classement
    """
    Affiche l'écran d'accueil du jeu.
    -Propose de jouer ou de quitter
    -Affiche le classement des scores 
    -affiche les règles
    """
    background(0)
    clic = ''
    font = createFont("PAC-FONT.TTF",48)
    textFont(font)
    textSize(90)
    fill(255,255,0)
    text("pac-man",width/2,180)
    font = loadFont("04b30-48.vlw")
    textFont(font)
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
    # fill(222,204,68)
    fill(255)
    for i in range(len(classement)) :
        text(classement[i][0],width/2-50,height/2+i*50)# numéro
        text(classement[i][1],width/2,height/2+i*50)# prénom
        text(classement[i][2],width/2+250,height/2+i*50)# score
        text(classement[i][3],width/2+400,height/2+i*50)# niveau
# règles
    regles = loadImage("regle-pacman2.png")
    image(regles,220,height/2+30,330,400)
#logo
    logo = loadImage("pacman-logo.jpg")
    image(logo,width/2,height/2-90,300,100)
    
    textAlign(CENTER)
    rectMode(CENTER)
     
    return clic

def ecran_pause():
    fill(255,0,0)
    text("PAUSE",width/2,height/2)

def ecran_fin() :
    """
    Affiche l'écran d'accueil du jeu.
    -Propose de jouer ou de quitter
    -Affiche le classement des scores 
    -affiche les règles
    """
    background(0)
    clic = ''
    textSize(90)
    fill(255)
    text("GAME OVER",width/2,180)
# Boutons
    stroke(0,232,36)
    if bouton(200,height-130,220,60,'REJOUER',[100,232,132],[0,232,36]) ==True:
        clic = 'REJOUER'
    stroke(255,0,0)
    if bouton(800,height-130,220,60,'QUITTER',[255,100,100],[255,0,0]) == True :
        clic = 'QUITTER'
# tableau des score
    textAlign(LEFT)
    rectMode(CORNER)
    
    fill(0)
    stroke(0)
    fill(20,0,255)
    rect(width/3-50,height/3,500,350,30)
    fill(255,255,20)
    text("tableau des scores",width/2-190,height/2-150)
    
    fill(255)
    for i in range(len(classement)) :
        text(classement[i][0],width/2-50,height/2+i*50)# numéro
        text(classement[i][1],width/2,height/2+i*50)# prénom
        text(classement[i][2],width/2+250,height/2+i*50)# score
        text(classement[i][3],width/2+400,height/2+i*50)# niveau
    
    textAlign(CENTER)
    rectMode(CENTER)
    noStroke()

    return clic

def ecran_record_battu():
    global score,classement
    background(0)
    font = loadFont("04b30-48.vlw")
    textFont(font)
    textSize(80)
    fill(255,255,0)
    text("RECORD BATTU !!", width/2, 180)
    textSize(30)
    fill(255)
    text("Bravo ! Vous avez battu un score ",width/2,height/2-50)
    text("du classement. Entrez votre nom",width/2,height/2)
    text("pour enregistrer votre score.",width/2,height/2+50)
    noFill()
    stroke(255)
    rect(width/2,height/3*2,500,50,7)
    textAlign(LEFT)
    textSize(22)
    text("Nom : " ,width/2-240,height/3*2+10)
    textAlign(CENTER)
    
    
    clic = ''
    if bouton(width-200,height-100,220,60,"SUIVANT",[100,232,132],[0,232,36]) :
        clic = 'SUIVANT'
    return clic
        
