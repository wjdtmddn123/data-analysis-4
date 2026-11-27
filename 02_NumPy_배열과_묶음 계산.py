import csv
import os
import numpy as np


def dp(name):
    """
    실행 위치가 어디든 data 폴더를 찾아 주는 작은 도우미 함수
    """
    here = os.path.dirname(os.path.abspath(__file__))
    for c in (
        os.path.join("data", name),
        os.path.join(here, "data", name),
        os.path.join(here, "..", "data", name),
    ):
        if os.path.exists(c):
            return c
    return os.path.join("data", name)


MCT = dp("10_mct_tool.csv")  # 40행 6열 오늘 쓰는 유일한 데이터 파일

# ======================================================
# 0. 리스트로는 왜 안 되나 - 곱셈이 곱셈이 아닌 장면
# ======================================================
#
# 상황) 온도 네 개를 재 뒀습니다. 전부 두 배로 만들고 싶어요.
print("=" * 60)
print("[0] 리스틀로 묶음 계산을 해 보면")
temps = [30, 30, 31, 29]
temps2 = [5, 6, 7, 8]
doubled = []
for t in temps:
    doubled.append(t * 2)
print(doubled)
print(temps * 2)

# 같은 일을 배열로 해 봅니다.
print("[0-1] 같은 일을 배열로")
arr = np.array(temps)
arr2 = np.array(temps2)
print("배열:", arr)
print("arr * 2 :", arr * 2)
print("arr + 5 :", arr + 5)
print("화씨로 바꾸기:", arr * 1.8 + 32)
print("배열 곱 가능 ?:", arr * arr2)

# 그럼 for 로 하면 되는데 왜 NumPy 를 쓰나?
# for 로 한 줄이 아니라 세 줄이 들었습니다 (빈 리스트 만들기 / for / append).
# 값 네 개라 세 줄이면 되는데, 40개여도 세 줄이고 400만 개여도 세 줄입니다.
# 줄 수가 문제가 아닙니다. 문제는 두 가지입니다.
# 1) 하고 싶은 일(두 배로)이 코드에 안 보입니다. 상 차리는 코드에 묻힙니다.
# 2) 느립니다. 400만 개를 파이썬 for 로 돌리는 것과 NumPy 로 하는 것은
#    속도가 수십 배 차이 납니다. - 오늘 측정하지 않습니다.
#    다음에 실제로 시간을 재 봅니다. 오늘은 "느리다" 까지만.

# ======================================================
# 1. 리스트와 배열은 무엇이 다른가 - 자료형이 하나로 통일됩니다.
# ======================================================
# 배열(array) = 같은 자료형의 숫자를 줄줄이 담아 두고,
# 묶음 전체에 계산을 한 번에 걸 수 있게 만든 그릇.
# 정식 이름은 ndarray입니다. (n차원 배열).
# 화면에 type()을 찍으면 ndarray 라고 나오는 게 그래서입니다.
#
# 비유: 반 아이들을 일으켜 세운다고 해 봅시다. for 문은 출석부를 펴고
# "김철수 일어서", "이영희 일어서..."를 40번 부르는 것이고
# 백터화는 "다 같이 일어서" 한 번 외치는 것입니다. 결과는 같은데
# 걸리는 시간이 다릅니다. 사람이 40명이든 400명이든 400만명이든 외치는 건 한 번이죠.
#
# 벡터화: for 문으로 하나씩 돌지 않고
# 묶음 전체를 한 번에 계산을 거는 방식. arr * 2 가 벡터화입니다.
# "벡터" 라는 말에 겁먹을 필요 없습니다. 여기서는 "줄줄이 늘어선 숫자 묶음"
# 이라는 뜻이고, 수학 수업의 화살표 벡터를 떠올리지 않아도 됩니다.
print("=" * 60)
print("[1] 리스트와 배열은 무엇이 다른가")
print("type(temps):", type(temps).__name__)
print("type(arr):", type(arr).__name__)
print("arr.dtype:", arr.dtype)

# 결정적인 차이 하나 - 리스트는 아무거나 섞어 담고, 배열은 못 담습니다.
box = [1, 2, 5, "삼십"]
print("리스트에 섞어 담기:", box, "/ 값의 자료형:", [type(v).__name__ for v in box])

mixed = np.array([1, 2, 3.5])
print("배열에 정수와 소수를 섞으면:", mixed, "/ dtype", mixed.dtype)


# 초보자가 가장 많이 내는 오류 - 대괄호를 빼먹는 것
# np.array(1,2,3)

# dtype(data type) = 그 배열이 담고 있는 자료형.
# int64 = 정수, float64 소수.


