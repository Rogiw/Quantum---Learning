from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import pandas as pd
import numpy as np


def bell_state(qc):

    qc = qc.copy()
    #aplicando a porta hadamard no primeiro qubit
    qc.h(0)

    #aplicando a porta cnot no segundo qubit, controlado pelo primeiro
    qc.cx(0, 1) # porta cnot, onde o primeiro qubit é o controle e o segundo é o alvo
  
    return qc

def simulate_bell_state(circuit):
    simulator = AerSimulator()
    compiled_circuit = transpile(circuit, simulator)
    result = simulator.run(compiled_circuit).result()
    counts = result.get_counts()
    return counts

def plot_bell_state(counts, titulo="Bell State"):
    
    print(f"Resultados para {titulo}: {counts}")
    plot_histogram(counts, title=titulo)
    plt.show()

def plot_bell_state(counts, titulo="Bell State"):
    print(f"Resultados para {titulo}: {counts}")
    fig = plot_histogram(counts, title=titulo)
    return fig

if __name__ == "__main__":
    n = int(input("Digite o número de qubits (n): "))
    combinacoes = [] #[000, 001, 010, 011, 100, 101, 110, 111] 2^n
                        #[00, 01, 10, 11] 2^n
                        #[0, 1] 2^n
    
    numero_de_combinacoes = 2 ** n
    for i in range(numero_de_combinacoes):
        combinacao = format(i, f'0{n}b') # converte o número i para uma string binária com n bits
        combinacoes.append(combinacao) 

    print(f"Combinacoes: {combinacoes}") 

    results = {}
    for combinacao in combinacoes:
        qc = QuantumCircuit(n, n)  # reset por combinação
        for i, bit in enumerate(combinacao):
            print(i , bit)
            if bool(int(bit)):
                qc.x(i)
        qc = bell_state(qc)
        qc.measure(range(n), range(n))
        counts = simulate_bell_state(qc)
        results[combinacao] = counts
        print(qc)

   # ======= UI INTERATIVA =======

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.3)

    first_key = combinacoes[0]
    plot_histogram(results[first_key], title=first_key, ax=ax)

    # rádio buttons (lista de combinações)
    rax = plt.axes([0.05, 0.3, 0.2, 0.5])
    radio = RadioButtons(rax, combinacoes)

    def update(label):
        ax.clear()
        plot_histogram(results[label], title=label, ax=ax)
        fig.canvas.draw_idle()

    radio.on_clicked(update)

    plt.show()
        