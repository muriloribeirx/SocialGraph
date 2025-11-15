import wikipediaapi
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# ==========
# 1️⃣ Inicialização
# ==========
wiki = wikipediaapi.Wikipedia(
    language='pt',
    user_agent='ProjetoGrafosWikipedia/1.0 (Universidade Federal de Engenharia, aluno: joao.silva@ufeng.br)'
)


# ==========
# 2️⃣ Função para obter links de uma página
# ==========
def get_links(title):
    page = wiki.page(title)
    if not page.exists():
        return []
    return list(page.links.keys())

# ==========
# 3️⃣ Função para buscar caminho entre duas páginas
#    (Busca em largura - BFS)
# ==========
def find_path(start_title, end_title, max_depth=2):
    G = nx.DiGraph()
    visited = set()
    queue = deque([(start_title, [start_title])])

    while queue:
        current_page, path = queue.popleft()
        if current_page in visited:
            continue
        visited.add(current_page)

        # Evita exploração muito profunda
        if len(path) > max_depth:
            continue

        links = get_links(current_page)
        for link in links:
            G.add_edge(current_page, link)
            if link == end_title:
                return G, path + [link]
            queue.append((link, path + [link]))

    return G, None

# ==========
# 4️⃣ Executando o exemplo
# ==========
start = "Neymar"
end = "Barack Obama"

print(f"Procurando caminho entre '{start}' e '{end}'...")

G, path = find_path(start, end, max_depth=2)

if path:
    print("➡️ Caminho encontrado:")
    print(" → ".join(path))
else:
    print("❌ Nenhum caminho encontrado dentro da profundidade definida.")

# ==========
# 5️⃣ Visualizando o grafo
# ==========
# if path:
#     subG = G.subgraph(path)
#     plt.figure(figsize=(10, 6))
#     nx.draw(
#         subG, 
#         with_labels=True, 
#         node_color='skyblue', 
#         node_size=1500, 
#         arrows=True,
#         font_size=8
#     )
#     plt.title(f"Caminho entre '{start}' e '{end}'")
#     plt.show()