# ======================================================
# 2. 규칙적인 배열 - 손으로 적지 않고 만들기
# ======================================================
# 배열을 만들 때마다 값을 손으로 적을 수는 없습니다.
# 0부터 39까지 측정 순번을 만들려고 숫자 40개를 치지는 않잖아요.
# 그래서 규칙적인 배열을 만들어 주는 함수가 다섯 개 있습니다.
#
# np.arrange(시작, 끝, 간격) -> 간격을 정합니다. 끝값은 안 들어갑니다.
# np.linspace(시작, 끝, 개수) -> 개수를 정합니다. 끝값이 들어갑니다.
# np.zeros(개수) -> 전부 0
# np.ones(개수) -> 전부 1
# np.full(개수, 값) -> 전부 그 값
#
# * 두 개만 기억하면 됩니다 - arrange는 간격, linspace는 개수.
print("=" * 60)
print("[2] 규칙적인 배열을 한 줄로 만들기")
print("    np.arange(5)           :", np.arange(5))
print("    np.arange(0, 10, 2)    :", np.arange(0, 10, 2))
print("    np.arange(0, 1, 0.3)   :", np.arange(0, 1, 0.3))
print("    np.linspace(0, 1, 5)   :", np.linspace(0, 1, 5))
print("    np.linspace(0, 100, 5) :", np.linspace(0, 100, 5))
print("    np.zeros(3)            :", np.zeros(3))
print("    np.ones(3)             :", np.ones(3))
print("    np.full(3, 7)          :", np.full(3, 7))

# 끝 값이 들어가는냐 안 들어가느냐.
print()
print("[2-1] 끝값이 포함되나")
print("    np.arange(0, 12, 3)   :", np.arange(0, 12, 3), "<- 12 가 없습니다")
print("    np.linspace(0, 12, 5) :", np.linspace(0, 12, 5), "<- 12 가 있습니다")
print("    개수:", len(np.arange(0, 12, 3)), "개 /", len(np.linspace(0, 12, 5)), "개")
print("    dtype:", np.arange(0, 12, 3).dtype, "/", np.linspace(0, 12, 5).dtype)

# 언제 쓰나 (실무에서 자주 쓰는 순서대로)
# arrange: 측정, 순번, 줄 번호   오늘 씁니다.
# zeros: 결과를 담은 빈 그릇을 미리 만들 때 (크기를 알고 있을 때)
# linspace: 그래프의 가로축을 매끄럽게 만들 때. (시각화 하면서 들어감)
# ones, full: 1로 채워 두고 급해 갈 때 -> "아직 안 쟀음"을 -1 로 표시해 둘 때


# ======================================================
# 3. dtype - 배열 하나에는 한 가지 자료형만 (함정 1)
# ======================================================
# 1번에서 "배열은 자료형을 하나로 통일한다"고 했습니다.
# 그 성질이 조용한 사고를 하나 만듭니다. 지금 그걸 밟아 봅시다.
#
# 비유: 눈금이 1cm 단위뿐인 줄자를 떠올려 보세요.
# 2.7cm를 재면 그 자에는 2.7을 적을 자리가 없습니다. 2 라고 적게 되죠.
# 0.7이 없어진 게 아니라, 자가 그 사이를 적을 수 없는 겁니다.
# 정수 배열이 그 자입니다. 칸마다 정수만 적을 수 있어요.
# 깨지는 지점 - 사람이 그 자로 재면 보통 가까운 눈금, 즉 3으로 읽습니다.
# 그런데 파이썬은 가까운 쪽으로 안 갑니다. 소수점 아래를 그냥 떼어 2로 적어요.
# 그 차이가 4번에서 다루는 '버림과 반올림' 입니다. 지금은 "떼어 낸다" 까지만

print("=" * 60)
print("[3] 배열 하나에는 한 가지 자료형만 들어갑니다")
ints = np.array([1, 2, 3])
print("    ints        :", ints, "/ dtype", ints.dtype)
ints[0] = 2.7  # 정수 배열의 첫 칸에 소수를 넣어 봅니다
print("    ints[0] = 2.7 한 뒤:", ints, "<- 2.7 이 2 가 됐습니다")
print("    ints.dtype  :", ints.dtype, "<- 정수 배열은 끝까지 정수입니다")

flo = np.array([1.0, 2.0, 3.0])  # 같은 일을 실수 배열에 해 봅니다
flo[0] = 2.7
print("    실수 배열에 같은 일:", flo, "<- 이쪽은 2.7 이 그대로 들어갑니다")

print()
print("[3-1] 나눗셈은 자료형을 바꿉니다")
odd = np.array([7, 8])
print("    np.array([7, 8])     :", odd, "/ dtype", odd.dtype)
print("    np.array([7, 8]) / 2 :", odd / 2, "/ dtype", (odd / 2).dtype)

