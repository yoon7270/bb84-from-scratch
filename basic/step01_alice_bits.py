import random

N = 10

alice_bits = []
alice_basis = []

bob_basis = []
bob_results = []

# 여기를 직접 구현
for _ in range(N):
    # Alice bit 생성
    alice_bits.append(random.randint(0,1))
    # Alice basis 생성
    alice_basis.append(random.randint(0,1))
    # bob_basis 생성
    bob_basis.append(random.randint(0,1))

for i in range(N):
    if alice_basis[i] == bob_basis[i]:
        bob_results.append(alice_bits[i])
    else:
        bob_results.append(random.randint(0,1))
print("Alice bits:", alice_bits)
print("Alice basis:", alice_basis)
print("bob_basis:", bob_basis)
print("bob_results:", bob_results)