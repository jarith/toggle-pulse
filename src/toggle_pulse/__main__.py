from os import getenv


def main() -> None:
    print(getenv("SOME_VARIABLE"))  # noqa: T201


if __name__ == "__main__":
    main()