# ======================================================
# 4. astype - 자료형 바꾸기, 반올림이 아니라 버림입니다. (함정2)
# ======================================================
# 3번은 '모르고 깎인' 경우였습니다. 이번엔 일부러 바꿉니다.
# 쓰는 함수는 astype이고, 함정이 똑같은 모양으로 또 나옵니다.
print("=" * 60)
print("[4] astype - 자료형을 바꾼 새 배열을 받습니다")
raw = np.array([1.7, -1.7, 2.3, 3.9])
print("    원본          :", raw, "/ dtype", raw.dtype)
print("    astype(int)   :", raw.astype(int), "<- 1.7 이 2 가 아니라 1 입니다")
print("    np.round      :", np.round(raw), "<- 반올림은 이쪽")
print("    np.floor      :", np.floor(raw), "<- 내림은 또 다릅니다. -1.7 을 보세요")
print("    원본은 그대로 :", raw, "<- astype 은 원본을 바꾸지 않습니다")

# 비유: 온도계로 생각하면 셋이 갈립니다. 영하 1.7도를 정수로 적어야 한다면
# 버림은 0쪽으로 당겨서 -1 로 적습니다. 소수점 아래를 떼기만 하니까.
# 반올림은 가까운 쪽으로 가서 -2 로 적습니다. -1.7은 -2에 더 가깝죠.
# 내림은 늘 더 추운 쪽으로 가서 -2 로 적습니다. 항상 아래쪽이니까요.
# 깨지는 지점 - 영상 1.7도에서는 버림도 1, 내림도 1 입니다. 같아 보여요.
# 0 보다 작아질 때만 갈립니다. 그래서 양수만 보고 "같은 거네" 하면 틀립니다.
#
# 버림(astype) 소수점 아래를 그냥 떼기.
# 반올림(round) 가까운 정수로.
# 내림(floor) 작은 쪽 정수로.


# ======================================================
# 5. 배열에게 물어보는 네 가지 - shape ndim size dtype
# ======================================================
# 데이터를 받으면 가장 먼저 하는 일이 "이게 몇 줄 몇 칸인가" 입니다.
# 01 단원에서 len(rows) 와 len(header)로 센 걸 기억 하실겁니다.
# NumPy 는 그걸 배열에게 직접 물어봅니다. 네 가지
#
# shape = 배열의 모양, (행 수, 열 수 ) 꼴의 묶음으로 나옵니다.
# *** (행, 열) *** 이렇게 들어 온다 무조건
# ndim = 차원 수, 한 줄로 늘어선 배열은 1, 표 모양은 2 입니다.
# size = 값이 모두 몇 개인가. shape의 숫자들을 곱한 값입니다.
# attribute = 함수가 아니라 "이미 가지고 있는 정보"


print("=" * 60)
print("[5] 배열에게 물어보는 네 가지")
table = np.array(
    [[30, 15.44, 4603], [30, 18.69, 4603]]
)  # 데이터 파일 앞 두 줄에서 세 칸만 떼 온 것입니다
print("    table")
print(table)
print("    table.shape :", table.shape, "<- (행, 열)")
print("    table.ndim  :", table.ndim, "<- 몇 차원인가")
print("    table.size  :", table.size, "<- 값이 모두 몇 개인가")
print("    table.dtype :", table.dtype, "<- 어떤 자료형인가")
print(
    "    검산:",
    table.shape[0],
    "x",
    table.shape[1],
    "=",
    table.shape[0] * table.shape[1],
)


print()
print("[5-1] 괄호를 붙이면")
try:
    table.shape()  # 속성에 괄호를 붙이면 터집니다
except TypeError as e:
    print("    table.shape() :", type(e).__name__, "-", e)


# ======================================================
# 6. 모양 바꾸기 - reshape · flatten (값은 그대로, 모양만)
# ======================================================
# 같은 12개 숫자를 한 줄로 늘어놓을 수도 있고, 3줄 4칸 표로 접을 수도 있습니다.
# 값은 그대로고 보는 모양만 바뀝니다. 그게 reshape입니다.
print("=" * 60)
print("[6] 모양 바꾸기 - 값은 그대로, 모양만")
seq = np.arange(12)
print("    seq                  :", seq)
print("    seq.reshape(3, 4)")
print(seq.reshape(3, 4))
print(
    "    seq.reshape(-1, 2).shape :", seq.reshape(-1, 2).shape, "<- -1 은 '알아서 계산'"
)
print("    reshape(3, 4).flatten()  :", seq.reshape(3, 4).flatten())
print("    원본 seq             :", seq, "<- reshape 도 원본을 바꾸지 않습니다")

print()
print("[6-1] 개수가 안 맞으면")
try:
    seq.reshape(5, 3)  # 12개를 15칸에 넣으라는 말이 됩니다
except ValueError as e:
    print("    seq.reshape(5, 3) :", type(e).__name__, "-", e)
print("    12 는 3x4, 2x6, 1x12 로는 접히고 5x3 = 15 로는 안 접힙니다")

