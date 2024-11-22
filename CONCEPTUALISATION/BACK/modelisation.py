import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from enum import Enum

width = 60
height = 20

main = "droite"

fig, ax = plt.subplots()

secu = bool(True)

rectangle = plt.Rectangle((0, 0), width, height, fill=None, edgecolor='black')
ax.add_patch(rectangle)

ax.set_xlim(-5, width + 5)
ax.set_ylim(-5, height + 5)
ax.set_aspect('equal')
# ax.axis('off')

diagonales_Gauche = ["HF", "HP", "BH", "HR", "FH", "FS", "FE", "FV", "PE", "PS", "PH", "BS", "BH", "RH", "SB", "SP", "SF", "EP", "EF"]
diagonales_Droite = ["MK", "MV", "ME", "MS", "RE", "RV", "RK", "BV", "BK", "PK", "KM", "KR", "KB", "KP", "VM", "VR", "VB", "ER", "EM", "SM"]
lettres_list = ['H', 'S', 'E', 'V', 'K', 'A', 'F', 'P', 'B', 'R', 'M', 'C', '.', '.', '.', '.', '.']
cooPetiteVolte = [
                  (6 ,5.5),   # H
                  (18, 5.5),  # S
                  (30, 5.5),  # E
                  (42, 5.5),  # V
                  (54, 5.5),  # K
                  (54.5, 10), # A
                  (54, 14.5), # F
                  (42, 14.5), # P
                  (30, 14.5), # B
                  (18, 14.5), # R
                  (6, 14.5),  # M
                  (5.5, 10),  # C
                   ]
positionsLettres = [
    (6, -1.5),    # H
    (18, -1.5),   # S
    (30, -1.5),   # E
    (42, -1.5),   # V
    (54, -1.5),   # K
    (61.5, 10),   # A
    (54, 21.5),   # F
    (42, 21.5),   # P
    (30, 21.5),   # B
    (18, 21.5),   # R
    (6, 21.5),    # M
    (-1.5, 10),   # C
    (30, 10.5),   # X
    (18, 10.5),   # I
    (6, 10.5),    # G
    (42, 10.5),   # L
    (54, 10.5)    # D
]
positionsFigures = [
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
    for letter, (x, y) in zip(lettres_list, positionsLettres):
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

    if depart >= len(positionsFigures) or arrive >= len(positionsFigures):
        print(f"Erreur : Indices hors limites pour '{A}' ou '{C}'.")
        secu = False
        return secu

    x_depart, y_depart = positionsFigures[depart]
    x_arrive, y_arrive = positionsFigures[arrive]

    if x_depart != x_arrive and y_depart != y_arrive:
        print(f"Erreur : '{A}' et '{C}' ne sont pas alignés correctement pour un doubler.")
        secu = False
        return secu

    ax.annotate('', xy=(x_arrive, y_arrive), xytext=(x_depart, y_depart),arrowprops=dict(facecolor='black', shrink=0.05, width=0.2, headwidth=8))
    return secu

def diagonale(secu, A, C, main):
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
    ValeurDepart = lettres_list[depart]
    ValeurArrive = lettres_list[arrive]
    combinaison = ValeurDepart + ValeurArrive
    
    if main == "gauche" or main == "droite":
        if main == "gauche":
            if combinaison not in diagonales_Gauche:
                print("Erreur : Cette diagonale n'est pas possible")
                return
        elif main == "droite":
            if combinaison not in diagonales_Droite:
                print("Erreur : Cette diagonale n'est pas possible")
                return
        depart = lettres_list.index(A)
        arrive = lettres_list.index(C)
        x_depart, y_depart = positionsFigures[depart]
        x_arrive, y_arrive = positionsFigures[arrive]
        ax.annotate('', xy=(x_arrive, y_arrive), xytext=(x_depart, y_depart), arrowprops=dict(facecolor = 'black', shrink=0.05, width=0.2, headwidth=8))
        secu = True
        return secu
    else:
        secu = False
        input(print("veuillez indiquer a quel main vous êtes ==> "))
        return
    
def PetiteVolte(secu, A):
    if A not in lettres_list:
        print(f"Erreur : '{A}' n'est pas dans la liste des lettres.")
        secu = False
        return secu

    depart = lettres_list.index(A)
    x_depart, y_depart = cooPetiteVolte[depart]

    cercle = Circle((x_depart, y_depart), 5, fill=False, edgecolor='black')
    ax.add_patch(cercle)
    secu = True
    return secu

AffichageLettres()
secu = doubler(True, 'A', 'C')
secu = diagonale(True, 'K', 'M', main)
secu = PetiteVolte(secu, 'C')

if secu == True:
    plt.show()