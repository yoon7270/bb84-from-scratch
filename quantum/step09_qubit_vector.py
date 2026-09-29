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

N = 10

alice_bits = []
alice_basis = []
bob_basis = []
bob_result = []

for _ in range(N):
    alice_bits.append(random.randint(0, 1))
    alice_basis.append(random.randint(0, 1))
    bob_basis.append(random.randint(0, 1))

alice_qubits = []

for i in range(N):
    # alice_bits[i]
    # alice_basis[i]
    # prepare_qubit() 사용
    alice_qubits.append(prepare_qubit(alice_bits[i], alice_basis[i]))

for i in range(N):
    # alice_bits[i]
    # alice_basis[i]
    # prepare_qubit() 사용
    bob_result.append(measure_qubit(alice_qubits[i], bob_basis[i]))

for i in range(N):
    print(
        "alice bit:", alice_bits[i],
        "alice basis:", alice_basis[i],
        "qubit:", alice_qubits[i],
        "bob basis:", bob_basis[i],
        "bob result:", bob_result[i]
    )

alice_key = []
bob_key = []
error_count = 0

for i in range(N):
    if alice_basis[i] == bob_basis[i]:
        alice_key.append(alice_bits[i])
        bob_key.append(bob_result[i])

for i in range(len(alice_key)):
    if alice_key[i] != bob_key[i]:
        error_count += 1



QBER = error_count / len(alice_bits)

print(QBER)
