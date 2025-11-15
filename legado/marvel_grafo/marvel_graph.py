import pandas as pd 
import networkx as nx
from itertools import combinations
from pyvis.network import Network
import kagglehub
import os
import json

def gerar_grafo(personagem):
    print("🔽 Baixando dataset do Kaggle...")
    path = kagglehub.dataset_download("csanhueza/the-marvel-universe-social-network")
    print("📂 Dataset baixado em:", path)

    # Arquivos
    edges_path = os.path.join(path, "edges.csv")
    nodes_path = os.path.join(path, "nodes.csv")

    df_edges = pd.read_csv(edges_path)
    df_nodes = pd.read_csv(nodes_path)

    # Corrigir nomes de colunas se necessário
    if "hero" not in df_edges.columns and "node" in df_edges.columns:
        df_edges.rename(columns={"node": "hero"}, inplace=True)
    if "hero" not in df_nodes.columns and "node" in df_nodes.columns:
        df_nodes.rename(columns={"node": "hero"}, inplace=True)

    # Dicionário de tipo (Hero/Villain)
    tipo_dict = df_nodes.set_index("hero")["type"].to_dict()

    # Gerar conexões entre heróis na mesma HQ
    edges = []
    for comic, grupo in df_edges.groupby("comic"):
        herois = grupo["hero"].unique()
        for h1, h2 in combinations(herois, 2):
            edges.append((h1, h2))

    edges_df = pd.DataFrame(edges, columns=["hero1", "hero2"])

    # Criar grafo
    G = nx.from_pandas_edgelist(edges_df, source="hero1", target="hero2")

    # Adicionar atributo de tipo
    nx.set_node_attributes(G, tipo_dict, "type")

    if personagem not in G:
        raise ValueError(f"O personagem '{personagem}' não foi encontrado no dataset.")

    vizinhos = list(G.neighbors(personagem))
    subG = G.subgraph([personagem] + vizinhos)

    # Criar grafo interativo
    net = Network(height="800px", width="100%", bgcolor="#0d1117", font_color="white")

    # ✅ Configuração visual em JSON válido
    net.set_options("""
    {
      "nodes": {
        "shape": "dot",
        "size": 25,
        "font": { "size": 18, "color": "#ffffff", "strokeWidth": 2, "strokeColor": "#000000" },
        "borderWidth": 3,
        "borderWidthSelected": 5,
        "color": {
          "border": "#ffffff",
          "background": "#63b3ed",
          "highlight": { "border": "#ff4d4d", "background": "#ff8080" },
          "hover": { "border": "#ff4d4d", "background": "#ff8080" }
        }
      },
      "edges": {
        "color": { "color": "#aaaaaa", "highlight": "#ff4d4d" },
        "smooth": { "type": "continuous", "roundness": 0.4 },
        "width": 1.5
      },
      "layout": { "improvedLayout": true },
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -15000,
          "centralGravity": 0.1,
          "springLength": 400,
          "springConstant": 0.03,
          "damping": 0.15,
          "avoidOverlap": 1
        }
      },
      "interaction": { "dragNodes": true, "hover": true, "zoomView": true }
    }
    """)

    # Adicionar nós
    for node in subG.nodes():
        tipo = G.nodes[node].get("type", "Unknown")
        if node == personagem:
            net.add_node(node, label=node, color="#ff4d4d", size=50, title=f"{node} — {tipo}")
        else:
            net.add_node(node, label=node, color="#63b3ed", size=25, title=f"{node} — {tipo}")

    # Arestas normais
    for edge in subG.edges():
        net.add_edge(edge[0], edge[1])

    # Dicionário de comunidades (para o JS)
    comunidades = {}
    for hero, tipo in tipo_dict.items():
        comunidades.setdefault(tipo, []).append(hero)

    comunidades_json = json.dumps(comunidades)

    # Salvar HTML
    html_path = os.path.join("static", f"grafo_{personagem.replace(' ', '_')}.html")
    os.makedirs("static", exist_ok=True)
    net.write_html(html_path)

    # Inserir o JavaScript que destaca as conexões ao clicar
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    js_code = f"""
<script>
const comunidades = {comunidades_json};

network.on("click", function(params) {{
  if (params.nodes.length > 0) {{
    const nodeId = params.nodes[0];
    const edges = network.body.data.edges.get();

    // Limpa arestas vermelhas antigas
    const novas = edges.filter(e => !e.id.startsWith('red_'));

    // Adiciona novas arestas vermelhas para os vizinhos do nó clicado
    const vizinhos = network.getConnectedNodes(nodeId);
    vizinhos.forEach(v => {{
      novas.push({{
        id: 'red_' + nodeId + '_' + v,
        from: nodeId,
        to: v,
        color: 'red',
        width: 3
      }});
    }});

    network.body.data.edges.clear();
    network.body.data.edges.add(novas);
  }}
}});
</script>
"""

    html = html.replace("</body>", js_code + "\n</body>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    return html_path
