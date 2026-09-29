import random

def run_bb84(N):
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

    return QBER


qber_results = []

# run_bb84(1000)을 100번 실행
for _ in range(100):
    qber = run_bb84(100000)
# 반환된 값을 qber_results에 저장
    qber_results.append(qber)
average_qber = sum(qber_results) / len(qber_results)
lowest_qber = min(qber_results)
highest_qber = max(qber_results)

print("실험 횟수:", len(qber_results))
print("평균 QBER:", average_qber)
print("최저 QBER(%):", lowest_qber * 100)
print("평균 QBER(%):", average_qber * 100)
print("최고 QBER(%):", highest_qber * 100)
