from flask import Flask, render_template, request, send_from_directory
from marvel_graph import gerar_grafo
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grafo', methods=['POST'])
def grafo():
    personagem = request.form.get('personagem')
    arquivo = gerar_grafo(personagem)
    return send_from_directory('static', os.path.basename(arquivo), as_attachment=False)

if __name__ == '__main__':
    print("🚀 Servidor Flask iniciando...")
    app.run(debug=True)
