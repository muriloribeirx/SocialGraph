from pyvis.network import Network
import os
from collections import defaultdict

def gerar_grafo(edges, start, end):

    # garantir pasta
    os.makedirs("static", exist_ok=True)

    # Criar grafo PyVis
    net = Network(
        # height="600px",
        # width="600px",
        bgcolor="#ffffff",
        font_color="black"
    )

    net.set_options("""
    {
      "nodes": {
        "shape": "dot",
        "size": 25,
        "font": { "size": 18, "color": "#000000" },
        "borderWidth": 2,
        "color": {
          "border": "#000000"
        }
      },
      "edges": {
        "color": { "color": "#000000" },   
        "smooth": { "enabled": true },
        "width": 1.5,
        "arrows": {
            "middle": { "enabled": true, "scaleFactor": 3 }
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

    # -------------------------
    # AGRUPAR ARESTAS POR PAR DE NÓS
    # -------------------------
    rotas = defaultdict(list)
    for (a, b) in edges:
        rotas[(a, b)].append((a, b))

        # Adicionar nós
        net.add_node(a, label=a, title=a)
        net.add_node(b, label=b, title=b)

    # -------------------------
    # ADICIONAR ARESTAS COM CURVATURAS "CAMPO MAGNÉTICO"
    # -------------------------
    for (a, b), lista in rotas.items():
        n = len(lista)

        # Gerar curvaturas distribuídas simetricamente
        # Exemplo: 5 rotas → [-0.6, -0.3, 0, 0.3, 0.6]
        if n == 1:
            curvas = [0]
        else:
            step = 0.6 / (n - 1)
            curvas = [(-0.6 + i * (1.2 / (n - 1))) for i in range(n)]

        for curvatura in curvas:
            if curvatura < 0:
                tipo = "curvedCCW"   # curva para baixo
            elif curvatura > 0:
                tipo = "curvedCW"    # curva para cima
            else:
                tipo = "curvedCW"    # linha reta

            net.add_edge(
                a, b,
                smooth={
                    "enabled": True,
                    "type": tipo,
                    "roundness": curvatura
                }
            )

    # -------------------------
    # CORES DOS NÓS
    # -------------------------
    for node in net.node_ids:
        net.get_node(node)["color"] = {
            "border": "#000000",
            "background": "#2F7ED0",
            "highlight": {"border": "#000000", "background": "#5FA6E0"},
            "hover": {"border": "#000000", "background": "#5FA6E0"}
        }

    # Destacar início
    if start in net.node_ids:
        net.get_node(start)["color"] = {
            "border": "#000000",
            "background": "#7ed02f",
            "highlight": {"border": "#000000", "background": "#96e24f"},
            "hover": {"border": "#000000", "background": "#96e24f"}
        }
        net.get_node(start)["size"] = 35
        node = net.get_node(start)
        node["x"] = -500
        node["y"] = 0
        node["fixed"] = True
        node["physics"] = False

    # Destacar fim
    if end in net.node_ids:
        net.get_node(end)["color"] = {
            "border": "#000000",
            "background": "#D02F2F",
            "highlight": {"border": "#000000", "background": "#E74B4B"},
            "hover": {"border": "#000000", "background": "#E74B4B"}
        }
        net.get_node(end)["size"] = 35
        node = net.get_node(end)
        node["x"] = 500
        node["y"] = 0
        node["fixed"] = True
        node["physics"] = False

    # SALVAR
    filename = f"grafo_{start}_{end}.html".replace(" ", "_")
    html_path = os.path.join("static", filename)
    net.write_html(html_path)

    return html_path