# ======================================================
# 7. CSV 파일을 배열로 읽기 - 그리고 e+07 이 뭔가?
# ======================================================
# delimiter 딜리미터    -> 칸을 나누는 글자. CSV는 쉼표
# skiprows -> 맨 위 몇 줄을 건너뛸까. 1 = 열 이름 줄을 건너뜀
# encoding = 글자를 어떤 규칙으로 읽을까?


print("=" * 60)
print("[7] CSV 파일을 배열로 읽기")
full = np.loadtxt(MCT, delimiter=",", skiprows=1, encoding="utf-8-sig")
print("    shape:", full.shape, "/ dtype:", full.dtype)
print("    앞 2줄")
print(full[:2])

# 위 결과가 눈에 안 들어옵니다. 보기 설정을 한 줄 바꿉니다.
print()
print("[7-1] 같은 배열인데 보기가 달라집니다")
np.set_printoptions(suppress=True)  # 지수 표기를 끄는 설정. 값은 안 바뀝니다
print(full[:2])

print()
print("[7-2] 열 이름은 따로 읽습니다")
with open(MCT, encoding="utf-8-sig") as f:
    head = next(csv.reader(f))  # 첫 줄만 꺼냅니다. 8단원에서 한 그 방법
print("    열 이름:", head)
print(
    "    공구번호 종류:",
    np.unique(full[:, 0]),
    "->",
    len(np.unique(full[:, 0])),
    "가지",
)

mct = np.loadtxt(
    MCT, delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5), encoding="utf-8-sig"
)
cols = head[1:]  # 열 이름도 공구번호를 뺀 5개로 맞춥니다
print("    공구번호를 뺀 배열:", mct.shape, "/ 열 이름", cols)
print("    앞 3줄")
print(mct[:3])

# 빈 칸이 있는 파일은 loadtxt 로 못 읽습니다. 지금 확인해 둡니다.
print()
print("[7-3] 빈 칸이 섞여 있으면")
sample = ["1,2,3", "4,,6"]  # 파일 대신 글자 두 줄로 흉내를 냅니다
# ★ 위 sample 이 파일 이름이 아니라 글자 두 줄인 게 눈에 걸리실 겁니다.
#   loadtxt 는 파일을 받으면 한 줄씩 꺼내 읽습니다. 그래서 '한 줄씩 꺼낼 수 있는 것'
#   이면 파일이 아니어도 받아 줍니다. 리스트도 한 줄씩 꺼낼 수 있으니 되는 거예요.
#   빈 칸이 있는 CSV 를 따로 만들지 않으려고 두 줄로 대신한 겁니다.
#   "4,,6" 의 쉼표 두 개가 붙어 있는 데를 보세요. 그 사이가 빈 칸입니다.
try:
    np.loadtxt(sample, delimiter=",")
except ValueError as e:
    print("    loadtxt    :", type(e).__name__, "-", e)
print("    genfromtxt :")
print(np.genfromtxt(sample, delimiter=","))

# ======================================================
# 실습 1 - 전류 40개를 배열로 다루기
# ======================================================
# [문제]
# 0번 ~ 7번에서 배운 것만 씁니다. 통계는 아직 안 씁니다.
#
# 1 - np.arange 로 측정 순번 0~39를 만드세요. 앞 5개와 뒤 3개, shape, dtype을 찍으세요.
print("=" * 60)
sequence = np.arange(40)
print(
    "앞 5개:",
    sequence[:5],
    "뒤 3개:",
    sequence[-3:],
    "shape:",
    sequence.shape,
    "dtype:",
    sequence.dtype,
)

# 2 - 10_mct_tool.csv에서 전류 열(3번 열)만 배열로 읽어 앞 5개를 찍으세요.
current = np.loadtxt(MCT, delimiter=",", skiprows=1, usecols=3, encoding="utf-8-sig")
print("전류 앞 5개:", current[:5])

# 3 - 그 배열의 shape, ndim, size, dtype을 한 줄에 찍으세요.
print(current.shape, current.ndim, current.size, current.dtype)

# 4 - 전류 40개를 8줄 5칸으로 접고, flatten 해서 원본과 같은지 확인하세요.
current_reshape = current.reshape(8, 5)
print(current_reshape)

print(np.array_equal(current_reshape.flatten(), current))
print(8 * 5, current.size)

# 5 - 7줄 6칸으로 접어 보고 어떤 오류가 나는지 확인하세요.
try:
    current.reshape(7, 6)
except ValueError as e:
    print(type(e).__name__, e)

