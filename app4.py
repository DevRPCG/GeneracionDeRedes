from flask import Flask, render_template, request
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def create_project_network(activities):
    G = nx.DiGraph()
    for activity, predecessors in activities.items():
        for predecessor in predecessors:
            G.add_edge(predecessor, activity)
    return G

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_url = None
    if request.method == 'POST':
        activities = {}
        for i in range(1, 9):
            activity = request.form.get(f'activity{i}')
            predecessors = request.form.get(f'predecessors{i}')
            activities[activity] = predecessors.split(',') if predecessors else []
        
        G = create_project_network(activities)
        
        # Dibujar la red de proyecto
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold', arrows=True)
        
        # Guardar la imagen en un buffer
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
    
    return render_template('index.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)