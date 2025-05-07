import numpy as np
from qiskit.quantum_info import Statevector
from numpy import sqrt
import math
from qiskit.quantum_info import Operator

# Operators to chose from
I = Operator(np.array([[1,0],[0,1]]))
X = Operator(np.array([[0,1],[1,0]]))
Y = Operator(np.array([[0,-1.0j],[1.0j,0]]))
Z = Operator(np.array([[1,0],[0,-1]]))
S = Operator(np.array([[1,0],[0,1.0j]]))
T = Operator(np.array([[1,0],[0,(1+1.0j)/sqrt(2)]]))
H = Operator(np.array([[1/sqrt(2),1/sqrt(2)],[1/sqrt(2),-1/sqrt(2)]]))

# Because I get list of strings and func is expecting operators

gate_dict = {"I": I, "X": X, "Y": Y, "Z": Z, "S": S, "T": T, "H": H}


def quantum_message(n_gates, gates):
    qubit = Statevector([1,0])
    iterations = 0
    if n_gates == 1:
        iterations = 8
    elif n_gates == 2:
        iterations = 4
    elif n_gates == 3:
        iterations = 8
    elif n_gates == 4:
        iterations = 2
    elif n_gates == 5:
        iterations = 8
    elif n_gates == 6:
        iterations = 4
    elif n_gates == 7:
        iterations = 8
    else:
        raise ValueError("possible number of gates: 1-7")

    binary_message = []

    for _ in range(iterations):
        for gate in gates:
            qubit = qubit.evolve(gate)
            outcome, qubit = qubit.measure()
            binary_message.append(int(outcome))

    text = ''
    for j in range(0, len(binary_message), 8):
        byte = binary_message[j:j + 8]
        binary_string = ''.join(str(bit) for bit in byte)
        character = chr(int(binary_string, 2))
        text += character

    return text, qubit, binary_message


def pretty_print_statevector(statevector):
    coeffs = statevector.data
    basis = ['|0⟩', '|1⟩']
    threshold = 1e-2  # tolerancija za prepoznavanje 1/sqrt(2)

    terms = []

    for coeff, base in zip(coeffs, basis):
        if np.abs(coeff) > 1e-6:  # ignorišemo skoro nule
            real = np.round(coeff.real, 3)
            imag = np.round(coeff.imag, 3)

            if np.abs(real - 1/np.sqrt(2)) < threshold:
                real_str = "1/√2"
            elif np.abs(real + 1/np.sqrt(2)) < threshold:
                real_str = "-1/√2"
            elif real != 0:
                real_str = f"{real}"
            else:
                real_str = ""

            if np.abs(imag - 1/np.sqrt(2)) < threshold:
                imag_str = "+1/√2j"
            elif np.abs(imag + 1/np.sqrt(2)) < threshold:
                imag_str = "-1/√2j"
            elif imag != 0:
                imag_str = f"{'+' if imag > 0 else '-'}{abs(imag)}j"
            else:
                imag_str = ""

            if real_str and imag_str:
                term = f"({real_str}{imag_str}){base}"
            elif real_str:
                term = f"{real_str}{base}"
            elif imag_str:
                term = f"{imag_str}{base}"
            else:
                term = ""

            terms.append(term)

    if not terms:
        return "0"

    # Lepo formatiranje + i -
    formatted_terms = []
    for i, term in enumerate(terms):
        if i == 0:
            formatted_terms.append(term)
        else:
            if term.startswith('-'):
                formatted_terms.append(f"- {term[1:]}")
            else:
                formatted_terms.append(f"+ {term}")

    return ' '.join(formatted_terms)


if __name__ == '__main__':

    user_input = ""
    chosen_gates = []
    while user_input != "EXIT":
        chosen_gates = []
        num_gates = int(input("Number of gates (1-7): "))
        for i in range(int(num_gates)):
            ac_gate = input(f"Choose gate {i + 1}: \nI\nX\nY\nZ\nS\nT\nH\n").upper()
            if ac_gate in gate_dict:
                chosen_gates.append(gate_dict[ac_gate])
            else:
                print(f"Invalid gate {ac_gate}. Try again.")

        answer = input("Your initial qubit state is:|0⟩\nDo you want to apply quantum gates to it?")
        if answer == "YES":
            text_message, final_state, binary_text = quantum_message(num_gates, chosen_gates)
            print(f"Your binary message is : {binary_text}")
            print(f"Your quantum message is {text_message}")
            print(f"Your qubit final quantum state after all operations and measurements: "
                  f"{pretty_print_statevector(final_state)}")

        elif answer == "NO":
            exit()

