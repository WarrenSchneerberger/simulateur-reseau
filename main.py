import pygame
import random
import math
from collections import deque
import heapq

isNotRun = True
noeudA = "0"
noeudB = "0"
text_result = ""


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
    for i in range(n_noeuds - 1):
        x_noeud = i
        while noeuds_liens[x_noeud] == 4:
            y_noeud = random.randint(0, n_noeuds - 1)
        y_noeud = random.randint(0, n_noeuds - 1)
        while x_noeud == y_noeud or (x_noeud, y_noeud) in liens or (y_noeud, x_noeud) in liens or noeuds_liens[
            y_noeud] == 4:
            y_noeud = random.randint(0, n_noeuds - 1)
        if i == n_noeuds - 2:
            if 0 in noeuds_liens:
                for i in range(len(noeuds_liens)):
                    if (noeuds_liens[i] == 0 and x_noeud != i and y_noeud != i and test == False):
                        x_noeud = i
                        test = True
                    elif (noeuds_liens[i] == 0 and test):
                        y_noeud = i

        lien = (x_noeud, y_noeud)
        noeuds_liens[x_noeud] += 1
        noeuds_liens[y_noeud] += 1
        liens.append(lien)
    for _ in range(n_liens - (n_noeuds - 1)):
        x_noeud = random.randint(0, n_noeuds - 1)
        y_noeud = random.randint(0, n_noeuds - 1)
        while x_noeud == y_noeud or (x_noeud, y_noeud) in liens or (y_noeud, x_noeud) in liens or noeuds_liens[
            x_noeud] == 4 or noeuds_liens[y_noeud] == 4:
            x_noeud = random.randint(0, n_noeuds - 1)
            y_noeud = random.randint(0, n_noeuds - 1)
        lien = (x_noeud, y_noeud)
        noeuds_liens[x_noeud] += 1
        noeuds_liens[y_noeud] += 1
        liens.append(lien)
    return liens


def DrawLink(fenetre, noir, positions_noeuds, position_liens):
    for position in position_liens:
        pygame.draw.line(fenetre, noir, positions_noeuds[position[0]], positions_noeuds[position[1]], 2)


def DrawNoeud(positions_noeuds, fenetre, noir, blanc, rayon_noeud):
    for i, position in enumerate(positions_noeuds):
        pygame.draw.circle(fenetre, noir, position, rayon_noeud)
        # Afficher le numéro d'identification
        font = pygame.font.Font(None, 36)
        text = font.render(str(i), True, blanc)
        text_rect = text.get_rect()
        text_rect.center = position
        fenetre.blit(text, text_rect)


def DrawDiametre(fenetre, positions_noeuds, position_liens, noir):
    diametre = CalculerDiametre(positions_noeuds, position_liens)
    font = pygame.font.Font(None, 36)
    # Elements de l'interface
    diametre_text = pygame.Rect(200, 0, 140, 32)
    # Afficher le texte des champs de texte
    texte_diametre = font.render("Le diamètre du réseau est : " + str(diametre), True, noir)
    fenetre.blit(texte_diametre, (diametre_text.x + 5, diametre_text.y + 5))


