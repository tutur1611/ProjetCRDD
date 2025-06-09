from flask import Flask, request, send_file, jsonify
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from io import BytesIO

app = Flask(__name__)

width = 60
height = 20
lettres_list = ['H', 'S', 'E', 'V', 'K', 'A', 'F', 'P', 'B', 'R', 'M', 'C']
positionsFigures = [
    (6, 0.5), (18, 0.5), (30, 0.5), (42, 0.5), (54, 0.5),  
    (59.5, 10),  
    (54, 20.5), (42, 20.5), (30, 20.5), (18, 20.5), (6, 20.5),  
    (0.5, 10)  
]

def generate_graph(figures):
    fig, ax = plt.subplots()
    rectangle = plt.Rectangle((0, 0), width, height, fill=None, edgecolor='black')
    ax.add_patch(rectangle)
    ax.set_xlim(-5, width + 5)
    ax.set_ylim(-5, 25)  
    ax.set_aspect('equal')

    for letter, (x, y) in zip(lettres_list, positionsFigures):
        if x == 0.5:  
            ax.text(x - 2, y, letter, fontsize=12, ha='center', va='center')
        elif x == width + 0.5:  
            ax.text(x + 2, y, letter, fontsize=12, ha='center', va='center')
        elif y == 0.5:  
            ax.text(x, y - 2, letter, fontsize=12, ha='center', va='center')
        elif y == 20.5: 
            ax.text(x, y + 1, letter, fontsize=12, ha='center', va='center')  

    for figure in figures:
        figure_type = figure['type']
        start = figure['start']
        end = figure.get('end', None)

        if figure_type == "Doubler":
            draw_doubler(ax, start, end)
        elif figure_type == "Diagonale":
            draw_diagonale(ax, start, end)
        elif figure_type == "Volte":
            draw_volte(ax, start)
        elif figure_type == "Cercle":
            draw_cercle(ax, start)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf

def draw_doubler(ax, A, C):
    if A in lettres_list and C in lettres_list:
        start_idx = lettres_list.index(A)
        end_idx = lettres_list.index(C)
        x_start, y_start = positionsFigures[start_idx]
        x_end, y_end = positionsFigures[end_idx]
        ax.annotate('', xy=(x_end, y_end), xytext=(x_start, y_start),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=0.2, headwidth=8))

def draw_diagonale(ax, A, C):
    if A in lettres_list and C in lettres_list:
        start_idx = lettres_list.index(A)
        end_idx = lettres_list.index(C)
        x_start, y_start = positionsFigures[start_idx]
        x_end, y_end = positionsFigures[end_idx]
        ax.annotate('', xy=(x_end, y_end), xytext=(x_start, y_start),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=0.2, headwidth=8))

def draw_cercle(ax, A):
    if A in lettres_list:
        idx = lettres_list.index(A)
        x, y = positionsFigures[idx]
        y = 10
        if A == 'C':
            x = 10
        if A == 'A':
            x = 50
        radius = 19 / 2
        circle = Circle((x, y), radius, fill=False, edgecolor='blue', linewidth=1.5)
        ax.add_patch(circle)

def draw_volte(ax, A):
    if A in lettres_list:
        idx = lettres_list.index(A)
        x, y = positionsFigures[idx]
        if A in ['H', 'S', 'E', 'V', 'K']:
            y = 5  
        if A in ['M','R','B','P','F']:
            y = 15
        if A == 'C':
            x = 5
        if A == 'A':
            x = 55
        radius = 9 / 2
        circle = Circle((x, y), radius, fill=False, edgecolor='black', linewidth=1.5)
        ax.add_patch(circle)

@app.route('/generate_graph', methods=['POST'])
def generate_graph_route():
    data = request.json
    figures = data.get('figures', [])
    buf = generate_graph(figures)
    return send_file(buf, mimetype='image/png')