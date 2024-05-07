# Brenda Uemura     RA:148177

#Detecção e Prevenção de Deadlock (35%)

# Definição do número de processos e recursos
N_PROCESSOS = 3
N_RECURSOS = 4

# Definição da classe Processo para representar os processos
class Processo:
    def __init__(self, recursos_alocados, recursos_necessarios):
        self.recursos_alocados = recursos_alocados
        self.recursos_necessarios = recursos_necessarios

# Definição da classe BB para representar o estado do banco de recursos
class BB:
    def __init__(self, processos, recursos_disponiveis):
        self.processos = processos
        self.recursos_disponiveis = recursos_disponiveis

# Função para copiar recursos de uma lista para outra
def copia_recursos(destino, origem):
    for i in range(len(origem)):
        destino[i] = origem[i]

# Função para exibir os processos e seus recursos alocados e necessários
def exibe_processos(processos):
    for i, processo in enumerate(processos):
        print(f"Processo {i}:")
        print("- Recursos alocados:   ", end="")
        print(*processo.recursos_alocados)
        print("- Recursos necessários:", end="")
        print(*processo.recursos_necessarios)
        print()

# Função para executar o algoritmo de detecção de deadlock
def executa(bb):
    # Inicialização de variáveis
    n = N_PROCESSOS
    m = N_RECURSOS
    recursos_disponiveis = bb.recursos_disponiveis[:]
    recursos_alocados = [[0] * m for _ in range(n)]
    recursos_necessarios = [[0] * m for _ in range(n)]
    processos_finalizados = [False] * n
    processos_finalizados_count = 0

    # Copia dos recursos alocados e necessários dos processos
    for i in range(n):
        copia_recursos(recursos_alocados[i], bb.processos[i].recursos_alocados)
        copia_recursos(recursos_necessarios[i], bb.processos[i].recursos_necessarios)

    # Execução do algoritmo de detecção de deadlock
    while processos_finalizados_count < n:
        processo_encontrado = False
        for i in range(n):
            if not processos_finalizados[i]:
                for j in range(m):
                    if recursos_necessarios[i][j] > recursos_disponiveis[j]:
                        break
                else:
                    processos_finalizados_count += 1
                    processos_finalizados[i] = True
                    processo_encontrado = True
                    for k in range(m):
                        recursos_disponiveis[k] += recursos_alocados[i][k]
        if not processo_encontrado:
            break
    return processos_finalizados_count == n

if __name__ == "__main__":
    # Definição dos processos e recursos para o primeiro teste
    processos = [
        Processo([0, 0, 1, 0], [2, 0, 0, 1]),
        Processo([2, 0, 0, 1], [1, 0, 1, 0]),
        Processo([0, 1, 2, 0], [2, 1, 0, 0])
    ]
    recursos_disponiveis = [2, 1, 0, 0]

    # Execução do primeiro teste
    print("----------- Teste 1 -----------")
    print("Processos:")
    exibe_processos(processos)
    print("Recursos disponíveis:", *recursos_disponiveis)

    bb = BB(processos, recursos_disponiveis)
    if executa(bb):
        print("Não ocorreu deadlock, logo o sistema está em estado seguro")
    else:
        print("Ocorreu deadlock")

    # Definição dos processos e recursos para o segundo teste
    processos2 = [
        Processo([0, 0, 1, 0], [2, 0, 0, 1]),
        Processo([2, 0, 0, 1], [1, 0, 1, 0]),
        Processo([0, 1, 2, 0], [2, 1, 0, 1])
    ]
    recursos_disponiveis2 = [2, 1, 0, 0]

    # Execução do segundo teste
    print("\n----------- Teste 2 -----------")
    print("Processos: ")
    exibe_processos(processos2)
    print("Recursos disponíveis:", *recursos_disponiveis2)

    bb2 = BB(processos2, recursos_disponiveis2)
    if executa(bb2):
        print("Não ocorreu deadlock, logo o sistema está em estado seguro")
    else:
        print("Ocorreu deadlock")
