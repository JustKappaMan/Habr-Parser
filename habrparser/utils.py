import argparse


def parse_cli_args() -> dict:
    """
    Parse command line arguments that will be passed to HabrParser
    """
    parser = argparse.ArgumentParser(
        description="Собирает информацию о топовых статьях на Хабре за последний год",
        allow_abbrev=False,
    )

    parser.add_argument("-l", "--language", help="язык статей", choices=["ru", "en"], default="ru")
    parser.add_argument("-f", "--format", help="формат вывода", choices=["json", "csv"], default="json")
    parser.add_argument(
        "-p",
        "--period",
        help="временной диапазон статей",
        choices=["daily", "weekly", "monthly", "yearly", "alltime"],
        default="daily",
    )

    return vars(parser.parse_args())
