import sys
import csv
import json
import argparse
import urllib.error
import urllib.request

import bs4


class HabrParser:
    __slots__ = ("cli_parser", "cli_args", "url", "page_source", "parsing_results")

    def __init__(self):
        self.cli_parser = argparse.ArgumentParser(
            description="Собирает информацию о топовых статьях на Хабре за последний год",
            allow_abbrev=False,
        )

        self.cli_parser.add_argument("-l", "--language", help="язык статей", choices=["ru", "en"], default="ru")
        self.cli_parser.add_argument("-f", "--format", help="формат вывода", choices=["json", "csv"], default="json")
        self.cli_parser.add_argument(
            "-p",
            "--period",
            help="временной диапазон статей",
            choices=["daily", "weekly", "monthly", "yearly", "alltime"],
            default="daily",
        )

        self.url = None
        self.cli_args = None
        self.page_source = None
        self.parsing_results = None

    def run(self) -> None:
        self.cli_args = vars(self.cli_parser.parse_args())
        self.url = f"https://habr.com/{self.cli_args['language']}/top/{self.cli_args['period']}/"

        self._fetch_page_source()
        self._parse_page_source()
        self._print_parsing_results()

    def _fetch_page_source(self) -> None:
        try:
            self.page_source = urllib.request.urlopen(self.url).read().decode("utf-8")
        except urllib.error.HTTPError as e:
            sys.exit(f"HTTPError: {e.code} ({e.reason})")
        except urllib.error.URLError as e:
            sys.exit(f"URLError: {e.reason}")
        except (Exception,) as e:
            sys.exit(f"Exception: {e}")

    def _parse_page_source(self) -> None:
        soup = bs4.BeautifulSoup(self.page_source, "html.parser")

        titles = [el.find("span").string for el in soup.find_all("a", class_="tm-title__link")]
        authors = [el.contents[0].strip() for el in soup.find_all("a", class_="tm-user-info__username")]
        pub_dates = [el.get("title") for el in soup.find_all("time")]

        if not (len(titles) == len(authors) == len(pub_dates)):
            sys.exit("Что-то пошло не так! Некоторые заголовки/авторы/даты отсутствуют.")

        self.parsing_results = [
            {"title": title, "author": author, "pub_date": pub_date}
            for title, author, pub_date in zip(titles, authors, pub_dates)
        ]

    def _print_parsing_results(self) -> None:
        if self.cli_args["format"] == "json":
            print(json.dumps(self.parsing_results, indent=4, ensure_ascii=False))
        elif self.cli_args["format"] == "csv":
            writer = csv.DictWriter(sys.stdout, fieldnames=["title", "author", "pub_date"])
            writer.writeheader()
            writer.writerows(self.parsing_results)
        else:
            sys.exit("Что-то пошло не так! Вы умудрились обойти валидацию ввода.")


if __name__ == "__main__":
    habr_parser = HabrParser()
    habr_parser.run()
