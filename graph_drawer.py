from pyvis.network import Network
import os

def gerar_grafo(edges, start, end):

    # garantir pasta
    os.makedirs("static", exist_ok=True)

    # Criar grafo PyVis
    net = Network(
        height="590px",
        width="100%",
        bgcolor="#f8f8f8",  # fundo claro
        font_color="black"  # texto escuro pra contrastar
    )

    net.set_options("""
    {
      "nodes": {
        "shape": "dot",
        "size": 25,
        "font": { "size": 18, "color": "#000000" },
        "borderWidth": 2,                     
        "color": {
          "border": "#000000",           
          "background": "#ffffff",        
          "highlight": { "border": "#ff4d4d", "background": "#ffe0e0" },
          "hover": { "border": "#ff4d4d", "background": "#ffe0e0" }
        }
      },
      "edges": {
        "color": { "color": "#000000" },   
        "smooth": { "type": "continuous", "roundness": 0.4 },
        "width": 1.5,
        "arrows": {
            "middle": { "enabled": true, "scaleFactor": 1.5 }
        }
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

    for node in net.node_ids:
        net.get_node(node)["color"] = {
            "border": "#000000",
            "background": "#2F7ED0",  # cor do nó
            "highlight": { "border": "#000000", "background": "#5FA6E0" },
            "hover": { "border": "#000000", "background": "#5FA6E0" }
        }


    # Destacar início
    if start in net.node_ids:
        net.get_node(start)["color"] =  {
            "border": "#000000",
            "background" : "#7ed02f",
            "highlight": { "border": "#000000", "background": "#96e24f" },
            "hover": { "border": "#000000", "background": "#96e24f" }
        }
        net.get_node(start)["size"] = 35

    # Destacar fim
    if end in net.node_ids:
        net.get_node(end)["color"] = {
            "border": "#000000",
            "background" :"#D02F2F",
            "highlight": { "border": "#000000", "background": "#E74B4B" },
            "hover": { "border": "#000000", "background": "#E74B4B" }
        }
        net.get_node(end)["size"] = 35

    # Nome do arquivo
    filename = f"grafo_{start}_{end}.html".replace(" ", "_")
    html_path = os.path.join("static", filename)

    net.write_html(html_path)

    return html_path
