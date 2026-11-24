# Report 2 : 집합 A = {1,2,3,4,5} 에 관한 관계의 동치 관계 판별 및 폐포 구현
#
# [기본 기능]
#   1. 관계 행렬 입력 기능   : input_matrix()
#   2. 동치 관계 판별 기능   : is_reflexive(), is_symmetric(), is_transitive(), check_equivalence()
#   3. 동치류 출력 기능      : equivalence_class(), print_equivalence_classes()
#   4. 폐포 구현 기능        : reflexive_closure(), symmetric_closure(), transitive_closure(), apply_closures()
#
# [추가 기능]
#   A. 입력 방식 메뉴(직접 입력 / 무작위 생성 / 예제 선택)와 반복 실행
#   B. 성질을 만족하지 않는 이유(반례 순서쌍) 출력
#   C. 관계를 순서쌍 집합으로 출력하고, 폐포로 추가된 순서쌍 표시
#   D. 서로 다른 동치류로 이루어진 분할(A/R) 출력

import random

A = [1, 2, 3, 4, 5]
N = len(A)

EXAMPLES = {
    "1": ("동치 관계인 예", [[1, 1, 0, 0, 0],
                           [1, 1, 0, 0, 0],
                           [0, 0, 1, 1, 0],
                           [0, 0, 1, 1, 0],
                           [0, 0, 0, 0, 1]]),
    "2": ("반사·대칭·추이 모두 아닌 예", [[0, 1, 0, 0, 0],
                                   [0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 1, 0],
                                   [0, 0, 0, 0, 0]]),
    "3": ("반사·대칭이지만 추이가 아닌 예", [[1, 1, 0, 0, 0],
                                     [1, 1, 1, 0, 0],
                                     [0, 1, 1, 0, 0],
                                     [0, 0, 0, 1, 1],
                                     [0, 0, 0, 1, 1]]),
}


# ---------------------------------------------------------------
# 1. 관계 행렬 입력 기능
# ---------------------------------------------------------------
def input_matrix():
    """사용자로부터 5 x 5 관계행렬을 행 단위로 입력받아 2차원 리스트로 반환"""
    print(f"{N} x {N} 관계행렬을 행 단위로 입력하세요. (예: 1 0 0 1 0)")
    matrix = []
    i = 0
    while i < N:
        line = input(f"{i + 1}행: ").split()
        if len(line) != N or any(x not in ("0", "1") for x in line):
            print(f"  → 0 또는 1을 {N}개 입력하세요.")
            continue
        matrix.append([int(x) for x in line])
        i += 1
    return matrix


def print_matrix(matrix, title=""):
    """관계행렬 출력"""
    if title:
        print(title)
    print("     " + " ".join(str(a) for a in A))
    for i in range(N):
        print(f"  {A[i]} [" + " ".join(str(x) for x in matrix[i]) + "]")


# [추가 기능 A] 무작위 관계행렬 생성
def random_matrix(p=0.3):
    return [[1 if random.random() < p else 0 for _ in range(N)]
            for _ in range(N)]


# [추가 기능 A] 예제 관계 선택
def choose_example():
    for k, (desc, _) in EXAMPLES.items():
        print(f"  {k}) {desc}")
    while True:
        k = input("예제 번호: ").strip()
        if k in EXAMPLES:
            return [row[:] for row in EXAMPLES[k][1]]
        print("  → 올바른 예제 번호를 입력하세요.")


# [추가 기능 A] 입력 방식 선택 메뉴
def choose_matrix():
    print("\n입력 방식을 선택하세요.")
    print("  1) 직접 입력   2) 무작위 생성   3) 예제 선택   0) 종료")
    while True:
        sel = input("선택: ").strip()
        if sel == "1": return input_matrix()
        if sel == "2": return random_matrix()
        if sel == "3": return choose_example()
        if sel == "0": return None
        print("  → 0~3 중에서 선택하세요.")


# [추가 기능 C] 관계를 순서쌍 집합으로 변환
def to_pairs(m):
    return [(A[i], A[j]) for i in range(N) for j in range(N)
            if m[i][j]]


def fmt_pairs(pairs):
    if not pairs:
        return "∅"
    return "{" + ", ".join(f"({a},{b})" for a, b in pairs) + "}"


# ---------------------------------------------------------------
# 2. 동치 관계 판별 기능
# ---------------------------------------------------------------
def is_reflexive(m):
    """반사 관계: 모든 a에 대해 (a, a) ∈ R"""
    return all(m[i][i] == 1 for i in range(N))


def is_symmetric(m):
    """대칭 관계: (a, b) ∈ R 이면 (b, a) ∈ R"""
    return all(m[i][j] == m[j][i]
               for i in range(N) for j in range(N))


def is_transitive(m):
    """추이 관계: (a, b) ∈ R 이고 (b, c) ∈ R 이면 (a, c) ∈ R"""
    for i in range(N):
        for j in range(N):
            if m[i][j]:
                for k in range(N):
                    if m[j][k] and not m[i][k]:
                        return False
    return True


# [추가 기능 B] 각 성질을 만족하지 않는 반례 찾기
def pair(i, j):
    return f"({A[i]},{A[j]})"


def reflexive_counterexamples(m):
    return [f"{pair(i, i)} ∉ R" for i in range(N) if not m[i][i]]


