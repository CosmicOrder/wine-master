import datetime
from pprint import pprint

import pandas
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(loader=FileSystemLoader(''),
                  autoescape=select_autoescape(['html', 'xml']))

template = env.get_template('template.html')

total_age = datetime.datetime.today().year - 1909
if str(total_age)[-1] == '1':
    years = 'год'
elif str(total_age)[-1] in ['2', '3', '4']:
    years = 'года'
else:
    years = 'лет'

wine_df = pd.read_excel('wine.xlsx')
wine_dict = wine_df.to_dict(orient='records')

wine_df2 = pd.read_excel('wine2.xlsx', keep_default_na=False)
wine_dict2 = wine_df2.to_dict(orient='records')

new_dict = {}
for i in wine_dict2:
    new_dict.setdefault(i['Категория'], []).append(i)

pprint(new_dict)

rendered_page = template.render(age=total_age, years=years,
                                wine_data=wine_dict)

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