# ======================================================
# 8. 필요한 칸만 꺼내기 - 인덱싱 슬라이싱
# ======================================================
# (40, 5) 배열에서 전류 한 열만, 또는 첫 줄만 꺼내고 싶습니다.
# 리스트에서 쓰던 대괄호를 그대로 씁니다. 다만 쉼표로 두 방향을 같이 줄 수 있습니다.
#
# 1차원 배열 arr[번호]   한 값
#          arr[시작:끝] 구간.  끝 번호는 안 들어갑니다.
#
# 2차원 배열 arr[행,열] 한 값
#          arr[행] 그 줄 전체
#          arr[:,열]  그 열 전체  <- 앞의 콜론이 "모든 행" 입니다.
print("=" * 60)
print("[8] 필요한 칸만 꺼내기")
cur = mct[:, 2]  # 전류 열 전체. 열 번호 2 는 cols 의 세 번째
print("    mct[0, 2]     :", mct[0, 2], "<- 0번 줄 2번 열 = 첫 줄 전류")
print("    mct[0]        :", mct[0], "<- 0번 줄 전체")
print("    mct[:, 2][:5] :", cur[:5], "<- 전류 열에서 앞 5개")
print("    mct[-1]       :", mct[-1], "<- 마지막 줄")
print("    cur[1:4]      :", cur[1:4], "<- 1번부터 3번까지 (4번은 빠집니다)")
print("    cur[::10]     :", cur[::10], "<- 10칸씩 건너뛰며")
print("    mct[:, 1:3][:3]")
print(mct[:, 1:3][:3])

print()
print("[8-1] 번호를 넘기면")
try:
    mct[40, 0]  # 줄은 0~39 까지입니다
except IndexError as e:
    print("    mct[40, 0] :", type(e).__name__, "-", e)
try:
    mct[0, 5]  # 열은 0~4 까지입니다
except IndexError as e:
    print("    mct[0, 5]  :", type(e).__name__, "-", e)
print("    mct[38:50].shape :", mct[38:50].shape, "<- 슬라이싱은 넘겨도 조용합니다")

# 여기서 나머지 열도 이름을 붙여 둡니다. 뒤에서 계속 씁니다.
cyc = mct[:, 0]  # 사이클타임
tmp = mct[:, 1]  # 온도
rpm = mct[:, 3]  # 회전수
tq = mct[:, 4]  # 토크


# ======================================================
# 9. 브로드캐스팅 - 짝이 안 맞는 계산을 늘려서 맞춥니다.
# ======================================================
# 0번에서 arr + 5 가 됐습니다. 그게 왜 되는지 이제 이름을 붙입니다.
#
# 브로드캐스팅 = 모양이 다른 것끼리 계산할 때
# NumPy가 작은 쪽을 늘려서 짝을 맞춰 주는 것.
# 방송처럼 "전체에 퍼뜨린다"는 뜻입니다.
# arr + 5 는 40개로 늘려서 같은 자리끼리 더한 것과 같습니다.
# * 실제로 5를 40개 복사해 메모리에 늘어놓는 건 아닙니다. 늘린 것처럼
# 계산만 합니다. 그래서 값이 400만 개여도 메모리가 두 배로 안 늘어납니다.
print("=" * 60)
print("[9] 브로드캐스팅 - 짝이 안 맞는 계산을 늘려서 맞춥니다")
three = np.array([70, 72, 71])
print("    three             :", three)
print("    three + 5         :", three + 5, "<- 5 가 세 개로 늘어났습니다")
print("    three + [1, 2, 3] :", three + np.array([1, 2, 3]), "<- 같은 자리끼리")
try:
    three + np.array([1, 2])  # 3개와 2개는 늘릴 방법이 없습니다
except ValueError as e:
    print("    three + [1, 2]    :", type(e).__name__, "-", e)
# 브로드캐스팅으로 실제로 하는 일 두 가지를 해 봅니다. 둘 다 현장에서 매일 씁니다.
# cur.min  cur.max cur.mean() cur.std() 가 나옵니다.
# 지금은 2를 넘는 것만 골라 찍었다로 읽으면 됩니다. 몰라도 안 막힘.
print()
print("[9-1] 전류를 0~1 사이로 옮기기 (최소-최대 정규화)")
scaled = (cur - cur.min()) / (cur.max() - cur.min())
print("    전류 앞 5개  :", cur[:5])
print("    옮긴 값 앞 5개:", np.round(scaled[:5], 2))
print("    최소", scaled.min(), "/ 최대", scaled.max(), "/ 개수", scaled.size)

print()
print("[9-2] 평균 0, 표준편차 1 로 옮기기 (표준화)")
z = (cur - cur.mean()) / cur.std()
print("    앞 8개:", np.round(z[:8], 2))
print("    2 를 넘는 값:", np.round(z[z > 2], 2), "/", (z > 2).sum(), "건")
# 정규화 - 값의 범위를 0~1 로 옮기는 것. 가장 작은 값이 0, 가장 큰 값이 1
# 표준화 - 평균을 0, 표준편차를 1 옮기는 것. 결과 숫자가
# 평균에서 표준편차의 몇 배만큼 떨어졌나를 뜻 합니다.

