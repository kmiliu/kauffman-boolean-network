"""Execute the analysis notebook in order, from any working directory."""
import json
import os
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    os.chdir(root)
    os.environ.setdefault('MPLBACKEND', 'Agg')
    notebook = json.loads((root / 'kauffman-boolean-network.ipynb').read_text())
    scope = {'__name__': '__main__'}
    for index, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code':
            exec(compile(''.join(cell['source']), f'notebook-cell-{index}', 'exec'), scope)


if __name__ == '__main__':
    main()
