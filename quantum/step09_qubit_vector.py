import numpy as np
import random
def prepare_qubit(bit, basis):
    if bit == 0 and basis == 0:
        return zero
    elif bit == 1 and basis == 0:
        return one
    elif bit == 0 and basis == 1:
        return plus
    elif bit == 1 and basis == 1:
        return minus

def measure_qubit(qubit, basis):
    if basis == 0:
        prob_0 = qubit[0] ** 2
    else:
        overlap_plus = np.dot(plus, qubit)
        prob_0 = overlap_plus ** 2
    r = random.random()

    if prob_0 > r:
        return 0
    else:
        return 1



zero = np.array([1, 0])
one = np.array([0, 1])

zero_normalization = zero[0] ** 2 + zero[1] ** 2
one_normalization = one[0] ** 2 + one[1] ** 2

value = 1 / np.sqrt(2)

plus = np.array([value, value])
plus_normalization = plus[0] ** 2 + plus[1] ** 2

minus = np.array([value, -value])
minus_normalization = minus[0] ** 2 + minus[1] ** 2

qubit = prepare_qubit(0, 1)  # |+>

prob_0 = qubit[0] ** 2
prob_1 = qubit[1] ** 2


def run_bb84(N):
    alice_qubits = []
    alice_bits = []
    alice_basis = []
    alice_key = []

    bob_basis = []
    bob_result = []
    bob_key = []

    eve_qubits = []
    eve_basis = []
    eve_results = []
    eve_qubits = []

    error_count = 0

    for _ in range(N):
        alice_bits.append(random.randint(0, 1))
        alice_basis.append(random.randint(0, 1))
        bob_basis.append(random.randint(0, 1))
        eve_basis.append(random.randint(0, 1))

    for i in range(N):
        # alice_bits[i]
        # alice_basis[i]
        # prepare_qubit() 사용
        alice_qubits.append(prepare_qubit(alice_bits[i], alice_basis[i]))

    for i in range(N):
        # alice_qubits[i]
        # eve_basis[i]
        # measure_qubit() 사용
        eve_results.append(measure_qubit(alice_qubits[i], eve_basis[i]))

    for i in range(N):
        # eve_results[i]
        # eve_basis[i]
        # prepare_qubit() 사용
        eve_qubits.append(prepare_qubit(eve_results[i], eve_basis[i]))

    for i in range(N):
        bob_result.append(measure_qubit(eve_qubits[i], bob_basis[i]))


    for i in range(N):
        if alice_basis[i] == bob_basis[i]:
            alice_key.append(alice_bits[i])
            bob_key.append(bob_result[i])

    for i in range(len(alice_key)):
        if alice_key[i] != bob_key[i]:
            error_count += 1

    QBER = error_count / len(alice_key)
    return QBER

qbers = []

for _ in range(100):
    qbers.append(run_bb84(1000))

average_qber = sum(qbers) / len(qbers)

print("Average QBER:", average_qber)
print("Average QBER %:", average_qber * 100)

# print("Alice bits :", alice_bits)
# print("Alice basis:", alice_basis)
# print("Eve basis  :", eve_basis)
# print("Eve result :", eve_results)
# print("Bob basis  :", bob_basis)
# print("Bob result :", bob_result)
