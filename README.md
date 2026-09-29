# BB84 From Scratch

BB84를 단순 확률 모델부터 NumPy 기반 qubit 벡터 표현까지 직접 구현하며 배우는 프로젝트다. 동작하는 코드를 만드는 것뿐 아니라, 측정 결과가 왜 그렇게 나오는지 계산하고 실험하면서 이해하는 과정을 기록한다.

## Learning Log

### 2026-09-29 — 랜덤으로 흉내 내던 양자 측정을 qubit 벡터로 이해하기

#### 오늘의 목표

기존에는 BB84의 규칙을 조건문으로 옮겼다. Alice가 random bit와 random basis를 만들고 Bob도 random basis를 고른다. 두 basis가 같으면 Alice의 bit를 그대로 얻고, 다르면 `random.randint(0, 1)`로 결과를 뽑았다.

이 방식으로 Sifted Key와 QBER까지 계산할 수 있었지만, “basis가 다르면 왜 랜덤인가?”라는 질문에는 코드 자체가 답하지 못했다. 오늘은 네 가지 qubit 상태를 벡터로 표현하고, 상태와 측정 basis로부터 확률을 구해 같은 동작이 나오는지 이해하는 데 집중했다. 실제 양자 하드웨어를 사용하는 단계가 아니라, 고전 컴퓨터에서 상태 벡터와 측정 확률을 계산하는 시뮬레이션이다.

#### 구현한 내용

현재 파일을 확인한 기준으로 구현 상태는 다음과 같다. 파일 번호가 있다고 해서 모든 단계가 채워진 것은 아니다.

| 위치 | 현재 내용 |
| --- | --- |
| `basic/step01_alice_bits.py` | Alice의 bit·basis, Bob의 basis 생성과 확률 기반 측정 |
| `basic/step04_sifted_key.py` | basis가 일치하는 위치에서 두 사람의 Sifted Key 추출 |
| `basic/step05_qber.py` | Sifted Key 기준 오류 수와 QBER 계산 |
| `attack/step06_eve_attack.py` | 단순 확률 모델의 Eve intercept-resend 공격 |
| `attack/step08_statistics.py` | 공격 모델을 100회 반복하고 QBER 평균·최솟값·최댓값 계산 |
| `quantum/step09_qubit_vector.py` | NumPy 상태 벡터, 상태 준비·측정, Sifted Key와 QBER 출력 |
| `basic/step02_alice_basis.py`, `basic/step03_bob_measure.py`, `attack/step07_qber_experiment.py`, `qiskit/step10_qiskit_bb84.py` | 아직 빈 파일 |
| `experiments/`, `requirements.txt` | 추가 실험 폴더와 의존성 목록은 아직 비어 있음 |

통계 코드의 주석에는 `run_bb84(1000)`이라고 적혀 있지만, 실제 호출은 `run_bb84(100000)`이다. 현재 실험 규모는 한 번에 100,000개 전송, 총 100회다.

벡터 구현에서는 `basis=0`을 Z, `basis=1`을 X로 사용한다. 네 상태는 다음과 같이 만들었다.

```python
zero = np.array([1, 0])
one = np.array([0, 1])
value = 1 / np.sqrt(2)
plus = np.array([value, value])
minus = np.array([value, -value])
```

`prepare_qubit()`은 보내려는 bit와 준비 basis를 받아 상태 벡터를 반환한다. 아래는 현재 구현이다.

```python
def prepare_qubit(bit, basis):
    if bit == 0 and basis == 0:
        return zero
    elif bit == 1 and basis == 0:
        return one
    elif bit == 0 and basis == 1:
        return plus
    elif bit == 1 and basis == 1:
        return minus
```

Alice의 bit·basis 리스트를 이 함수로 변환해 `alice_qubits`에 저장하고, Bob은 자신의 basis로 각 벡터를 `measure_qubit()`에 전달한다. 이제 측정 함수는 Alice의 원래 bit나 basis를 직접 비교하지 않는다. 입력 상태와 Bob의 측정 basis로 확률을 계산한다.

#### 공부하면서 막힌 부분

**“bit를 이미 0과 1로 정해버리면 그게 양자화라고 할 수 있는가?”**

