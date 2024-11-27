class Grafo:
    def __init__(self):
        self.grafo = {}

    def carregar_grafo(self, arquivo):
        # Abrir o arquivo com codificação UTF-8 para evitar problemas com caracteres especiais
        with open(arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                # Dividindo a linha para separar o vértice e as arestas
                vertice, arestas = linha.split(':')
                vertice = vertice.strip()
                arestas = arestas.strip()

                # Inicializar o vértice no grafo se não existir
                if vertice not in self.grafo:
                    self.grafo[vertice] = {}

                # Limpar a string das arestas removendo espaços extras
                arestas = arestas.strip('()')

                # Dividindo as arestas por ')(' e percorrendo as arestas
                for aresta in arestas.split('),'):
                    # Remover qualquer parêntese extra e espaços ao redor
                    aresta = aresta.strip('() ')
                    
                    # Separar destino e peso da aresta
                    if ',' in aresta:
                        destino, peso = aresta.split(',')
                        destino = destino.strip()
                        try:
                            peso = int(peso.strip())
                            # Adicionando a aresta no grafo
                            self.grafo[vertice][destino] = peso
                            #print(f"Arestra válida: {vertice} -> {destino}, {peso}")
                        except ValueError:
                            print(f"Aresta inválida encontrada: ({destino}, {peso})")

    


    def alterar_pesos_aleatorios(self):
        """Altera os pesos das arestas de forma determinística."""
        for vertice in self.grafo:
            for vizinho in self.grafo[vertice]:
                novo_peso = (self.grafo[vertice][vizinho] * 3) % 97 + 1
                self.grafo[vertice][vizinho] = novo_peso

    def buscar_em_profundidade(self, origem, destino):
        """Busca em profundidade no grafo."""
        visitados = set()
        caminho = []

        def dfs(v):
            if v in visitados:
                return False
            visitados.add(v)
            caminho.append(v)
            if v == destino:
                return True
            for vizinho in self.grafo.get(v, {}):
                if dfs(vizinho):
                    return True
            caminho.pop()
            return False

        if dfs(origem):
            return caminho
        else:
            return None

    def buscar_em_largura(self, origem, destino):
        """Busca em largura no grafo."""
        from collections import deque
        fila = deque([(origem, [origem])])
        visitados = set()

        while fila:
            atual, caminho = fila.popleft()
            if atual == destino:
                return caminho
            if atual in visitados:
                continue
            visitados.add(atual)
            for vizinho in self.grafo.get(atual, {}):
                fila.append((vizinho, caminho + [vizinho]))

        return None

    def dijkstra(self, origem, destino):
        """Busca pelo algoritmo de Dijkstra."""
        distancias = {v: float('inf') for v in self.grafo}
        anteriores = {v: None for v in self.grafo}
        distancias[origem] = 0
        visitados = set()

        while True:
            nao_visitados = {v: distancias[v] for v in distancias if v not in visitados}
            if not nao_visitados:
                break
            atual = min(nao_visitados, key=nao_visitados.get)
            visitados.add(atual)

            for vizinho, peso in self.grafo.get(atual, {}).items():
                nova_distancia = distancias[atual] + peso
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    anteriores[vizinho] = atual

        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = anteriores[atual]

        caminho.reverse()
        return caminho if distancias[destino] != float('inf') else None

    def floyd_warshall(self):
        vertices = list(self.grafo.keys())
        dist = {v: {u: float('inf') for u in vertices} for v in vertices}
        pred = {v: {u: None for u in vertices} for v in vertices}  # Predecessores

        # Inicializar distâncias e predecessores
        for v in self.grafo:
            dist[v][v] = 0
            for vizinho, peso in self.grafo[v].items():
                dist[v][vizinho] = peso
                pred[v][vizinho] = v  # Vizinho direto como predecessor

        # Algoritmo de Floyd-Warshall
        for k in vertices:
            for i in vertices:
                for j in vertices:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        pred[i][j] = pred[k][j]

        return dist, pred

    @staticmethod    
    def reconstruir_caminho(pred, origem, destino):
        """Reconstrói o caminho entre origem e destino usando a matriz de predecessores."""
        caminho = []
        atual = destino
        while atual:
            caminho.insert(0, atual)
            if atual == origem:
                break
            atual = pred[origem][atual]
        if caminho[0] == origem:
            return caminho
        return None

    def bellman_ford(self, origem, destino):
        """Busca pelo algoritmo de Bellman-Ford."""
        distancias = {v: float('inf') for v in self.grafo}
        anteriores = {v: None for v in self.grafo}
        distancias[origem] = 0

        for _ in range(len(self.grafo) - 1):
            for u in self.grafo:
                for v, peso in self.grafo[u].items():
                    if distancias[u] + peso < distancias[v]:
                        distancias[v] = distancias[u] + peso
                        anteriores[v] = u

        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = anteriores[atual]

        caminho.reverse()
        return caminho if distancias[destino] != float('inf') else None


