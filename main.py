import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(loader=FileSystemLoader(''),
                  autoescape=select_autoescape(['html', 'xml']))

template = env.get_template('template.html')

total_age = datetime.datetime.today().year - 1920
if str(total_age)[-1] == '1' \
        and str(total_age)[-2:] not in ['11', '12', '13', '14']:
    years = 'год'
elif str(total_age)[-1] in ['2', '3', '4'] \
        and str(total_age)[-2:] not in ['11', '12', '13', '14']:
    years = 'года'
else:
    years = 'лет'

wine_df = pd.read_excel('wine3.xlsx', keep_default_na=False)
wine_dict = wine_df.to_dict(orient='records')

new_dict = {}
for i in wine_dict:
    new_dict.setdefault(i['Категория'], []).append(i)

rendered_page = template.render(age=total_age, years=years,
                                wine_data=new_dict)

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