처음에는 qubit이라면 무조건 0과 1이 50:50으로 존재해야 한다고 생각했다. 그래서 Alice가 처음부터 bit를 정하는 것이 이상하게 느껴졌다.

여기서 구분해야 했던 것은 **전달하려는 고전 정보**와 **그 정보를 담도록 준비한 양자 상태**였다. bit 0은 Z basis에서 $|0\rangle$로, X basis에서 $|+\rangle$로 준비할 수 있다. bit 1도 각각 $|1\rangle$, $|-\rangle$에 대응한다. Alice가 메시지의 bit를 정했다는 사실과 Bob의 측정 결과가 항상 확정된다는 것은 다른 이야기였다.

특히 50:50은 상태만 보고 붙이는 성질이 아니었다. $|0\rangle$도 Z로 측정하면 0이 확정적이지만, X로 측정하면 두 결과가 반반이다. 반대로 $|+\rangle$는 X로 측정하면 bit 0이 확정적이고 Z로 측정하면 반반이다.

**“Z basis로 보내더라도 Bob의 basis가 다르면 왜 랜덤 결과가 나오는가?”**

기존 코드에서는 basis가 다르면 랜덤이라고 직접 정했다. 벡터로 바꾸면서 그 규칙의 근거를 계산하기 시작했다. 예를 들어 $|0\rangle=[1,0]$을 X로 측정할 때, 가능한 결과는 $|+\rangle$와 $|-\rangle$다.

$$
\langle +|0\rangle = \frac{1}{\sqrt{2}}\cdot1 + \frac{1}{\sqrt{2}}\cdot0 = \frac{1}{\sqrt{2}}
$$

$$
P(+) = |\langle +|0\rangle|^2 = \frac12,\qquad
P(-) = |\langle -|0\rangle|^2 = \frac12
$$

같은 basis에서는 준비한 상태에 해당하는 결과가 확정적이고, BB84의 서로 다른 Z·X basis에서는 두 결과의 확률이 같아진다. 이전의 `random.randint(0, 1)`은 이 경우의 측정 통계를 간단히 흉내 낸 것이었다.

**“`np.dot()`은 무엇을 계산하는가?”**

처음에는 내적이라는 말 자체가 잘 와닿지 않았다. 지금 사용하는 실수 1차원 배열에서는 같은 위치의 성분을 곱하고 더하는 계산이다.

```python
overlap_plus = np.dot(plus, qubit)
prob_0 = overlap_plus ** 2
```

현재 상태가 X basis의 $|+\rangle$와 얼마나 겹치는지 계산한 값은 **확률 진폭**이다. 그 값 자체가 확률은 아니며, 절댓값의 제곱이 $|+\rangle$, 즉 X basis의 bit 0을 얻을 확률이 된다. $|0\rangle$을 넣어 약 0.5가 나오는 것을 확인하면서 내적과 측정 확률이 연결되기 시작했다.

현재 네 상태는 모두 실수이므로 코드의 단순 제곱으로 충분하다. 일반적인 복소수 상태까지 확장하면 내적에는 복소켤레가 필요하므로 `np.vdot(plus, qubit)`과 `abs(overlap) ** 2`를 사용해야 한다. 이 확장은 아직 구현하지 않았다.

**“왜 X basis 측정에서는 plus만 계산하고 minus는 계산하지 않는가?”**

처음에는 두 상태가 있으니 내적도 두 번 해야 한다고 생각했다. 하지만 정규화된 qubit을 X basis로 측정하면 가능한 결과는 $|+\rangle$와 $|-\rangle$뿐이고, 두 확률의 합은 1이다.

$$
P(-)=1-P(+)
$$

따라서 $P(+)$만 구하면 나머지는 자동으로 정해진다. Z basis에서 $P(0)$만 구하고 남은 확률을 $P(1)$로 처리하는 것과 같은 방식이다.

**“확률을 구한 다음, 실제 결과 하나는 어떻게 뽑는가?”**

