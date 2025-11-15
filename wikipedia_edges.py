import wikipediaapi
from collections import deque

# ========== Inicialização ==========
wiki = wikipediaapi.Wikipedia(
    language='pt',
    user_agent='ProjetoGrafosWikipedia/1.0 (Universidade Federal de Engenharia, aluno: joao.silva@ufeng.br)'
)

# ========== Função para obter links ==========
def get_links(title):
    page = wiki.page(title)
    if not page.exists():
        return []
    return list(page.links.keys())

# ========== Busca SOMENTE caminhos ==========
def gerar_edges(start_title, end_title, max_depth, max_paths):
    """
    Retorna SOMENTE as arestas dos caminhos encontrados.
    Exemplo de retorno:
    [('Neymar', 'Estados Unidos'), ('Estados Unidos', 'Barack Obama')]
    """
    
    queue = deque([(start_title, [start_title])])
    visited = set()
    found_paths = []

    while queue and len(found_paths) < max_paths:
        current_page, path = queue.popleft()

        if current_page in visited:
            continue
        visited.add(current_page)

        if len(path) > max_depth:
            continue

        links = get_links(current_page)

        for link in links:
            new_path = path + [link]

            if link == end_title:
                found_paths.append(new_path)
                if len(found_paths) >= max_paths:
                    break
            else:
                queue.append((link, new_path))

    # ---- extrai somente arestas dos caminhos encontrados ----
    edges = []
    seen = set()

    for path in found_paths:
        for i in range(len(path) - 1):
            edge = (path[i], path[i+1])
            if edge not in seen:
                edges.append(edge)
                seen.add(edge)
    print(edges)
    return edges


# # ========== Teste temporário ==========
# start = "Neymar"
# end = "Barack Obama"
# max_depth = 2
# max_paths = 1

# gerar_edges(start, end, max_depth, max_paths)