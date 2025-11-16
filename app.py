from flask import Flask, render_template, request, jsonify
from wikipedia_edges import gerar_edges
from graph_drawer import gerar_grafo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grafo', methods=['POST'])
def grafo():
    try:
        start = request.form.get('start')
        end = request.form.get('end')
        depth = int(request.form.get('depth'))
        paths_limit = int(request.form.get('paths'))

        edges = gerar_edges(start, end, depth, paths_limit)
        html_file = gerar_grafo(edges, start, end)

        return jsonify({"html_file": html_file})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("🚀 Servidor Flask iniciado...")
    app.run(debug=True)
