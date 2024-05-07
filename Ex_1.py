#Brenda Uemura      RA: 148177

# Criação de Processos e Gerenciamento (30%)  >> EX_1 <<
# utilizando a funcao fork()

import multiprocessing

def calcula_intervalo(lista): # calcula o intervalo entre dois números
    if lista[0] == lista[1]:
        return -1
    if lista[0] > lista[1]:
        return lista[0] - lista[1] + 1
    else:
        return lista[1] - lista[0] + 1

# Função para ser executada pelos processos filhos, que calcula a soma parcial dos números no intervalo atribuído a cada processo
def calcular_soma_parcial(pipe, lista, inicio, quantidade):
    soma = sum(lista[inicio:inicio + quantidade])  # Calcula a soma parcial dos números no intervalo atribuído
    pipe.send(soma)  # Envia a soma parcial através do pipe para o processo pai

def main():
    # Entrada do usuário para determinar a quantidade de processos filhos a serem criados
    qnt_filhos = int(input("Digite quantos processos filhos devem ser criados: "))

    # Entrada do usuário para definir o intervalo que deseja somar
    intervalo = list(map(int, input("Digite o intervalo que deseja ser somado (dois números separados por espaço): ").split()))

    # Cálculo da quantidade de números no intervalo
    qnt_num_intervalo = calcula_intervalo(intervalo)

    # Divisão do intervalo entre os processos filhos
    num_por_filho = [qnt_num_intervalo // qnt_filhos] * qnt_filhos
    resto = qnt_num_intervalo % qnt_filhos
    for i in range(resto):
        num_por_filho[i] += 1

    # Criação da lista com os números do intervalo
    lista = [intervalo[0] + k for k in range(qnt_num_intervalo)]

    # Criação dos pipes para comunicação entre processos
    pipes = [multiprocessing.Pipe() for _ in range(qnt_filhos)]
    processos = []

    # Loop para criar os processos filhos
    for i in range(qnt_filhos):
        inicio = sum(num_por_filho[:i])  # Determina o índice de início do intervalo atribuído ao processo filho
        quantidade = num_por_filho[i]  # Determina a quantidade de números no intervalo atribuído ao processo filho
        processo = multiprocessing.Process(target=calcular_soma_parcial, args=(pipes[i][1], lista, inicio, quantidade))  # Cria o processo filho
        processo.start()  # Inicia o processo filho
        processos.append(processo)  # Adiciona o processo filho à lista de processos

    # Soma final inicializada
    soma_final = 0
    for pipe in pipes:
        soma_parcial = pipe[0].recv()  # Recebe a soma parcial do processo filho através do pipe
        soma_final += soma_parcial  # Adiciona a soma parcial à soma final

    # Imprime o resultado final
    print("Somatório final =", soma_final)

    # Aguarda todos os processos filhos terminarem
    for processo in processos:
        processo.join()

if __name__ == "__main__":
    main()
