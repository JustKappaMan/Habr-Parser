from habrparser.main import HabrParser
from habrparser.utils import parse_cli_args


if __name__ == "__main__":
    habr_parser = HabrParser(**parse_cli_args())
    habr_parser.run()
