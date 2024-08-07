import sys
import csv
import json
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup

from habrparser.utils import parse_cli_args


class HabrParser:
    """
    A class to parse top articles info from Habr.
    """

    __slots__ = ("url", "fmt", "page_source", "parsing_results")

    def __init__(self, language: str = "ru", fmt: str = "json", period: str = "daily"):
        """
        Initialize the HabrParser instance with given params.
        """
        self.url = f"https://habr.com/{language}/top/{period}/"
        self.fmt = fmt
        self.page_source = None
        self.parsing_results = None

    def run(self, print_results: bool = False) -> list:
        """
        Run the entire process of fetching, parsing, and printing the info.
        """
        self._fetch_page_source()
        self._parse_page_source()

        if print_results:
            self._print_parsing_results()

        return self.parsing_results

    def _fetch_page_source(self) -> None:
        """
        Fetch the page source of the `self.url`.
        """
        try:
            self.page_source = urlopen(self.url).read().decode("utf-8")
        except HTTPError as e:
            sys.exit(f"HTTPError: {e.code} ({e.reason})")
        except URLError as e:
            sys.exit(f"URLError: {e.reason}")
        except (Exception,) as e:
            sys.exit(f"Exception: {e}")

    def _parse_page_source(self) -> None:
        """
        Parse the fetched page source to extract the top articles info and store it as a dict.
        """
        soup = BeautifulSoup(self.page_source, "lxml")

        titles = [el.find("span").string for el in soup.find_all("a", class_="tm-title__link")]
        authors = [el.contents[0].strip() for el in soup.find_all("a", class_="tm-user-info__username")]
        pub_dates = [el.get("title") for el in soup.find_all("time")]

        if not (len(titles) == len(authors) == len(pub_dates)):
            sys.exit("Something went wrong! Some data is missing.")

        self.parsing_results = [
            {"title": title, "author": author, "pub_date": pub_date}
            for title, author, pub_date in zip(titles, authors, pub_dates)
        ]

    def _print_parsing_results(self) -> None:
        """
        Print the parsing results in the specified format.
        """
        if self.fmt == "json":
            print(json.dumps(self.parsing_results, indent=4, ensure_ascii=False))
        elif self.fmt == "csv":
            writer = csv.DictWriter(sys.stdout, fieldnames=("title", "author", "pub_date"))
            writer.writeheader()
            writer.writerows(self.parsing_results)


if __name__ == "__main__":
    habr_parser = HabrParser(**parse_cli_args())
    habr_parser.run(print_results=True)