# ======================================================
# 10. 조건으로 고르기 - 불리언 인덱싱
# ======================================================
# 01 단원에서는 이렇게 했습니다 - [t for t in temps if t> 862]
# NumPy 는 이렇게 씁니다 - cur[cur > 50]
# 같은 일인데 생김새가 아주 다릅니다. 둘로 끊어서 봅시다.
# 불리언 인덱싱 = 참/거짓 배열을 대괄호에 넣어 "참인 자리만" 꺼내는 것
# 두 단계로 들어갑니다
# 1) cur > 50 이 먼저 계산돼서 [False False False True ...]가 만들어짐
# 2) cur[그 배열] 이 True 자리의 값만 모아 새 배열을 만듭니다.
print("=" * 60)
print("[10] 조건으로 고르기")
print("    cur > 50 (앞 10개):", (cur > 50)[:10])
print("    cur[cur > 50]     :", cur[cur > 50])
print("    몇 건인가         :", (cur > 50).sum(), "건")
print("    몇 퍼센트인가     :", round((cur > 50).mean() * 100, 1), "%")
print("    몇 번째 줄인가    :", np.where(cur > 50)[0])
print("    np.where(조건,1,0):", np.where(cur > 50, 1, 0)[:10])

print()
print("[10-1] 조건 두 개를 겹칠 때")
print("    전류>50 그리고 토크>100:", ((cur > 50) & (tq > 100)).sum(), "건")
print("    전류>50 또는   토크>100:", ((cur > 50) | (tq > 100)).sum(), "건")
try:
    (cur > 50) and (tq > 100)  # and 는 배열에 못 씁니다
except ValueError as e:
    print("    and 로 쓰면:", type(e).__name__, "-", e)
# ======================================================
# 11. 조건에 맞는 '줄'을 통째로 꺼내기
# ======================================================
# 10번에서는 전류 값만 꺼냈습니다. 그런데 분석에서 정말 궁금한 건 이거예요
# "그 줄의 다른 칸은 어땠냐?"
# 전류가 튄 그 순간, 회전수는 어땠고 토크는 어땠는지.
# 참/거짓 배열을 2차원 배열의 대괄호에 그냥 넣으면 '줄' 이 뽑힙니다. 한 줄입니다.
print("=" * 60)
print("[11] 조건에 맞는 '줄' 을 통째로 꺼내기")
print("    열 이름:", cols)
print("    토크가 100 넘는 줄")
print(mct[tq > 100])

# 01단원에서 로트A/B/C 로 나눠 재던 걸 여기서도 하고 싶습니다.
# 그런데 공구번호가 한 종류뿐이라(7-2) 그걸로는 못 나눕니다. 회전수를 보니 길이 있었습니다.
print()
print("[11-1] 회전수로 두 묶음을 나눠 재 봅니다")
usual = rpm == 4603  # 가장 많이 나온 회전수. 아래 검산으로 확인합니다
print("    회전수 4603 인 줄:", usual.sum(), "줄 / 아닌 줄:", (~usual).sum(), "줄")
print(
    "    4603 묶음  : 전류 평균",
    round(cur[usual].mean(), 2),
    "/ 토크 평균",
    round(tq[usual].mean(), 2),
)
print(
    "    나머지 묶음: 전류 평균",
    round(cur[~usual].mean(), 2),
    "/ 토크 평균",
    round(tq[~usual].mean(), 2),
)
print(
    "    검산:",
    usual.sum(),
    "+",
    (~usual).sum(),
    "=",
    usual.sum() + (~usual).sum(),
    "/ 전체",
    len(mct),
)
# == <- 소수에 쓸 때 조심해야 합니다.


# ======================================================
# 12. 통계 한 번에 - 그리고 평균 10.7, 중앙값 2.0 함정 3,4
# ======================================================
# 01 단원에서는 평균을 이렇게 냈습니다 - sum(temps) / len(temps)
# 최대 최소는 max() min(), 흔들림은 for를 돌려 직접 만들었습니다.
# NumPy 는 전부 매서드 한 개씩입니다.
#   cur.sum()      합계           cur.min()  최소
#   cur.mean()     평균           cur.max()  최대
#   cur.std()      표준편차       cur.var()  분산
#   np.median(cur) 중앙값  <- 이것만 앞에 np. 가 붙습니다.
#   왜 median 만 생김새가 다른가 -> 외워야함.
# 중앙값 -> 값듫을 줄 세웠을 때 가운대 있는 값.
#          평균과 다릅니다. 아주 다릅니다.
# 표준편차(std)  = 값들이 평균에서 평균적으로 얼마나 떨어져 있나.
# 분산(var) = 표준편차에 제곱근을 씌우기 전의 값. 표준편차의 제곱.
print("=" * 60)
print("[12] 통계는 메서드 한 개씩입니다")
print("    전류 합계    :", round(cur.sum(), 2))
print("    전류 개수    :", cur.size)
print("    전류 평균    :", round(cur.mean(), 2))
print("    전류 중앙값  :", np.median(cur))
print("    전류 최소/최대:", cur.min(), "/", cur.max())
print("    전류 표준편차:", round(cur.std(), 2))

