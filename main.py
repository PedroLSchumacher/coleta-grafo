from funcionalidades import Grafo
import time

def menu():
    grafo = Grafo()
    grafo.carregar_grafo("grafo.txt")

    while True:
        print("\nMenu Principal:")
        print("1. Iniciar o dia")
        print("2. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Saudações!")
            gerenciar_rotas(grafo)
        elif opcao == "2":
            print("Saindo aqui, valeu!")
            break
        else:
            print("Visshhhhh, é por aqui não.")


def gerenciar_rotas(grafo):
    # Listas de clientes predefinidas
    opcoes_clientes = [
        ["C16", "C9", "C17", "C11", "C18"],
        ["C3", "C7", "C2", "C12", "C20"],
        ["C13", "C18", "C1", "C3", "C8"],
        ["C5", "C16", "C7", "C21", "C4"],
    ]

    while True:
        print("\nMenu de Rotas:")
        print("1. Gerar lista de clientes")
        print("2. Sair")
        opcao = input("Bora lá, escolha uma opção: ")

        if opcao == "1":
            print("\nOlha só, tua lista de clientes é essa hoje:")
            for i, lista in enumerate(opcoes_clientes, start=1):
                print(f"{i}. {', '.join(lista)}")

            escolha = input("Escolha uma lista (1-4): ")

            if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes_clientes):
                lista_clientes = opcoes_clientes[int(escolha) - 1]
                print("\nLista de clientes selecionada:", ", ".join(lista_clientes))
                calcular_rota(grafo, lista_clientes)
            else:
                print("Vishhh, vai precisar escolher de novo.")
        elif opcao == "2":
            print("Voltandooo.")
            break
        else:
            print("Opção errada meu chapa.")


def calcular_rota(grafo, lista_clientes):
    print("\nAgora vamos calcular a sua rota saindo dos Correios, passando pela lista de clientes e terminando no CD.")
    rota_completa = ["Correios"] + lista_clientes + ["CD"]
    relatorio = {"rota": rota_completa, "detalhes": [], "custo_total": 0, "tempo_execucao": 0}

    while True: 
        print("\nMétodos de Busca:")
        print("1. Busca em Profundidade")
        print("2. Busca em Largura")
        print("3. Dijkstra")
        print("4. Floyd-Warshall")
        print("5. Bellman-Ford")
        print("6. Voltar")
        escolha = input("Escolha um método: ")

        if escolha in {"1", "2", "3", "5"}:
            caminho_total = []
            custo_total = 0
            tempo_total = 0  # Variável para somar os tempos de execução

            for i in range(len(rota_completa) - 1):
                origem, destino = rota_completa[i], rota_completa[i + 1]

                # Medir o tempo de execução
                inicio = time.time()
                if escolha == "1":
                    sub_caminho = grafo.buscar_em_profundidade(origem, destino)
                elif escolha == "2":
                    sub_caminho = grafo.buscar_em_largura(origem, destino)
                elif escolha == "3":
                    sub_caminho = grafo.dijkstra(origem, destino)
                elif escolha == "5":
                    sub_caminho = grafo.bellman_ford(origem, destino)
                fim = time.time()

                tempo_execucao = fim - inicio
                tempo_total += tempo_execucao

                if sub_caminho:
                    custo = sum(
                        grafo.grafo[sub_caminho[j]][sub_caminho[j + 1]]
                        for j in range(len(sub_caminho) - 1)
                    )
                    custo_total += custo
                    caminho_total.extend(sub_caminho if not caminho_total else sub_caminho[1:])
                    relatorio["detalhes"].append((origem, destino, custo, tempo_execucao))
                else:
                    print(f"Nenhum caminho encontrado entre {origem} e {destino}.")
                    return

            relatorio["custo_total"] = custo_total
            relatorio["tempo_execucao"] = tempo_total
            print("Rota gerada pelo algoritmo:", " -> ".join(caminho_total))
            print(f"Tempo total de execução: {tempo_total:.4f} segundos")

        elif escolha == "4":
            # Medir o tempo total de execução para Floyd-Warshall
            inicio = time.time()
            distancias, predecessores = grafo.floyd_warshall()
            fim = time.time()

            tempo_execucao = fim - inicio  # Tempo total do algoritmo
            caminho_total = []
            custo_total = 0

            for i in range(len(rota_completa) - 1):
                origem, destino = rota_completa[i], rota_completa[i + 1]
                sub_caminho = grafo.reconstruir_caminho(predecessores, origem, destino)

                if sub_caminho:
                    custo = distancias[origem][destino]
                    custo_total += custo
                    caminho_total.extend(sub_caminho if not caminho_total else sub_caminho[1:])

                    # Atribuir um tempo fixo hipotético para cada subrota
                    tempo_por_subrota = tempo_execucao / (len(rota_completa) - 1)
                    relatorio["detalhes"].append((origem, destino, custo, tempo_por_subrota))
                else:
                    print(f"Nenhum caminho encontrado entre {origem} e {destino}.")
                    return

            relatorio["custo_total"] = custo_total
            relatorio["tempo_execucao"] = tempo_execucao
            print("Rota gerada pelo algoritmo Floyd-Warshall:", " -> ".join(caminho_total))
            print(f"Tempo total de execução: {tempo_execucao:.4f} segundos")

        elif escolha == "6":
            break
        else:
            print("Opção inválida.")
            continue

        gerenciar_relatorio(relatorio)


def gerenciar_relatorio(relatorio):
    while True:
        print("\nMenu do Relatório:")
        print("1. Gerar relatório")
        print("2. Sair e finalizar o dia")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            print("\nRelatório da Rota:")
            print("Rota completa:", " -> ".join(relatorio["rota"]))
            print("Detalhes da rota:")
            for origem, destino, custo, tempo in relatorio["detalhes"]:
                print(f"  {origem} -> {destino}: Custo {custo}, Tempo: {tempo:.4f} segundos")
            print(f"Custo total: {relatorio['custo_total']}")
            print(f"Tempo total de execução: {relatorio['tempo_execucao']:.4f} segundos")
        elif escolha == "2":
            print("Está na hora de dar tchau!")
            exit()
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
