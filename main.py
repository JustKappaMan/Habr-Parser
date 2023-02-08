import sys
import csv
import json
import urllib.error
import urllib.request
import argparse

import bs4


def main():
    cli_parser = argparse.ArgumentParser(
        description='Parses info about top articles of the last year from Habr.com',
        epilog='You can redirect CL output to a file using the redirection operator',
        allow_abbrev=False,
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40)
    )

    cli_parser.add_argument(
        '-l',
        '--language',
        help='set language of articles',
        choices=['en', 'ru'],
        default='en'
    )

    cli_parser.add_argument(
        '-f',
        '--format',
        help='set output format',
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

        titles = soup.find_all(class_='tm-article-snippet__title-link')
        authors = soup.find_all(class_='tm-user-info__username')
        dates = soup.find_all('time')

        rows = [{
            'title': row[0].string,
            'author': row[1].contents[0].strip(),
            'date': row[2].get('title')}
            for row in zip(titles, authors, dates)
        ]

        if len(titles) == len(authors) == len(dates):
            if cli_args['format'] == 'json':
                print(json.dumps(rows, indent=4))
            elif cli_args['format'] == 'csv':
                writer = csv.DictWriter(sys.stdout, fieldnames=['title', 'author', 'date'])
                writer.writeheader()
                writer.writerows(rows)
            else:
                sys.exit('Something went wrong! You bypassed CL arguments validation somehow!')
        else:
            sys.exit('Something went wrong! Some titles/authors/dates are missing!')


if __name__ == '__main__':
    main()
