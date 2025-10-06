from typing import Callable


def caching_fibonacci() -> Callable[[int], int]:
    """
    Returns Fibonacci function with cache support:
    recursive implementation, but previous results are reused
    """
    numbers = dict()

    def fibonacci(n: int) -> int:
        """
        Returns Nth Fibonacci number
        """
        nonlocal numbers
        
        if n <= 0:
            return 0

        if n == 1:
            return 1
            
        if n in numbers:
            return numbers[n]

        numbers[n] = fibonacci(n - 2) + fibonacci(n - 1)
        return numbers[n]

    return fibonacci


def main():
    fibb = caching_fibonacci()
    print([fibb(i) for i in range(0, 7)])
    print([fibb(i) for i in range(1, 10)])


if __name__ == "__main__":
    main()
