import os
import click
from datetime import datetime
from idwall_formatter import format_text
myfile = open(os.path.join(
    os.path.dirname('strings'),
    'idwall_formatter.py'))


@click.command()
@click.option('--text', required=True, help='A text')
@click.option('--justify', is_flag=True)
def _format_text(text: click.STRING, justify: click.BOOL):
    formatted_text = format_text(text=text, justify=justify)
    time_now = datetime.now()
    with open(f'{time_now}.txt', 'w', encoding='utf-8') as file:
        file.write(formatted_text)

if __name__ == "__main__":
    _format_text()

