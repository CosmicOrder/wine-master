import datetime
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

FOUNDATION_DATE = 1920


def main():
    env = Environment(loader=FileSystemLoader(''),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')

    wine_path = os.getenv('WINE_PATH', default='wine.xlsx')

    wines_from_excel_df = pd.read_excel(wine_path, keep_default_na=False)
    wines_from_excel = wines_from_excel_df.to_dict(orient='records')

    wines = {}
    for wine_from_excel in wines_from_excel:
        wines.setdefault(wine_from_excel['Категория'], []) \
            .append(wine_from_excel)

    company_age = datetime.datetime.today().year - FOUNDATION_DATE
    if str(company_age)[-1] == '1' \
            and str(company_age)[-2:] not in ['11', '12', '13', '14']:
        age = 'год'
    elif str(company_age)[-1] in ['2', '3', '4'] \
            and str(company_age)[-2:] not in ['11', '12', '13', '14']:
        age = 'года'
    else:
        age = 'лет'

    rendered_page = template.render(company_age=company_age, age=age,
                                    wines=wines)

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
