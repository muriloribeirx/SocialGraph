from pyvis.network import Network
import os

def gerar_grafo(edges, start, end):

    # garantir pasta
    os.makedirs("static", exist_ok=True)

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

    # Caminho do arquivo final
    filename = f"grafo_{start}_{end}.html".replace(" ", "_")
    html_path = os.path.join("static", filename)

    # Gerar HTML
    net.write_html(html_path)

    return html_path
