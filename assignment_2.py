from typing import Generator, Callable
from decimal import Decimal
import re


def generator_numbers(text: str) -> Generator[Decimal, None, None]:
    """
    Generator: extracts all decimals from text as sequence

    Parameters:
        text (str): Text to extract numbers

    Returns:
        Generator[Decimal, None, None]: Sequence of numbers in text
    """
    for match in re.finditer(r"\b(\d+(\.\d+)?)\b", text):
        number = match.group(1)
        yield Decimal(number)


def sum_profit(text: str, func: Callable[[str], Generator[Decimal, None, None]]) -> Decimal:
    """
    Calculates sum of decimals in text
    
    Parameters:
        text (str): Text to extract numbers
        func (Callable[[str], Generator[Decimal]]): Function applied to text to extract decimals

    Returns:
        Decimal: Sum of numbers in text
    """
    total = Decimal()
    for number in func(text):
        total += number

    return total


def main() -> None:
    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими надходженнями "
        "27.45 і 324.00 доларів."
    )
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")


if __name__ == "__main__":
    main()
