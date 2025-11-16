from pyvis.network import Network
import os

def gerar_grafo(edges, start, end):

    # garantir pasta
    os.makedirs("static", exist_ok=True)

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

    # Criar grafo PyVis
    net = Network(
        height="800px",
        width="100%",
        bgcolor="#0d1117",
        font_color="white"
    )

    net.barnes_hut()

    # Adicionar nós e edges
    for a, b in edges:
        net.add_node(a, label=a)
        net.add_node(b, label=b)
        net.add_edge(a, b)

    # Destacar o start e o end
    net.get_node(start)["color"] = "red"
    net.get_node(start)["size"] = 40

    net.get_node(end)["color"] = "green"
    net.get_node(end)["size"] = 40

    net.set_options(
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
    )

    # Caminho do arquivo final
    filename = f"grafo_{start}_{end}.html".replace(" ", "_")
    html_path = os.path.join("static", filename)

    # Gerar HTML
    net.write_html(html_path)

    return html_path
