import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
largeur = 800
hauteur = 600

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Graphique de Réseau")

# Nombre de nœuds
n = random.randint(3, 30)
if(n==3):
    n_liens = random.randint((n-1), 3)
elif(n==4):
    n_liens = random.randint((n-1), 6)
else:
    n_liens = random.randint((n-1), ((n*4)/2))

print("n Liens :")
print(n_liens)
# Liste pour stocker les positions des nœuds
positions_noeuds = []
liens = []
noeuds_liens = [0] * n
test = False
for i in range(n-1):
    x_noeud = i
    while noeuds_liens[x_noeud]==4:
        y_noeud = random.randint(0, n-1)
    y_noeud = random.randint(0, n-1)
    while x_noeud == y_noeud or (x_noeud, y_noeud) in liens or (y_noeud, x_noeud) in liens or noeuds_liens[y_noeud] == 4:
        y_noeud = random.randint(0, n-1)
    if i == n-2:
        if 0 in noeuds_liens:
            print("oui")
            for i in range(len(noeuds_liens)):
                        if(noeuds_liens[i] == 0 and x_noeud != i and y_noeud != i and test == False):
                            x_noeud = i
                            test = True
                        elif(noeuds_liens[i] == 0 and test):
                            y_noeud = i
                                
    lien = (x_noeud, y_noeud)
    print(str(lien)+" "+str(noeuds_liens))
    noeuds_liens[x_noeud]+=1
    noeuds_liens[y_noeud]+=1
    print(noeuds_liens)
    liens.append(lien)
for _ in range(n_liens-(n-1)):
    x_noeud = random.randint(0, n-1)
    y_noeud = random.randint(0, n-1)
    while x_noeud == y_noeud or (x_noeud, y_noeud) in liens or (y_noeud, x_noeud) in liens or noeuds_liens[x_noeud]==4 or noeuds_liens[y_noeud]==4:
        x_noeud = random.randint(0, n-1)
        y_noeud = random.randint(0, n-1)
    lien = (x_noeud, y_noeud)
    noeuds_liens[x_noeud]+=1
    noeuds_liens[y_noeud]+=1
    liens.append(lien)

# Générer des positions aléatoires pour les nœuds sans superposition
rayon_noeud = 20
for _ in range(n):
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

# Boucle principale
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    # Effacer l'écran
    fenetre.fill(blanc)

    for lien in liens:
        pygame.draw.line(fenetre, noir, positions_noeuds[lien[0]], positions_noeuds[lien[1]], 2)

    # Dessiner les nœuds
    for position in positions_noeuds:
        pygame.draw.circle(fenetre, noir, position, rayon_noeud)

    pygame.display.flip()

# Quitter Pygame
pygame.quit()
