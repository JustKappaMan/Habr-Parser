from .main import HabrParser
from .utils import parse_cli_args


if __name__ == "__main__":
    habr_parser = HabrParser(**parse_cli_args())
    habr_parser.run()