먼저 `prob_0 = 0.5`로 고정하고 `random.random()`으로 1,000번 결과를 뽑아 봤다. 이 함수가 만드는 0 이상 1 미만의 값이 `prob_0`보다 작으면 0, 그렇지 않으면 1로 처리했다. 학습 중 얻은 결과는 484:516, 다른 실행에서는 498:502였다.

확률이 0.5라는 것과 매번 정확히 절반씩 나온다는 것은 달랐다. 확률을 계산하는 단계와, 그 확률에 따라 결과 하나를 샘플링하는 단계를 구분하게 됐다. 이 과정을 현재 측정 함수에 넣었다.

```python
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
```

**“Sifted Key가 같다고 나오면 구현이 맞는 것 아닌가?”**

처음에는 `bob_key`에도 실수로 `alice_bits[i]`를 넣었다. 그러면 Bob이 무엇을 측정했든 두 키는 같아져서 검증 의미가 없어진다. Bob의 키에는 실제 측정값인 `bob_result[i]`를 넣어야 했다. 현재 소스에는 이 수정이 반영되어 있다.

```python
if alice_basis[i] == bob_basis[i]:
    alice_key.append(alice_bits[i])
    bob_key.append(bob_result[i])
```

**“QBER의 분모는 전체 전송 bit 수인가?”**

처음에는 `error_count / len(alice_bits)`로 계산했다. 하지만 비교하는 오류는 basis가 일치해 남겨 둔 키에서 센 것이므로, 분모도 전체 전송 수가 아니라 Sifted Key 길이여야 한다.

$$
\mathrm{QBER}=\frac{\text{Sifted Key에서 서로 다른 bit 수}}{\text{Sifted Key 길이}}
$$

학습하면서 확인한 올바른 계산은 다음과 같다. **아래는 수정해야 할 식이며, 현재 벡터 파일에 반영된 코드가 아니다.**

```python
# alice_key가 비어 있지 않을 때
QBER = error_count / len(alice_key)
```

README 작성 시 확인한 `quantum/step09_qubit_vector.py`에는 아직 `len(alice_bits)`가 남아 있다. 반면 기존 `basic/step05_qber.py`와 공격 모델은 `len(alice_key)`를 사용한다. Eve가 없어 오류 수가 0이면 잘못된 분모로도 결과가 0.0이라서, 출력만 보고 이 실수를 놓칠 수 있었다. Sifted Key가 비어 있으면 QBER는 정의할 수 없으므로 그 경우의 처리도 필요하다.

#### 이해하게 된 핵심 개념

오늘 가장 크게 바뀐 것은 qubit을 “항상 반반인 bit”로 보던 관점이다. 상태 준비에 쓰는 bit, 상태 벡터의 진폭, 특정 basis로 측정할 때의 확률, 실제로 얻은 측정 결과는 서로 다른 단계였다.

| 준비한 상태 | Z 측정: P(0), P(1) | X 측정: P(0), P(1) |
| --- | --- | --- |
| $|0\rangle$ | 1, 0 | 1/2, 1/2 |
| $|1\rangle$ | 0, 1 | 1/2, 1/2 |
| $|+\rangle$ | 1/2, 1/2 | 1, 0 |
| $|-\rangle$ | 1/2, 1/2 | 0, 1 |

벡터 성분은 확률이 아니라 진폭이다. $|-\rangle$의 음수 성분도 음수 확률이라는 뜻이 아니다. 상대적인 부호가 내적에 영향을 주어 X 측정에서 $|+\rangle$와 구별된다. 정규화는 진폭의 절댓값 제곱 합이 1이라는 조건이며, 현재 코드에서도 네 상태의 성분 제곱 합을 계산한다.

기존 구현은 측정 결과의 규칙을 조건문에 직접 넣었다. 벡터 구현은 상태와 측정 basis의 관계로 확률을 계산한 다음 결과를 샘플링한다. 난수를 없앤 것이 아니라, **어떤 확률로 난수를 사용해야 하는지 상태에서 계산하도록 바꾼 것**이다.

현재 `measure_qubit()`은 bit만 반환하며 측정 후 상태 벡터를 갱신하거나 반환하지 않는다. Bob의 단일 측정에는 이 구조를 사용하고 있고, Eve가 측정한 뒤 어떤 상태를 다시 보내야 하는지는 다음 단계에서 다룰 예정이다.

