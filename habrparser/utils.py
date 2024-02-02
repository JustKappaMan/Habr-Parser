import argparse


def parse_cli_args() -> dict:
    """
    Parse command line arguments that will be passed to HabrParser.
    """
    parser = argparse.ArgumentParser(
        description="Collect info about the top articles on Habr for a given period of time",
        allow_abbrev=False,
    )

    parser.add_argument("-l", "--language", help="articles language", choices=("ru", "en"), default="ru")
    parser.add_argument("-f", "--format", help="output format", choices=("json", "csv"), default="json")
    parser.add_argument(
        "-p",
        "--period",
        help="publication date range",
        choices=("daily", "weekly", "monthly", "yearly", "alltime"),
        default="daily",
    )

    return vars(parser.parse_args())
