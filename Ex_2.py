# Brenda Uemura     RA:148177

# Escalonamento de Processos (35%) >> EX_2 <<
# Descrição: Desenvolva um programa que simule os seguintes algoritmos de escalonamento de processos: First-Come,
# First-Served (FCFS); Round Robin (RR) e; Shortest Job First (SJF).

import copy

# FIRST COME, FIRST SERVE
class FCFS:
    def execute(self, processos):

        tempo_retorno_total, tempo_resposta_total, tempo_espera_total = 0, 0, 0 # inicializacao dos tempos
        tempo_inicio = processos[0][0] # armazena o instante de chegada do primeiro processo
        soma_duracao = 0 # soma das durações do processos

        for n, processo in enumerate(processos):
            # O primeiro processo possui tempo de resposta e tempo de espera zero
            if n != 0:
                tempo_resposta_total += soma_duracao - (processo[0] - tempo_inicio)
                tempo_espera_total += soma_duracao - (processo[0] - tempo_inicio)
            soma_duracao += processo[1] # Acumula a duracao de cada processo
            tempo_retorno_total += soma_duracao - (processo[0] - tempo_inicio)

        return self.calcular_medias(tempo_retorno_total, tempo_resposta_total, tempo_espera_total, processos)

    def calcular_medias(self, retorno_total, resposta_total, espera_total, processos):
        num_processos = len(processos)
        retorno_medio = retorno_total / num_processos
        resposta_medio = resposta_total / num_processos
        espera_medio = espera_total / num_processos

        # convertendo para string, substitui ponto por virgula, com uma casa decimal
        retorno_medio = ("%.1f" % retorno_medio).replace('.', ',')
        resposta_medio = ("%.1f" % resposta_medio).replace('.', ',')
        espera_medio = ("%.1f" % espera_medio).replace('.', ',')

        return retorno_medio, resposta_medio, espera_medio # Retorna os tempos médios formatados

# SMALLEST JOB FIRST
class SJF:
    def execute(self, processos):

        procs = copy.deepcopy(processos) # Cria uma copia da lista de processos para evitar alterações na lista original
        tempo_retorno_total, tempo_resposta_total, tempo_espera_total = 0, 0, 0 # inicializacao dos tempos
        tempo_inicio = processos[0][0] # Armazena o instante de chegada do primeiro processo
        tempo_atual, soma_duracao = tempo_inicio, 0  # Inicializa o tempo atual com o instante de chegada do primeiro processo

        while procs:
            proximo = self.proximo_processo(procs, tempo_atual) # Busca o próximo processo a ser executado
            if proximo == -1: # Ocorrencia de vacuo. Não há processo com tempo de chegada <= ao tempo atual
                tempo_atual = procs[0] # Atualiza o tempo atual para o tempo de chegada do próximo processo na lista
            else:
                # Calcula o tempo de resposta e de espera do próximo processo
                tempo_resposta_total += soma_duracao - (procs[proximo][0] - tempo_inicio)
                tempo_espera_total += soma_duracao - (procs[proximo][0] - tempo_inicio)
                # Acumula a duração do próximo processo
                soma_duracao += procs[proximo][1]
                # Calcula o tempo de retorno do próximo processo
                tempo_retorno_total += soma_duracao - (procs[proximo][0] - tempo_inicio)
                tempo_atual += procs[proximo][1] # Adiciona a duração do próximo processo ao tempo atual
                procs.pop(proximo) # Remove o próximo processo da lista
        
        return self.calcular_medias(tempo_retorno_total, tempo_resposta_total, tempo_espera_total, processos)

    def proximo_processo(self, procs, ta): # busca o proximo indice a ser executado 
        menor_duracao = None
        index_melhor = -1

        for index, p in enumerate(procs):
            if p[0] <= ta: # Se no instante atual o processo já entrou no sistema
                # Se for o primeiro processo com tempo <= tempo_atual
                if menor_duracao is None or p[1] < menor_duracao or (p[1] == menor_duracao and p[0] < procs[index_melhor][0]):
                    menor_duracao = p[1]
                    index_melhor = index

        return index_melhor

    def calcular_medias(self, retorno_total, resposta_total, espera_total, processos):
        num_processos = len(processos)
        retorno_medio = retorno_total / num_processos
        resposta_medio = resposta_total / num_processos
        espera_medio = espera_total / num_processos

        retorno_medio = ("%.1f" % retorno_medio).replace('.', ',')
        resposta_medio = ("%.1f" % resposta_medio).replace('.', ',')
        espera_medio = ("%.1f" % espera_medio).replace('.', ',')

        return retorno_medio, resposta_medio, espera_medio

