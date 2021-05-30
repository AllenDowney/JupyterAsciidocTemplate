import nbformat as nbf
from glob import glob
from pypandoc import convert_text
import re

# Text to look for in adding tags
tag_search_dict = {
    "remove-cell": "#hide\n",
    "hide-cell": "#hide\n",
    "remove-input": "#hide_input\n",
    "hide-input": "#hide_input\n",
    "remove-output": "#hide_output\n",
    "hide-output": "#hide_output\n",
}

def remove_border(path):
    """Remove the border tag from HTML tables.
    """
    with open(path) as fin:
        lines = fin.read().split('\n')

    for i in range(len(lines)):
        line = lines[i]
        if '<table border=' in line:
            lines[i] = re.sub(r'border=\\"1\\" ', r'', line)

    with open(path, 'w') as fout:
        fout.write('\n'.join(lines))


def process_output(output):
    data = output.get('data', {})
    html = data.get('text/html', [])
    # Turns out that nbf.read does some processing
    # that makes it hard to make simple text changes


def convert_line(line):
    """Convert a line to asciidoc."""
    line = convert_text(line, 'asciidoc', format='gfm',
                    extra_args=['--wrap=none'])
    return line


def convert_quote(i, lines, res):
    """Convert block quote to a raw asciidoc block."""
    res.append('```asciidoc')
    res.append('____')

    while i < len(lines):
        line = lines[i]
        if not line.startswith('>'):
            break
        res.append(convert_line(line[1:]))
        i += 1

    res.append('____')
    res.append('```')
    return i


def process_quotes(text):
    """Convert block quotes to asciidoc."""
    res = []
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('>'):
            i = convert_quote(i, lines, res)
        else:
            res.append(line)
        i += 1
    return '\n'.join(res)


def process_cell(cell):
    # process block quotes
    if cell['cell_type'] == 'markdown':
        source = cell['source']
        cell['source'] = process_quotes(source)

    # remove solutions
    if cell['cell_type'] == 'code':
        source = cell['source']
        if source.startswith('# Solution'):
            cell['source'] = '#hide'

    # move tags into comments for fastdoc
    cell_tags = cell.get('metadata', {}).get('tags', [])
    for key, val in tag_search_dict.items():
        if key in cell_tags:
            cell['source'] = val + cell['source']

    # process the outputs
    for output in cell.get('outputs', []):
        process_output(output)


def process_notebook(path):
    ntbk = nbf.read(path, nbf.NO_CONVERT)

    for cell in ntbk.cells:
        process_cell(cell)

    nbf.write(ntbk, path)


# Collect a list of the notebooks in the content folder
paths = glob("chap*.ipynb")

for path in sorted(paths):
    print('Prepping', path)
    process_notebook(path)
    remove_border(path)
