from flask import Flask, render_template, request, send_file
from wikipedia_edges import gerar_edges
from graph_drawer import gerar_grafo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grafo', methods=['POST'])
def grafo():
    try:
        # Captura dos campos do formulário
        start = request.form.get('start')
        end = request.form.get('end')
        depth = int(request.form.get('depth'))
        paths_limit = int(request.form.get('paths'))

        # 1) Gera os edges (NÃO salva nada)
        edges = gerar_edges(start, end, depth, paths_limit)

        print("Edges recebidos:", edges)

        # 2) Gera o grafo e retorna o caminho do HTML
        html_file = gerar_grafo(edges, start, end)

        print("Arquivo gerado:", html_file)

        # 3) Envia o arquivo final
        return send_file(html_file)

    except Exception as e:
        return f"Erro ao gerar grafo: {e}", 500


if __name__ == '__main__':
    print("🚀 Servidor Flask iniciado...")
    app.run(debug=True)
