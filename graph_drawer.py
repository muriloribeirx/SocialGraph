from pyvis.network import Network
import os

def gerar_grafo(edges, start, end):

    # garantir pasta
    os.makedirs("static", exist_ok=True)

    # Criar grafo PyVis
    net = Network(
        height="590px",
        width="100%",
        bgcolor="#0d1117",
        font_color="white"
    )

    # Aplicar o estilo personalizado (SEU CÓDIGO)
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

    # Adicionar nós e arestas (versão simples usando apenas "edges")
    for a, b in edges:
        net.add_node(a, label=a, title=a)
        net.add_node(b, label=b, title=b)
        net.add_edge(a, b)

    # Destacar início
    if start in net.node_ids:
        net.get_node(start)["color"] = "red"
        net.get_node(start)["size"] = 45

    # Destacar fim
    if end in net.node_ids:
        net.get_node(end)["color"] = "green"
        net.get_node(end)["size"] = 45

    # Nome do arquivo
    filename = f"grafo_{start}_{end}.html".replace(" ", "_")
    html_path = os.path.join("static", filename)

    net.write_html(html_path)

    return html_path