# 다섯 열을 한 번에 재 봅니다. for 는 '열을 돌기' 위한 것이고 계산은 전부 NumPy 가 합니다.
print()
print("[12-1] 다섯 열을 한 줄씩 재 봅니다")
for i in range(len(cols)):
    c = mct[:, i]
    print(
        f"    {cols[i]:<6} 평균 {c.mean():>9.2f}  중앙값 {np.median(c):>9.2f}"
        f"  표준편차 {c.std():>8.2f}  최소 {c.min():>8.2f}  최대 {c.max():>8.2f}"
    )

# 위 표에서 한 줄만 다시 봅니다. 오늘 세 번째 함정입니다.
print()
print("[12-2] 토크 한 줄만 다시 보세요")
print("    토크 평균:", round(tq.mean(), 2), "/ 중앙값:", np.median(tq))
print("    줄 세워서 작은 쪽 5개:", np.sort(tq)[:5], "/ 큰 쪽 5개:", np.sort(tq)[-5:])
print(
    "    평균보다 큰 줄:",
    (tq > tq.mean()).sum(),
    "건 / 작은 줄:",
    (tq < tq.mean()).sum(),
    "건",
)

# 네 번째 함정. 같은 데이터에서 표준편차가 두 개 나옵니다.
print()
print("[12-3] 표준편차는 두 가지가 있습니다")
print("    cur.std()       :", round(cur.std(), 4), "<- 분모가 40")
print("    cur.std(ddof=1) :", round(cur.std(ddof=1), 4), "<- 분모가 39")
print(
    "    cur.var()       :",
    round(cur.var(), 4),
    "/ var(ddof=1):",
    round(cur.var(ddof=1), 4),
)
# ddof = 분모에서 뺄 개수, 기본값은 0 입니다.
# ddof=0 이면 분모가 개수(40), ddof=1 이면 개수-1(39)
# NumPy는 0이 기본이고, Pandas의 .std()는 1이 기본입니다.

# ======================================================
# 13. axis - 어느 방향으로 재는가
# ======================================================
#
# 축(axis) = 배열에서 세는 방향
# 2차원 배열에서는 두 방향뿐입니다
# axis=0 줄 방향(위에서 아래로) -> 결과가 '열별'로 나옵니다.
# axis=1 칸 방향(왼쪽에서 오른쪽으로) -> 결과가 '행별'로 나옵니다.
# axis는 '무엇을 기준으로'가 아니라 '무엇을 따라 훑어 없앨지'입니다.
# axis=0 을 주면 줄 방향이 없어지고 열만 남습니다. 그래서 '열별 평균'이 됩니다.
# (40,6)
print("=" * 60)
print("[13] axis - 어느 방향으로 재는가")
print("    mct.shape:", mct.shape, "<- 40줄 5열")
down = mct.mean(axis=0)  # 줄 방향으로 훑어 없앰 -> 열별 평균 5개
across = mct.mean(axis=1)  # 칸 방향으로 훑어 없앰 -> 행별 평균 40개
print("    mct.mean(axis=0) -> 값", len(down), "개")
for i in range(len(cols)):
    print(f"        {cols[i]:<6} {down[i]:>10.2f}")
print(
    "    mct.mean(axis=1) -> 값", len(across), "개 / 앞 3개:", np.round(across[:3], 2)
)
print(
    "    mct.mean()       ->", round(mct.mean(), 2), "<- 축을 안 주면 200개 전부의 평균"
)

# 바꿔 써 봅니다. 여기가 오늘의 함정입니다.
print()
print("[13-1] 바꿔 쓰면 어떻게 되나")
print("    열별 평균 첫 값(사이클타임):", round(down[0], 2))
print("    행별 평균 첫 값(첫 줄)     :", round(across[0], 2))
print("    첫 줄:", mct[0])
print("    손으로 검산:", round(mct[0].sum() / 5, 2), "<- 행별 평균 첫 값과 같습니다")


# ======================================================
# 14. for 문 없이 - 01단원에서 for 로 하던 일을 다시
# ======================================================
# 오늘의 마지막 섹션입니다. 01단원에서 한 일을 두 방법으로 나란히 해 봅니다.
# 숫자가 같은지, 코드가 얼마나 줄었는지 둘 다 보세요.
print("=" * 60)
print("[14] 01단원에서 for 로 하던 일")
with open(MCT, encoding="utf-8-sig") as f:  # 01단원 방식: csv 모듈로 읽기
    r = csv.reader(f)
    next(r)  # 열 이름 줄을 버립니다
    rows = list(r)

vals = []  # 1) 빈 리스트를 만들고
for row in rows:  # 2) for 로 돌면서
    vals.append(float(row[3]))  # 3) 전류 칸을 숫자로 바꿔 담습니다
