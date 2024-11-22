import matplotlib.pyplot as plt

width = 60
height = 20

fig, ax = plt.subplots()

secu = bool(True)

rectangle = plt.Rectangle((0, 0), width, height, fill=None, edgecolor='black')
ax.add_patch(rectangle)

ax.set_xlim(-5, width + 5)
ax.set_ylim(-5, height + 5)
ax.set_aspect('equal')
ax.axis('off')

lettres_list = ['H', 'S', 'E', 'V', 'K', 'A', 'F', 'P', 'B', 'R', 'M', 'C', '.', '.', '.', '.', '.']
positionsAffiche = [
    (6, -1.5),  # H
    (18, -1.5), # S
    (30, -1.5), # E
    (42, -1.5), # V
    (54, -1.5), # K
    (61.5, 10), # A
    (54, 21.5), # F
    (42, 21.5), # P
    (30, 21.5), # B
    (18, 21.5), # R
    (6, 21.5),  # M
    (-1.5, 10), # C
    (30, 10),   # X
    (18, 10),   # I
    (6, 10),    # G
    (42, 10),   # L
    (54, 10)    # D
]
positionsAffichage = [
    (6, 0.5),   # H
    (18, 0.5),  # S
    (30, 0.5),  # E
    (42, 0.5),  # V
    (54, 0.5),  # K 
    (59.5, 10), # A
    (54, 19.5), # F
    (42, 19.5), # P
    (30, 19.5), # B
    (18, 19.5), # R
    (6, 19.5),  # M
    (0.5, 10),  # C
    (30, 10),   # X
    (18, 10),   # I
    (6, 10),    # G
    (42, 10),   # L
    (54, 10)    # D
]

def AffichageLettres():
    for letter, (x, y) in zip(lettres_list, positionsAffiche):
        ax.text(x, y, letter, fontsize=12, ha='center', va='center')

def doubler(secu, A, C):
    if A not in lettres_list or C not in lettres_list:
        print(f"Erreur : '{A}' ou '{C}' n'est pas dans la liste des lettres.")
        secu = False
        return secu

    if A == C:
        print("Erreur : votre point de départ est identique a votre point d'arrivé.")
        secu = False
        return secu

    depart = lettres_list.index(A)
    arrive = lettres_list.index(C)

    if depart >= len(positionsAffichage) or arrive >= len(positionsAffichage):
        print(f"Erreur : Indices hors limites pour '{A}' ou '{C}'.")
        secu = False
        return secu

    x_depart, y_depart = positionsAffichage[depart]
    x_arrive, y_arrive = positionsAffichage[arrive]

    if x_depart != x_arrive and y_depart != y_arrive:
        print(f"Erreur : '{A}' et '{C}' ne sont pas alignés correctement pour un doubler.")
        secu = False
        return secu

    ax.annotate('', xy=(x_arrive, y_arrive), xytext=(x_depart, y_depart),
                arrowprops=dict(facecolor='black', shrink=0.05, width=0.2, headwidth=8))
    return secu



AffichageLettres()
secu = doubler(True, 'A', 'C')

if secu == True:
    plt.show()