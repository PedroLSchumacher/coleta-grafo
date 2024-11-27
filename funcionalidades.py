class Grafo:
    def __init__(self):
        self.grafo = {}

    def carregar_grafo(self, arquivo):
    
        with open(arquivo, 'r', encoding='utf-8') as f: # Abrir o arquivo com codificação UTF-8 para evitar problemas com caracteres especiais
            for linha in f:
                # Dividindo a linha para separar o vértice e as arestas
                vertice, arestas = linha.split(':')  # Divide a linha em duas partes: o vértice (antes dos dois pontos) e as arestas (depois dos dois pontos).
                vertice = vertice.strip()  # Remove espaços em branco extras ao redor do nome do vértice.
                arestas = arestas.strip()  # Remove espaços em branco extras ao redor das arestas.

                # Inicializar o vértice no grafo se não existir
                if vertice not in self.grafo:  # Verifica se o vértice já está no dicionário `self.grafo`.
                    self.grafo[vertice] = {}  # Inicializa o vértice com um dicionário vazio para armazenar suas conexões.

                # Limpar a string das arestas removendo espaços extras
                arestas = arestas.strip('()')  # Remove parênteses extras na extremidade da string.

                # Dividindo as arestas por ')(' e percorrendo as arestas
                for aresta in arestas.split('),'):  # Divide as arestas com base na separação `),` para tratar cada aresta individualmente.
                    # Remover qualquer parêntese extra e espaços ao redor
                    aresta = aresta.strip('() ')  # Remove parênteses e espaços extras ao redor da descrição da aresta.

                    # Separar destino e peso da aresta
                    if ',' in aresta:  # Verifica se a aresta contém a vírgula, indicando que há destino e peso.
                        destino, peso = aresta.split(',')  # Divide a string da aresta em duas partes: o destino e o peso.
                        destino = destino.strip()  # Remove espaços em branco do nome do destino.
                        try:
                            peso = int(peso.strip())  # Converte o peso para um número inteiro, removendo espaços em branco.
                            # Adicionando a aresta no grafo
                            self.grafo[vertice][destino] = peso  # Adiciona o destino e o peso ao dicionário do vértice no grafo.
                            # print(f"Aresta válida: {vertice} -> {destino}, {peso}")
                        except ValueError:  # Lida com erros na conversão do peso para inteiro.
                            print(f"Aresta inválida encontrada: ({destino}, {peso})")  # Informa o usuário se encontrou uma aresta com dados inválidos.

    def buscar_em_profundidade(self, origem, destino):
        
        visitados = set() # Conjunto para rastrear os vértices visitados durante a busca.
        caminho = [] # Lista para armazenar o caminho atual entre origem e destino.
        
        def dfs(v): # Função recursiva que realiza a busca em profundidade.
            
            if v in visitados: # Verifica se o vértice já foi visitado para evitar ciclos.
                return False  # Retorna False, pois já exploramos este vértice.

            visitados.add(v) # Marca o vértice como visitado.
            caminho.append(v) # Adiciona o vértice atual ao caminho.

            if v == destino: # Verifica se o vértice atual é o destino.
                return True  # Retorna True, pois encontramos o destino.

            # Itera sobre os vizinhos do vértice atual.
            for vizinho in self.grafo.get(v, {}):  # Usa `.get` para evitar KeyError caso o vértice não tenha vizinhos.
                if dfs(vizinho): # Realiza a busca recursivamente nos vizinhos.
                    return True  # Se o destino for encontrado em um vizinho, retorna True.

            caminho.pop() # Se nenhum caminho foi encontrado através deste vértice, remove-o do caminho.

            return False  # Retorna False para indicar falha em encontrar o destino a partir deste vértice.

        if dfs(origem): # Inicia a busca em profundidade a partir do vértice de origem.
            return caminho  # Retorna o caminho encontrado se o destino for alcançado.
        else:
            return None  # Retorna None se não houver caminho entre origem e destino.

    def buscar_em_largura(self, origem, destino):
        
        from collections import deque # Importa `deque`, uma estrutura eficiente para manipular filas.

        fila = deque([(origem, [origem])]) # Cria a fila, inicializando com um tupla contendo o vértice inicial e o caminho até ele.

        visitados = set() # Conjunto para armazenar os vértices visitados, evitando ciclos.

        while fila: # Enquanto houver vértices na fila para explorar.
            atual, caminho = fila.popleft() # Remove o primeiro elemento da fila (FIFO).

            
            if atual == destino: # Verifica se o vértice atual é o destino.
                return caminho  # Retorna o caminho encontrado.

            if atual in visitados: # Ignora o vértice se ele já foi visitado.
                continue

            visitados.add(atual) # Marca o vértice como visitado.

            # Itera sobre os vizinhos do vértice atual.
            for vizinho in self.grafo.get(atual, {}):  # Usa `.get` para evitar erros se não houver vizinhos.
                
                fila.append((vizinho, caminho + [vizinho])) # Adiciona o vizinho à fila com o caminho atualizado.

        return None # Retorna `None` se nenhum caminho for encontrado.

    def dijkstra(self, origem, destino):

        distancias = {v: float('inf') for v in self.grafo} # Inicializa as distâncias de todos os vértices como infinito.

        anteriores = {v: None for v in self.grafo} # Inicializa os predecessores (para reconstruir o caminho) como None.

        distancias[origem] = 0 # Define a distância do vértice de origem como 0 (ponto de partida).

        visitados = set() # Conjunto para rastrear os vértices visitados.

        
        while True: # Laço principal do algoritmo
            nao_visitados = {v: distancias[v] for v in distancias if v not in visitados} # Seleciona os vértices que ainda não foram visitados e suas distâncias.

            if not nao_visitados: # Se não houver vértices não visitados, encerra o laço.
                break

            atual = min(nao_visitados, key=nao_visitados.get) # Encontra o vértice não visitado com a menor distância.
            visitados.add(atual) # Marca o vértice atual como visitado.

            
            for vizinho, peso in self.grafo.get(atual, {}).items(): # Atualiza as distâncias dos vizinhos do vértice atual.
                nova_distancia = distancias[atual] + peso # Calcula a nova distância ao vizinho passando pelo vértice atual.

                
                if nova_distancia < distancias[vizinho]: # Se a nova distância for menor, atualiza a distância e o predecessor.
                    distancias[vizinho] = nova_distancia
                    anteriores[vizinho] = atual

        
        caminho = [] # Reconstrói o caminho percorrendo os predecessores a partir do destino.
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = anteriores[atual]

        caminho.reverse() # Reverte o caminho para que comece na origem e termine no destino.

        return caminho if distancias[destino] != float('inf') else None # Retorna o caminho se o destino for alcançável; caso contrário, retorna `None`.

    def floyd_warshall(self):
        
        vertices = list(self.grafo.keys()) # Lista dos vértices no grafo.
        dist = {v: {u: float('inf') for u in vertices} for v in vertices} # Inicializa a matriz de distâncias com infinito (inacessível) para todos os pares.
        pred = {v: {u: None for u in vertices} for v in vertices} # Inicializa a matriz de predecessores com None (sem caminho conhecido).

        
        for v in self.grafo: # Inicializa as distâncias diretas entre vértices adjacentes e o próprio vértice.
            # A distância do vértice para si mesmo é 0.
            dist[v][v] = 0 # Para cada vizinho, define a distância inicial como o peso da aresta.
            for vizinho, peso in self.grafo[v].items():
                dist[v][vizinho] = peso
                pred[v][vizinho] = v # Define o predecessor inicial como o próprio vértice.

        
        for k in vertices: # Algoritmo de Floyd-Warshall: considera cada vértice como intermediário (k).
            for i in vertices:  # Origem (i)
                for j in vertices:  # Destino (j)
                    if dist[i][k] + dist[k][j] < dist[i][j]: # Se passar por k reduz a distância entre i e j, atualiza.
                        dist[i][j] = dist[i][k] + dist[k][j]
                        pred[i][j] = pred[k][j] # Atualiza o predecessor para indicar o novo caminho mais curto.

        return dist, pred # Retorna a matriz de distâncias mínimas e a matriz de predecessores.

    @staticmethod
    def reconstruir_caminho(pred, origem, destino):
        
        caminho = [] # Inicializa o caminho como uma lista vazia.

        atual = destino # Começa pelo destino e retrocede até a origem usando os predecessores.
        while atual:
            caminho.insert(0, atual) # Insere o vértice no início do caminho.
            if atual == origem: # Se alcançou a origem, termina o laço.
                break
            atual = pred[origem][atual] # Atualiza o vértice atual para o predecessor.
        if caminho[0] == origem: # Verifica se o caminho começa na origem; caso contrário, não há caminho válido.
            return caminho

        return None # Retorna `None` se não foi possível reconstruir um caminho válido.

    def bellman_ford(self, origem, destino):
        
        distancias = {v: float('inf') for v in self.grafo} # Inicializa as distâncias de todos os vértices como infinito (inacessível).
        
        anteriores = {v: None for v in self.grafo} # Inicializa o predecessor de cada vértice como None (sem caminho conhecido ainda).
        
        distancias[origem] = 0 # Define a distância da origem para ela mesma como 0.

        
        for _ in range(len(self.grafo) - 1): # Relaxa todas as arestas (|V| - 1) vezes, onde |V| é o número de vértices.
            for u in self.grafo:  # Para cada vértice 'u'
                for v, peso in self.grafo[u].items():  # Para cada aresta (u -> v) com peso 'peso'
                    if distancias[u] + peso < distancias[v]: # Verifica se o caminho atual para v via u é mais curto.
                        distancias[v] = distancias[u] + peso # Atualiza a distância mínima para o vértice v.
                        anteriores[v] = u # Define u como predecessor de v no caminho mais curto.

        caminho = [] # Reconstrói o caminho do destino até a origem usando os predecessores.
        atual = destino
        while atual is not None:  # Enquanto houver predecessores
            caminho.append(atual)  # Adiciona o vértice atual ao caminho.
            atual = anteriores[atual]  # Move para o predecessor.

        caminho.reverse() # Inverte o caminho para que ele vá da origem para o destino.

        return caminho if distancias[destino] != float('inf') else None # Retorna o caminho se o destino for acessível (distância < infinito).


