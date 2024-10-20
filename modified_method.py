def isEven(num: int) -> bool:
    """
    If the number is even then it will return true otherwise false

    Arguments:
    num (int): The integer to be checked

    Returns:
    bool: The boolean value of the result
    """
    if num % 2 == 0:
        return True
    return False


def sum(lst: list) -> int:
    """
    Function to sum up all the numbers in the given list.

    Arguments:
    lst (list): List of numbers.

    Returns:
    int: Sum of all the numbers in the list.
    """
    total = 0
    if not isinstance(lst, list):
        return "enter valid list"
    for num in lst:
        total += num
    return total


def get_fibonacci_list(n) -> list:
    """
    This function generates the first 'n' numbers in the Fibonacci sequence.

    Arguments:
    n (int): The number of Fibonacci numbers to be generated and returned.

    Returns:
    list: A list containing the first 'n' Fibonacci numbers.
    """
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
