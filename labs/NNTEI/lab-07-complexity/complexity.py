"""Lab 07 — P vs exponential: subset-sum brute force vs DP. Run: python3 complexity.py"""
import time


def brute_subset_sum(nums, target):
    """O(2^n): any subset summing to target?"""
    n = len(nums)
    for mask in range(1 << n):
        if sum(nums[i] for i in range(n) if mask >> i & 1) == target:
            return True
    return False


def dp_subset_sum(nums, target):
    """O(n*S) pseudopolynomial DP over reachable sums."""
    reach = {0}
    for x in nums:
        reach |= {s + x for s in reach if s + x <= target}
    return target in reach


def best_of(fn, *a, k=3):
    best = float("inf")
    for _ in range(k):
        t = time.perf_counter()
        out = fn(*a)
        best = min(best, time.perf_counter() - t)
    return out, best


def _check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    cases = [([3, 1, 4, 2, 2], 6, True), ([5, 7, 11], 4, False),
             ([2, 4, 8], 14, True), ([], 0, True), ([1, 2, 3], 7, False)]
    for nums, t, want in cases:
        _check(brute_subset_sum(nums, t) == want, f"brute {nums} {t}")
        _check(dp_subset_sum(nums, t) == want, f"dp {nums} {t}")
    print(f"{'n':>3} {'brute ms':>10} {'dp ms':>10}  verdict")
    import random
    rng = random.Random(42)
    prev = None
    for n in (10, 14, 18, 21):
        nums = [rng.randint(1, 50) for _ in range(n)]
        target = sum(nums) // 3
        r1, t1 = best_of(brute_subset_sum, nums, target)
        r2, t2 = best_of(dp_subset_sum, nums, target)
        _check(r1 == r2, f"solvers disagree at n={n}")
        flag = ""
        if prev and t1 > prev * 1.4 and n > 10:
            flag = " (~doubling: exponential)"
        print(f"{n:>3} {t1*1e3:>10.2f} {t2*1e3:>10.2f}  agree={r1}{flag}")
        prev = t1
    print("ALL SELF-CHECKS PASSED")


if __name__ == "__main__":
    main()
