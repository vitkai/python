def kaprekar_step(number):
    digits = str(number)

    smaller = int("".join(sorted(digits)))
    bigger = int("".join(sorted(digits, reverse=True)))

    return bigger - smaller


def main(number):
    # Validate input
    if number < 10:
        raise ValueError("Number must contain at least 2 digits.")

    digits = str(number)

    if len(set(digits)) == 1:
        raise ValueError("Digits must not be identical.")

    previous = number

    while True:
        result = kaprekar_step(previous)

        print(f"{previous} => ", end="")
        
        digits = str(previous)
        smaller = int("".join(sorted(digits)))
        bigger = int("".join(sorted(digits, reverse=True)))

        print(f"{bigger}-{smaller}={result}")

        # Stop if result has fewer than 2 digits
        if result < 10:
            break

        # Stop if result is equal to the previous number
        if result == previous:
            break

        previous = result


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <number>")
        sys.exit(1)

    try:
        number = int(sys.argv[1])
        main(number)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)