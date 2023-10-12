import pygame
import random

def PositionsNoeuds(n_noeuds, largeur, hauteur, rayon_noeud):
    positions_noeuds = []
    for _ in range(n_noeuds):
        while True:
            x = random.randint(rayon_noeud, largeur - rayon_noeud)
            y = random.randint(rayon_noeud, hauteur - rayon_noeud)
            position = (x, y)

            # Vérifier s'il y a une superposition avec d'autres nœuds
            superposition = False
            for other_position in positions_noeuds:
                distance = pygame.math.Vector2(position) - pygame.math.Vector2(other_position)
                if distance.length() < 2 * rayon_noeud:
                    superposition = True
                    break

            if not superposition:
                positions_noeuds.append(position)
                break
    return positions_noeuds

def PositionLiens(n_liens, n_noeuds):
    liens = []
    noeuds_liens = [0] * n_noeuds
    test = False
    for i in range(n_noeuds-1):
        x_noeud = i
        while noeuds_liens[x_noeud]==4:
            y_noeud = random.randint(0, n_noeuds-1)
        y_noeud = random.randint(0, n_noeuds-1)
        while x_noeud == y_noeud or (x_noeud, y_noeud) in liens or (y_noeud, x_noeud) in liens or noeuds_liens[y_noeud] == 4:
            y_noeud = random.randint(0, n_noeuds-1)
        if i == n_noeuds-2:
            if 0 in noeuds_liens:
                for i in range(len(noeuds_liens)):
                            if(noeuds_liens[i] == 0 and x_noeud != i and y_noeud != i and test == False):
                                x_noeud = i
                                test = True
                            elif(noeuds_liens[i] == 0 and test):
                                y_noeud = i
                                    
        lien = (x_noeud, y_noeud)
        noeuds_liens[x_noeud]+=1
        noeuds_liens[y_noeud]+=1
        liens.append(lien)
    for _ in range(n_liens-(n_noeuds-1)):
        x_noeud = random.randint(0, n_noeuds-1)
        y_noeud = random.randint(0, n_noeuds-1)
        while x_noeud == y_noeud or (x_noeud, y_noeud) in liens or (y_noeud, x_noeud) in liens or noeuds_liens[x_noeud]==4 or noeuds_liens[y_noeud]==4:
            x_noeud = random.randint(0, n_noeuds-1)
            y_noeud = random.randint(0, n_noeuds-1)
        lien = (x_noeud, y_noeud)
        noeuds_liens[x_noeud]+=1
        noeuds_liens[y_noeud]+=1
        liens.append(lien)
    return liens

def GraphiqueReseau(largeur, hauteur, positions_noeuds, position_liens, rayon_noeud):
    # Initialisation de Pygame
    pygame.init()
    # Couleurs
    blanc = (255, 255, 255)
    noir = (0, 0, 0)

    # Création de la fenêtre
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Graphique de Réseau")

    # Boucle principale
    continuer = True
    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False

        # Effacer l'écran
        fenetre.fill(blanc)

        for position in position_liens:
            pygame.draw.line(fenetre, noir, positions_noeuds[position[0]], positions_noeuds[position[1]], 2)

        # Dessiner les nœuds
        for position in positions_noeuds:
            pygame.draw.circle(fenetre, noir, position, rayon_noeud)

        pygame.display.flip()

    # Quitter Pygame
    pygame.quit()
# Main

largeur = 800
hauteur = 600
rayon_noeud = 20

n_noeuds = random.randint(3, 30)

if(n_noeuds==3):
    n_liens = random.randint((n_noeuds-1), 3)
elif(n_noeuds==4):
    n_liens = random.randint((n_noeuds-1), 6)
else:
    n_liens = random.randint((n_noeuds-1), ((n_noeuds*4)/2))

positions_noeuds = PositionsNoeuds(n_noeuds, largeur, hauteur, rayon_noeud)
position_liens = PositionLiens(n_liens, n_noeuds)
GraphiqueReseau(largeur, hauteur, positions_noeuds, position_liens, rayon_noeud)
print(position_liens)
    