avg = sum(vals) / len(vals)  # 4) 평균
gaps = []  # 5) 또 빈 리스트
for v in vals:  # 6) 또 for
    gaps.append(abs(v - avg))  # 7) 평균에서 떨어진 거리

print(
    "    순수 파이썬: 개수",
    len(vals),
    "/ 평균",
    round(avg, 2),
    "/ 최대",
    max(vals),
    "/ 최소",
    min(vals),
    "/ 흔들림",
    round(sum(gaps) / len(gaps), 2),
)

print()
print("[14-1] 같은 일을 NumPy 로")
print(
    "    NumPy      : 개수",
    cur.size,
    "/ 평균",
    round(cur.mean(), 2),
    "/ 최대",
    cur.max(),
    "/ 최소",
    cur.min(),
    "/ 흔들림",
    round(np.abs(cur - cur.mean()).mean(), 2),
)

print()
print("[14-2] 두 평균을 끝자리까지 비교하면")
print("    순수 파이썬:", avg)
print("    NumPy      :", cur.mean())

# ======================================================
# 실습 2 - 토크가 튀는 줄의 정체
# ======================================================
# [문제]
# 11번에서 "회전수가 떨어지고 전류가 올라간 순간에 토크가 튀었다"를 두 줄로 봤습니다.
# 이번엔 두 줄이 아니라 40줄 전체로 확인하세요. 그리고 축을 한 번 확인합니다.
#
# 1. 토크가 100 넘는 줄을 통째로 꺼내고 몇 건인지 세세요.
print("=" * 60)
a = mct[tq > 100]
print(len(a), "건")

# 2. 그 줄들의 회전수와 전류를 전체 평균과 나란히 찍으세요.
print(rpm[tq > 100], round(rpm.mean(), 2))
print(cur[tq > 100], round(cur.mean(), 2))

# 3. 회전수 4000 미만인 줄과 4000 이상인 줄의 토크 평균을 각각 내세요.
usual = rpm >= 4000
print("4000이상", round(tq[usual].mean(), 2))
print("4000미만", round(tq[~usual].mean(), 2))

# 4. 열별 평균과 행별 평균의 '개수'를 찍어 어느 쪽이 열별인지 확인하세요.
down = mct.mean(axis=0)
across = mct.mean(axis=1)
print("열별평균의 개수:", len(down), "행별평균의 개수:", len(across))

# 5. 검산 두 줄 - 줄 수의 합, 그리고 토크 합계의 합.
print("토크 합계", tq.sum())

# ======================================================
# 마무리 - 오늘 세운 것
# ======================================================
# 오늘 외울 문장 하나 - "묶음에 한 번 쓰면 전부에 적용된다."
#   arr * 2 · arr + 5 · cur > 50 · cur.mean() 이 전부 이 문장입니다.
#
# 오늘 배운 것을 한 줄씩
#   만들기   np.array · arange(간격) · linspace(개수) · zeros · ones · full
#   물어보기 shape(행, 열) · ndim · size · dtype      <- 괄호 없음
#   바꾸기   reshape(모양) · flatten() · astype(자료형) <- 결과를 받아 적어야 함
#   읽기     np.loadtxt(파일, delimiter, skiprows, usecols, encoding)
#   꺼내기   arr[행, 열] · arr[:, 열] · arr[시작:끝] · arr[조건]
#   재기     sum · mean · std · min · max · var · np.median(앞에 np.)
#   방향     axis=0 열별 · axis=1 행별
#
# 오늘 밟은 함정 다섯 - 전부 "오류가 안 나는" 것들입니다
#   ① 정수 배열에 2.7 을 넣으면 2 가 된다                     (3번)
#   ② astype(int) 는 버림이다. 반올림이 아니다                 (4번)
#   ③ 토크 평균 10.7, 중앙값 2.0 - 평균이 가운데가 아니다       (12-2)
#   ④ 표준편차가 분모에 따라 12.89 와 13.06 둘이다             (12-3)
#   ⑤ axis=0 과 axis=1 을 바꿔 쓰면 멀쩡한 숫자가 틀리게 나온다 (13번) ★
#   ★ 공통점을 보세요 - 다섯 개 모두 프로그램이 멀쩡히 돌았습니다.
#     코드가 짧아지면 틀렸을 때 알아채기도 어려워집니다. 그래서 검산이 더 중요해집니다.
#
# 01단원에서 세운 습관 셋이 오늘 어떻게 쓰였나
#   습관 1  파일을 받으면 크기부터 센다      -> shape 를 찍는 것 (5·7번)
#   습관 2  평균 하나로 끝내지 않는다        -> 중앙값도 같이 재는 것 (12번)
#   습관 3  센 숫자의 합이 전체와 맞나 본다  -> 11-1 과 실습 ②의 검산 (도구가 바뀌어도 습관은 그대로)
