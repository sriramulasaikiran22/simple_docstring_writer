def isEven(num: int) -> bool:
    if num%2==0:
        return True
    return False


def sum(lst: list) -> int:
    total=0
    if not isinstance(lst, list):
        return "enter valid list"
    for num in lst:
        total+=num
    return total

def get_fibonacci_list(n) -> list:
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fib_series = [0, 1]
    for i in range(2, n):
        next_fib = fib_series[-1] + fib_series[-2]
        fib_series.append(next_fib)

    return fib_series



