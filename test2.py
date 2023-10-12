import pygame

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

# Définition des nœuds
noeuds = [(200, 300), (400, 100), (600, 300), (400, 500)]

# Définition des liens (en spécifiant les indices des nœuds connectés)
liens = [(0, 1), (1, 2), (3, 1)]

# Création d'une liste de liens pour chaque nœud
liens_noeuds = [[] for _ in range(len(noeuds))]

# Remplir les listes de liens pour chaque nœud
for lien in liens:
    noeud1, noeud2 = lien
    liens_noeuds[noeud1].append(noeud2)
    liens_noeuds[noeud2].append(noeud1)

# Boucle principale
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    # Effacer l'écran
    fenetre.fill(blanc)

    # Dessiner les liens
    for lien in liens:
        pygame.draw.line(fenetre, noir, noeuds[lien[0]], noeuds[lien[1]], 2)

    # Dessiner les nœuds
    rayon_noeud = 20
    for i, noeud in enumerate(noeuds):
        pygame.draw.circle(fenetre, noir, noeud, rayon_noeud)

        # Dessiner des liens supplémentaires depuis ce nœud
        for j in liens_noeuds[i]:
            pygame.draw.line(fenetre, noir, noeud, noeuds[j], 2)

    pygame.display.flip()

# Quitter Pygame
pygame.quit()
