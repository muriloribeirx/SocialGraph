# Algoritmo de Ford-Fulkerson (versão simplificada)

# Função para procurar um caminho do início (source) até o final (sink)
def bfs(grafo_residual, inicio, fim, caminho_pai):
    visitado = []
    fila = [inicio]

    while fila:
        u = fila.pop(0)
        visitado.append(u)

        for v in grafo_residual[u]:
            if v not in visitado and grafo_residual[u][v] > 0:
                caminho_pai[v] = u
                fila.append(v)
                if v == fim:
                    return True
    return False


def ford_fulkerson(grafo, inicio, fim):
    # Cria uma cópia do grafo para ser o grafo residual
    grafo_residual = {}
    for u in grafo:
        grafo_residual[u] = {}
        for v in grafo[u]:
            grafo_residual[u][v] = grafo[u][v]

    # Garante que todos os nós existam no grafo residual
    for u in grafo:
        for v in grafo[u]:
            if v not in grafo_residual:
                grafo_residual[v] = {}
            if u not in grafo_residual[v]:
                grafo_residual[v][u] = 0

    caminho_pai = {}
    fluxo_maximo = 0

    # Enquanto houver um caminho com capacidade disponível
    while bfs(grafo_residual, inicio, fim, caminho_pai):
        # Encontra o menor fluxo possível no caminho encontrado
        fluxo_caminho = float("inf")
        v = fim
        while v != inicio:
            u = caminho_pai[v]
            fluxo_caminho = min(fluxo_caminho, grafo_residual[u][v])
            v = u

        # Atualiza as capacidades do grafo residual
        v = fim
        while v != inicio:
            u = caminho_pai[v]
            grafo_residual[u][v] -= fluxo_caminho
            grafo_residual[v][u] += fluxo_caminho
            v = u

        # Soma o fluxo encontrado
        fluxo_maximo += fluxo_caminho

    return fluxo_maximo


# ===== Grafo do problema =====
grafo = {
    'Paulínia': {'Piracicaba': 7, 'Campinas': 2},
    'Piracicaba': {'Sorocaba': 5},
    'Campinas': {'Itu': 1, 'Jundiaí': 1},
    'Itu': {'Sorocaba': 1, 'São Paulo': 5, 'Jundiaí': 5},
    'Jundiaí': {'São Paulo': 5},
    'Sorocaba': {'São Paulo': 5}
}

# ===== Execução =====
inicio = 'Paulínia'
fim = 'São Paulo'

fluxo = ford_fulkerson(grafo, inicio, fim)
print(f"Fluxo Máximo de {inicio} até {fim}: {fluxo}")
