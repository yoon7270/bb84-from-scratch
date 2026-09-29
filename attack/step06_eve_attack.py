import random

N = 100000

alice_bits = []
alice_basis = []

bob_basis = []
bob_results = []

alice_key = []
bob_key = []

eve_basis = []
eve_results = []

error_count = 0

# 여기를 직접 구현
for _ in range(N):
    # Alice bit 생성
    alice_bits.append(random.randint(0,1))
    # Alice basis 생성
    alice_basis.append(random.randint(0,1))
    # bob_basis 생성
    bob_basis.append(random.randint(0,1))
    # eve_basis 생성
    eve_basis.append(random.randint(0,1))

for i in range(N):
    if alice_basis[i] == eve_basis[i]:
        eve_results.append(alice_bits[i])
    else:
        eve_results.append(random.randint(0,1))

for i in range(N):
    if bob_basis[i] == eve_basis[i]:
        bob_results.append(eve_results[i])
    else:
        bob_results.append(random.randint(0,1))

for j in range(N):
    if alice_basis[j] == bob_basis[j]:
        alice_key.append(alice_bits[j])
        bob_key.append(bob_results[j])

for k in range(len(alice_key)):
    if alice_key[k] != bob_key[k]:
        error_count += 1

QBER = error_count / len(alice_key)

print("Sifted key length:", len(alice_key))
print("Error count:", error_count)
print("QBER:", QBER)
print("QBER(%):", QBER * 100)