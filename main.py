import sys
import csv
import json
import urllib.error
import urllib.request
import argparse

import bs4


def main():
    cli_parser = argparse.ArgumentParser(
        description='Собирает информацию о топовых статьях на Хабре за последний год',
        allow_abbrev=False,
        formatter_class=lambda x: argparse.HelpFormatter(x, max_help_position=40)
    )

    cli_parser.add_argument(
        '-l',
        '--language',
        help='задаёт язык статей',
        choices=['ru', 'en'],
        default='ru'
    )

    cli_parser.add_argument(
        '-f',
        '--format',
        help='задаёт формат вывода',
        choices=['json', 'csv'],
        default='json'
    )

    cli_args = vars(cli_parser.parse_args())

    url = f'https://habr.com/{cli_args["language"]}/top/yearly/'

    try:
        page_source = urllib.request.urlopen(url).read().decode('utf-8')
    except urllib.error.HTTPError as e:
        sys.exit(f'HTTPError: {e.code} ({e.reason})')
    except urllib.error.URLError as e:
        sys.exit(f'URLError: {e.reason}')
    else:
        soup = bs4.BeautifulSoup(page_source, 'html.parser')

        titles = [el.find('span').string for el in soup.find_all('a', class_='tm-title__link')]
        authors = [el.contents[0].strip() for el in soup.find_all('a', class_='tm-user-info__username')]
        dates = [el.get('title') for el in soup.find_all('time')]

        rows = [{
            'title': title,
            'author': author,
            'date': date}
            for title, author, date in zip(titles, authors, dates)
        ]

        if len(titles) == len(authors) == len(dates):
            if cli_args['format'] == 'json':
                print(json.dumps(rows, indent=4, ensure_ascii=False))
            elif cli_args['format'] == 'csv':
                writer = csv.DictWriter(sys.stdout, fieldnames=['title', 'author', 'date'])
                writer.writeheader()
                writer.writerows(rows)
            else:
                sys.exit('Что-то пошло не так! Вы умудрились обойти валидацию ввода.')
        else:
            sys.exit('Что-то пошло не так! Некоторые заголовки/авторы/даты отсутствуют.')


if __name__ == '__main__':
    main()
