import wikipediaapi
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# ========== 1️⃣ Inicialização ==========
wiki = wikipediaapi.Wikipedia(
    language='pt',
    user_agent='ProjetoGrafosWikipedia/1.0 (Universidade Federal de Engenharia, aluno: joao.silva@ufeng.br)'
)

# ========== 2️⃣ Função para obter links de uma página ==========
def get_links(title):
    page = wiki.page(title)
    if not page.exists():
        return []
    return list(page.links.keys())

# ========== 3️⃣ Função para buscar até N caminhos ==========
def find_paths(start_title, end_title, max_depth=2, max_paths=5):
    """
    Busca até 'max_paths' caminhos entre duas páginas da Wikipédia.
    """
    G = nx.DiGraph()
    queue = deque([(start_title, [start_title])])
    visited = set()
    found_paths = []

    while queue and len(found_paths) < max_paths:
        current_page, path = queue.popleft()

        # Evita revisitar
        if current_page in visited:
            continue
        visited.add(current_page)

        # Limita profundidade
        if len(path) > max_depth:
            continue

        # Obtém links
        links = get_links(current_page)
        for link in links:
            G.add_edge(current_page, link)
            new_path = path + [link]

            # Se encontrou o destino
            if link == end_title:
                found_paths.append(new_path)
                if len(found_paths) >= max_paths:
                    break  # Para se já atingiu o limite
            else:
                queue.append((link, new_path))

    return G, found_paths

# ========== 4️⃣ Entrada do usuário ==========
start = input("Digite o primeiro assunto: ").strip()
end = input("Digite o segundo assunto: ").strip()

print(f"\n🔎 Procurando caminhos entre '{start}' e '{end}' (no máximo 5, profundidade até 3)...\n")

# ========== 5️⃣ Execução ==========
G, paths = find_paths(start, end, max_depth=2, max_paths=5)

# ========== 6️⃣ Resultados ==========
if paths:
    print(f"✅ {len(paths)} caminho(s) encontrado(s):\n")
    for i, p in enumerate(paths, 1):
        print(f"{i}. " + " → ".join(p))
else:
    print("❌ Nenhum caminho encontrado dentro da profundidade definida.")

# ========== 7️⃣ Visualização opcional ==========
if paths:
    sub_nodes = set(node for path in paths for node in path)
    subG = G.subgraph(sub_nodes)

    plt.figure(figsize=(12, 8))
    nx.draw(
        subG,
        with_labels=True,
        node_color='lightblue',
        node_size=1500,
        arrows=True,
        font_size=8
    )
    plt.title(f"Caminhos entre '{start}' e '{end}' (no máximo 5, profundidade 3)")
    plt.show()