def DrawCalDistance(fenetre, noir, click, positions_noeuds, position_liens):
    nb_noeud = len(positions_noeuds)
    font_title = pygame.font.Font(None, 30)
    font = pygame.font.Font(None, 48)
    font_40 = pygame.font.Font(None, 40)
    font_25 = pygame.font.Font(None, 25)

    input_text1 = pygame.Rect(50, 100, 32, 32)
    input_left1 = pygame.Rect(50, 130, 16, 16)
    input_right1 = pygame.Rect(66, 130, 16, 16)

    input_text2 = pygame.Rect(100, 100, 32, 32)
    input_left2 = pygame.Rect(100, 130, 16, 16)
    input_right2 = pygame.Rect(116, 130, 16, 16)

    result1_texte = pygame.Rect(150, 100, 140, 40)

    buttonAStar = pygame.Rect(50, 150, 140, 40)

    buttonDijkstra = pygame.Rect(200, 150, 140, 40)

    box = pygame.Rect(30, 30, 450, 200)
    box_border = pygame.Rect(30, 30, 450, 200)

    text1 = font_title.render("La distance optimale entre: ", True, noir)
    texte_input1 = "5"
    texte_input2 = "4"
    global noeudA
    global noeudB
    global isNotRun
    global text_result
    mx, my = pygame.mouse.get_pos()
    if input_left1.collidepoint((mx, my)):
        if click and isNotRun:
            # Réduit le numéro du Noeud A
            noeudA = Less(noeudA)
            isNotRun = False
    if input_right1.collidepoint((mx, my)):
        if click and isNotRun:
            # Augmente le numéro du Noeud A
            noeudA = More(noeudA, nb_noeud)
            isNotRun = False
    if input_left2.collidepoint((mx, my)):
        if click and isNotRun:
            # Réduit le numéro du Noeud B
            noeudB = Less(noeudB)
            isNotRun = False
    if input_right2.collidepoint((mx, my)):
        if click and isNotRun:
            # Augmente le numéro du Noeud B
            noeudB = More(noeudB, nb_noeud)
            isNotRun = False
    if buttonDijkstra.collidepoint((mx, my)):
        if click and isNotRun:
            # Calcule de la distance optimal
            distance = CalDistanceDijkstra(noeudA, noeudB, positions_noeuds, position_liens)
            if distance is not None:
                text_result = f"Algo de Dijkstra: La distance est: {distance}."
            else:
                text_result = f"Il n'y a pas de chemin entre {noeudA} et {noeudB}."
            isNotRun = False
    if buttonAStar.collidepoint((mx, my)):
        if click and isNotRun:
            # Calcule de la distance optimal
            distance = CalDistanceAStar(noeudA, noeudB, positions_noeuds, position_liens)
            if distance is not None:
                text_result = f"Algo de A*: La distance est: {distance}."
            else:
                text_result = f"Il n'y a pas de chemin entre {noeudA} et {noeudB}."
            isNotRun = False

            # Dessiner les éléments de l'interface
    pygame.draw.rect(fenetre, (255, 255, 255), box, 0)
    pygame.draw.rect(fenetre, noir, box_border, 2)
    pygame.draw.rect(fenetre, noir, input_text1, 2)
    pygame.draw.rect(fenetre, noir, input_text2, 2)
    pygame.draw.rect(fenetre, noir, input_right1, 1)
    pygame.draw.rect(fenetre, noir, input_right2, 1)
    pygame.draw.rect(fenetre, noir, input_left1, 1)
    pygame.draw.rect(fenetre, noir, input_left2, 1)
    pygame.draw.rect(fenetre, noir, buttonAStar, 1)
    pygame.draw.rect(fenetre, noir, buttonDijkstra, 1)

    fenetre.blit(text1, (50, 50))

    # Afficher le texte des champs de texte
    result1 = font_25.render(text_result, True, noir)
    texte_surface1 = font_40.render(noeudA, True, noir)
    texte_surface2 = font_40.render(noeudB, True, noir)
    more = font_40.render("+", True, noir)
    less = font_40.render("-", True, noir)
    text_buttonAStar = font_40.render("AStar", True, noir)
    text_buttonDijkstra = font_40.render("Dijkstra", True, noir)
    fenetre.blit(texte_surface1, (input_text1.x + 6, input_text1.y + 3))
    fenetre.blit(texte_surface2, (input_text2.x + 6, input_text1.y + 3))
    fenetre.blit(text_buttonAStar, (buttonAStar.x + 6, buttonAStar.y + 3))
    fenetre.blit(text_buttonDijkstra, (buttonDijkstra.x + 6, buttonDijkstra.y + 3))
    fenetre.blit(more, (input_right1.x, input_right1.y - 7))
    fenetre.blit(more, (input_right2.x, input_right2.y - 7))
    fenetre.blit(less, (input_left1.x + 3, input_left1.y - 7))
    fenetre.blit(less, (input_left2.x + 3, input_left2.y - 7))
    fenetre.blit(result1, (result1_texte.x, result1_texte.y - 7))