# ROUND ROBIN 
class RR:
    def execute(self, processos, quantum):

        procs = [list(p) for p in processos]  # Converter processos para lista temporariamente
        tempo_retorno_total, tempo_resposta_total, tempo_espera_total = 0, 0, 0
        tempo_inicio = processos[0][0] # Armazena o instante de chegada do primeiro processo
        tempo_atual, soma_duracao = tempo_inicio, 0 # Inicializa o tempo atual com o instante de chegada do primeiro processo
        num_processos = len(processos) # Número total de processos

        while procs:
            while True: # Loop para buscar o próximo processo a ser executado
                if procs[0][0] < tempo_atual or procs[0][0] == tempo_inicio:
                    break
                else: # Movimenta o processo para o final da fila
                    p = procs[0]
                    procs.pop(0)
                    procs.append(p)

            if -1 not in procs[0]: # Marcação de que o processo já foi executado uma vez
                procs[0].append(-1)
                tempo_resposta_total += tempo_atual - procs[0][0]

            if procs[0][1] <= quantum: # Se a duração do processo for menor ou igual ao quantum
                tempo_atual += procs[0][1]
                tempo_retorno_total += tempo_atual - procs[0][0]
                for index, proc in enumerate(procs): # Atualiza o tempo de espera para todos os processos, exceto o primeiro
                    if index != 0 and proc[0] < tempo_atual:
                        tempo_espera_total += min(quantum, tempo_atual - proc[0])
                procs.pop(0)
            else: # Se a duração do processo for maior que o quantum
                procs[0][1] -= quantum
                tempo_atual += quantum
                for index, proc in enumerate(procs): # Atualiza o tempo de espera para todos os processos, exceto o primeiro
                    if index != 0 and proc[0] < tempo_atual:
                        tempo_espera_total += min(quantum, tempo_atual - proc[0])
                # Movimenta o processo para o final da fila
                p = procs[0] 
                procs.pop(0)
                procs.append(p)

        # Calcula os tempos médios de retorno, resposta e espera
        retorno_medio = tempo_retorno_total / num_processos
        resposta_medio = tempo_resposta_total / num_processos
        espera_medio = tempo_espera_total / num_processos

        # Formata os tempos médios para uma casa decimal, substituindo ponto por vírgula
        retorno_medio = ("%.1f" % retorno_medio).replace('.', ',')
        resposta_medio = ("%.1f" % resposta_medio).replace('.', ',')
        espera_medio = ("%.1f" % espera_medio).replace('.', ',')

        return retorno_medio, resposta_medio, espera_medio # Retorna os tempos médios formatados



def main():
    entrada = input("Insira os processos no formato 'chegada1 duracao1 chegada2 duracao2 ...' e pressione Enter:\n")
    entradas = entrada.split()  # Dividir a entrada em uma lista de strings
    processos = [(int(entradas[i]), int(entradas[i+1])) for i in range(0, len(entradas), 2)]  # Converter cada par de valores em uma tupla de inteiros

    fcfs = FCFS()
    fcfs_result = fcfs.execute(processos)

    sjf = SJF()
    sjf_result = sjf.execute(processos)

    rr = RR()
    rr_result = rr.execute(processos, 2)

    saida_fcfs = "FCFS {0} {1} {2}".format(*fcfs_result)
    saida_sjf = "SJF {0} {1} {2}".format(*sjf_result)
    saida_rr = "RR {0} {1} {2}".format(*rr_result)
    saida = "{0}\n{1}\n{2}".format(saida_fcfs, saida_sjf, saida_rr)

    print(saida)

if __name__ == '__main__':
    main()