def symmetric_counterexamples(m):
    return [f"{pair(i, j)} ∈ R 이지만 {pair(j, i)} ∉ R"
            for i in range(N) for j in range(N)
            if m[i][j] and not m[j][i]]


def transitive_counterexamples(m):
    return [f"{pair(i, j)},{pair(j, k)} ∈ R 이지만 {pair(i, k)} ∉ R"
            for i in range(N) for j in range(N) for k in range(N)
            if m[i][j] and m[j][k] and not m[i][k]]


def print_counterexamples(m, r, s, t):
    checks = [("반사", r, reflexive_counterexamples),
              ("대칭", s, symmetric_counterexamples),
              ("추이", t, transitive_counterexamples)]
    for name, ok, finder in checks:
        if not ok:
            ce = finder(m)
            more = f" 외 {len(ce) - 3}개" if len(ce) > 3 else ""
            print(f"    · {name} 반례: " + "; ".join(ce[:3]) + more)


def check_equivalence(m):
    """반사·대칭·추이 결과를 출력하고 동치 관계 여부를 반환"""
    r, s, t = is_reflexive(m), is_symmetric(m), is_transitive(m)
    yn = lambda b: "O" if b else "X"
    print(f"  반사 관계: {yn(r)}   대칭 관계: {yn(s)}   추이 관계: {yn(t)}")
    print_counterexamples(m, r, s, t)          # [추가 기능 B]
    if r and s and t:
        print("  → 이 관계는 동치 관계입니다.")
        return True
    names = ("반사", "대칭", "추이")
    lacking = [n for n, ok in zip(names, (r, s, t)) if not ok]
    print(f"  → 동치 관계가 아닙니다. ({', '.join(lacking)} 관계 불만족)")
    return False


# ---------------------------------------------------------------
# 3. 동치류 출력 기능
# ---------------------------------------------------------------
def equivalence_class(m, i):
    """원소 A[i]의 동치류 [A[i]] = { x | (A[i], x) ∈ R }"""
    return [A[j] for j in range(N) if m[i][j] == 1]


# [추가 기능 D] 서로 다른 동치류만 모은 분할 A/R
def partition(m):
    parts = []
    for i in range(N):
        cls = equivalence_class(m, i)
        if cls not in parts:
            parts.append(cls)
    return parts


def print_equivalence_classes(m):
    print("  [동치류]")
    for i in range(N):
        cls = equivalence_class(m, i)
        print(f"    [{A[i]}] = {{{', '.join(map(str, cls))}}}")
    parts = partition(m)                       # [추가 기능 D]
    text = ", ".join("{" + ", ".join(map(str, c)) + "}" for c in parts)
    print(f"  [분할] A/R = {{ {text} }}  (동치류 {len(parts)}개)")


# ---------------------------------------------------------------
# 4. 폐포 구현 기능
# ---------------------------------------------------------------
def reflexive_closure(m):
    """반사 폐포: R ∪ {(a, a) | a ∈ A}"""
    c = [row[:] for row in m]
    for i in range(N):
        c[i][i] = 1
    return c


def symmetric_closure(m):
    """대칭 폐포: R ∪ R^-1"""
    return [[m[i][j] | m[j][i] for j in range(N)]
            for i in range(N)]


def transitive_closure(m):
    """추이 폐포: Warshall 알고리즘"""
    c = [row[:] for row in m]
    for k in range(N):
        for i in range(N):
            for j in range(N):
                c[i][j] |= c[i][k] & c[k][j]
    return c


def apply_closures(m):
    """반사 → 대칭 → 추이 순서로, 만족하지 않는 성질에 대해 폐포를 적용"""
    steps = [("반사", is_reflexive, reflexive_closure),
             ("대칭", is_symmetric, symmetric_closure),
             ("추이", is_transitive, transitive_closure)]
    current = m
    for name, check, closure in steps:
        if check(current):
            print(f"\n[{name} 폐포] 이미 {name} 관계이므로 변환하지 않습니다.")
            continue
        new = closure(current)
        print(f"\n[{name} 폐포]")
        print_matrix(current, "  ◇ 변환 전")
        print_matrix(new, "  ◆ 변환 후")
        added = [(A[i], A[j]) for i in range(N) for j in range(N)
                 if new[i][j] and not current[i][j]]    # [추가 기능 C]
        print(f"  + 추가된 순서쌍({len(added)}개): {fmt_pairs(added)}")
        current = new
    return current


# ---------------------------------------------------------------
# main
# ---------------------------------------------------------------
def run(R):
    print()
    print_matrix(R, "[입력된 관계행렬]")
    print(f"  R = {fmt_pairs(to_pairs(R))}")

    print("\n[동치 관계 판별]")
    if check_equivalence(R):
        print_equivalence_classes(R)
        return

    print("\n========== 폐포 변환 ==========")
    closed = apply_closures(R)

    print("\n[폐포 변환 후 동치 관계 재판별]")
    print_matrix(closed)
    print(f"  R' = {fmt_pairs(to_pairs(closed))}")
    if check_equivalence(closed):
        print_equivalence_classes(closed)


def main():
    print("=" * 50)
    print(" 동치 관계 판별 및 폐포 프로그램  (A = {1,2,3,4,5})")
    print("=" * 50)
    while True:
        R = choose_matrix()
        if R is None:
            print("프로그램을 종료합니다.")
            break
        run(R)
        print("\n" + "-" * 50)


if __name__ == "__main__":
    main()