def More(nb, nb_noeud):
    if int(nb) == nb_noeud - 1:
        return nb
    else:
        return str(int(nb) + 1)


def Less(nb):
    if int(nb) == 0:
        return str(0)
    else:
        return str(int(nb) - 1)


def CalDistanceDijkstra(noeudA, noeudB, positions_noeuds, position_liens):
    start_node = int(noeudA)
    end_node = int(noeudB)

    # Construire le graphique à partir des positions et liens
    graph = {i: [] for i in range(len(positions_noeuds))}
    for lien in position_liens:
        graph[lien[0]].append((lien[1], 1))  # Poids des liens = 1
        graph[lien[1]].append((lien[0], 1))

    # Initialiser les distances à l'infini sauf pour le nœud de départ
    distances = {node: float('infinity') for node in graph}
    distances[start_node] = 0

    # File de priorité pour maintenir les nœuds non explorés
    priority_queue = [(0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Si on atteint le nœud de destination, retourner la distance
        if current_node == end_node:
            return current_distance

        # Parcourir les voisins du nœud actuel
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            # Mettre à jour la distance si un chemin plus court est trouvé
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    # Si on ne trouve pas de chemin, retourner None
    return None


def heuristic(node, end_node, positions_noeuds):
    # Heuristique basée sur la distance euclidienne
    x1, y1 = positions_noeuds[node]
    x2, y2 = positions_noeuds[end_node]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def CalDistanceAStar(noeudA, noeudB, positions_noeuds, position_liens):
    start_node = int(noeudA)
    end_node = int(noeudB)

    # Construire le graphique à partir des positions et liens
    graph = {i: [] for i in range(len(positions_noeuds))}
    for lien in position_liens:
        graph[lien[0]].append((lien[1], 1))  # Poids des liens = 1
        graph[lien[1]].append((lien[0], 1))

    # File de priorité pour maintenir les nœuds non explorés
    priority_queue = [(0 + heuristic(start_node, end_node, positions_noeuds), 0, start_node)]
    visited = set()

    while priority_queue:
        current_total_cost, current_cost, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == end_node:
            return current_cost

        for neighbor, weight in graph[current_node]:
            if neighbor not in visited:
                priority = current_cost + weight + heuristic(neighbor, end_node, positions_noeuds)
                heapq.heappush(priority_queue, (priority, current_cost + weight, neighbor))

    # Si on ne trouve pas de chemin, retourner None
    return None


def GraphiqueReseau(largeur, hauteur, positions_noeuds, position_liens, rayon_noeud):
    # Initialisation de Pygame
    pygame.init()

    # Couleurs
    blanc = (255, 255, 255)
    noir = (0, 0, 0)

    # Création de la fenêtre
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Graphique de Réseau")

    # Création de la surface de texte pour le message
    font_message = pygame.font.Font(None, 24)
    message_surface = font_message.render(
        'Appuyez sur "ESPACE" pour les algorithmes & "Entrée" pour les formes canoniques', True, noir)
    message_rect = message_surface.get_rect()
    message_rect.centerx = largeur // 2
    message_rect.bottom = hauteur


    # Variables pour le déplacement des nœuds
    dragging = False
    dragged_node = None

    # Variable pour déclencher DrawOptionMenu
    draw_option_menu = False

    draw_topology = False

    # Variable pour savoir si je click ou non
    click = False

    # Boucle principale
    continuer = True
    while continuer:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    click = True
                    for i, position in enumerate(positions_noeuds):
                        if math.dist(event.pos, position) <= rayon_noeud:
                            dragging = True
                            dragged_node = i
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    global isNotRun
                    isNotRun = True
                    click = False
                    dragging = False
                    dragged_node = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    draw_option_menu = not draw_option_menu  # Inverser l'état
                elif event.key == pygame.K_RETURN:  # Touche "Entrée"
                    draw_topology = not draw_topology

        if dragging and dragged_node is not None:
            # Mettre à jour la position du nœud en fonction de la position de la souris
            positions_noeuds[dragged_node] = pygame.mouse.get_pos()

        # Effacer l'écran
        fenetre.fill(blanc)

        # Dessiner les liens
        DrawLink(fenetre, noir, positions_noeuds, position_liens)

        # Dessiner les nœuds avec un numéro d'identification
        DrawNoeud(positions_noeuds, fenetre, noir, blanc, rayon_noeud)

        # Dessiner le diamètre du réseau
        DrawDiametre(fenetre, positions_noeuds, position_liens, noir)

        # Dessiner le menu d'options si la variable est True
        if draw_option_menu:
            DrawCalDistance(fenetre, noir, click, positions_noeuds, position_liens)
        if draw_topology:
            colorier_formes_topologiques(fenetre, positions_noeuds, position_liens, noir)

        # Dessiner la surface de texte du message en bas de la fenêtre
        fenetre.blit(message_surface, message_rect)

        pygame.display.flip()
        
    # Dessiner la surface de texte du message en bas de la fenêtre
    fenetre.blit(message_surface, message_rect)
    # Quitter Pygame
    pygame.quit()


def distanceMax(graph, start):
    visited = [False] * len(graph)
    distances = [0] * len(graph)

    queue = deque([(start, 0)])
    visited[start] = True

    while queue:
        current, current_distance = queue.popleft()

        for neighbor in graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append((neighbor, current_distance + 1))
                distances[neighbor] = current_distance + 1

    return max(distances)


def CalculerDiametre(positions_noeuds, position_liens):
    graph = {i: [] for i in range(len(positions_noeuds))}

    for lien in position_liens:
        graph[lien[0]].append(lien[1])
        graph[lien[1]].append(lien[0])

    diametre = 0

    for start in range(len(positions_noeuds)):
        max_distance = distanceMax(graph, start)

        if max_distance > diametre:
            diametre = max_distance

    return diametre

def detecter_formes_topologiques(position_liens):
    graph = {}
    for lien in position_liens:
        if lien[0] not in graph:
            graph[lien[0]] = []
        if lien[1] not in graph:
            graph[lien[1]] = []
        graph[lien[0]].append(lien[1])
        graph[lien[1]].append(lien[0])
    return graph

def colorier_formes_topologiques(fenetre, positions_noeuds, position_liens, noir):
    graph = detecter_formes_topologiques(position_liens)
    visited = set()
    couleur_cycle = (255, 0, 0)  # Couleur pour les cycles

    for node in graph:
        if node not in visited:
            cycle = detecter_cycle(graph, node, visited, None)
            if cycle:
                # Dessiner des lignes colorées entre les nœuds du cycle
                for i in range(len(cycle) - 1):
                    start_node = cycle[i]
                    end_node = cycle[i + 1]
                    pygame.draw.line(fenetre, couleur_cycle, positions_noeuds[start_node], positions_noeuds[end_node], 2)

                # Rejoindre le dernier nœud avec le premier pour fermer le cycle
                pygame.draw.line(fenetre, couleur_cycle, positions_noeuds[cycle[-1]], positions_noeuds[cycle[0]], 2)

    pygame.display.flip()


def detecter_cycle(graph, node, visited, parent):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            cycle = detecter_cycle(graph, neighbor, visited, node)
            if cycle:
                return cycle
        elif parent is not None and neighbor != parent:
            return [neighbor, node, neighbor]
    return None


# Main
largeur = 1000
hauteur = 800
rayon_noeud = 20
n_noeuds = random.randint(3, 30)
if (n_noeuds == 3):
    n_liens = random.randint((n_noeuds - 1), 3)
elif (n_noeuds == 4):
    n_liens = random.randint((n_noeuds - 1), 6)
else:
    n_liens = random.randint((n_noeuds - 1), ((n_noeuds * 4) / 2))
positions_noeuds = PositionsNoeuds(n_noeuds, largeur, hauteur, rayon_noeud)
position_liens = PositionLiens(n_liens, n_noeuds)

GraphiqueReseau(largeur, hauteur, positions_noeuds, position_liens, rayon_noeud)