#### 실험 결과

아래 수치는 오늘 학습 중 관찰한 결과를 기록한 것이다. README 작성 과정에서 새로 실행해 얻은 수치가 아니며, 1,000회 샘플링 실험의 별도 스크립트나 출력 로그는 현재 프로젝트에 저장되어 있지 않다.

| 실험 | 학습 중 확인한 결과와 해석 |
| --- | --- |
| `prob_0 = 0.5`, 1,000회 샘플링 | 0:1이 484:516, 다른 실행에서 498:502. 정확히 절반은 아니지만 50:50에 가까웠다. |
| 같은 basis로 준비·측정 | 준비한 bit에 해당하는 결과를 얻었다. 이론적 확률은 1이다. |
| 다른 basis로 준비·측정 | 두 결과가 약 50:50으로 나오는 것을 확인했다. |
| Eve 없는 벡터 기반 BB84 | 두 Sifted Key가 같았고 QBER 출력은 0.0이었다. 다만 현재 소스의 분모 오류까지 검증한 결과는 아니다. |
| 확률 모델의 intercept-resend 반복 실험 | QBER가 약 25%에 가까워지는 것을 확인했다. 정확한 평균·최솟값·최댓값은 이 기록에 남기지 않았다. |

Eve가 모든 qubit을 가로채 무작위 basis로 측정하고 다시 보내는 이상적 모델에서는, Sifted Key에 남는 위치를 기준으로 Eve가 잘못된 basis를 고를 확률이 1/2이고 그 경우 Bob의 bit가 틀릴 확률이 1/2이다. 따라서 기대 QBER는 다음과 같다.

$$
\frac12\times\frac12=\frac14=25\%
$$

이 공격 실험은 `attack/`의 **단순 확률 모델**에서 진행한 것이다. 현재 벡터 기반 파일은 `N = 10`인 Eve 없는 구현이며, 벡터 기반 공격 실험까지 완료한 것은 아니다. 또한 샘플 수를 늘리면 비율이 이론값에 가까워지는 경향이 있지만, 매 실행마다 오차가 반드시 줄어드는 것은 아니다.

#### 오늘의 정리

오늘은 BB84의 규칙을 코드로 따라 쓰는 단계에서, 그 규칙을 상태 벡터와 내적으로 설명하는 단계로 넘어갔다. 처음 이상하게 느꼈던 “bit를 정했는데 왜 결과가 랜덤이지?”라는 질문은 준비한 상태와 측정 basis를 구분하면서 풀리기 시작했다.

내적으로 확률 진폭을 구하고, 제곱해서 확률을 얻고, 난수로 결과 하나를 선택하는 흐름이 연결됐다. Sifted Key와 QBER에서도 결과가 그럴듯한지뿐 아니라 실제로 누구의 값을 비교하는지, 어떤 집합을 분모로 삼는지를 확인해야 한다는 것을 배웠다.

#### 다음 목표

다음에는 **벡터 기반 BB84에 Eve의 intercept-resend 공격을 추가**한다. 아직 구현하지 않은 단계이며, 다음 순서로 진행할 예정이다.

1. 현재 벡터 코드의 QBER 분모를 `len(alice_key)`로 수정하고, Sifted Key가 비었을 때의 처리를 추가한다.
2. Eve가 각 qubit마다 random basis를 선택하고 `measure_qubit()`으로 측정하게 한다.
3. Eve의 측정 bit와 basis를 `prepare_qubit()`에 넣어 재전송할 상태를 준비한다. Alice의 원래 벡터를 그대로 Bob에게 넘기지 않도록 한다.
4. Bob이 재전송된 상태를 자신의 basis로 측정한 뒤, Alice와 Bob의 basis가 일치하는 위치에서 키와 QBER를 계산한다.
5. 전송 수와 반복 횟수를 늘려 Eve가 없을 때의 QBER 0과, 모든 신호를 intercept-resend했을 때의 약 25%를 비교한다.

이를 통해 기존 확률 모델에서 관찰한 오류율을 벡터 기반 상태 준비와 측정으로도 설명할 수 있는지 확인하려고 한다.
