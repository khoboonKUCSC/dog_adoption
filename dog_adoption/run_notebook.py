"""Execute the Dog_Adoption.ipynb notebook in-place to populate all cell outputs."""
import nbformat
from nbformat.v4 import new_output
import sys, io, os, base64, traceback

os.environ['MPLBACKEND'] = 'Agg'

nb_path = 'Dog_Adoption.ipynb'
nb = nbformat.read(nb_path, as_version=4)

namespace = {'__name__': '__main__'}

import matplotlib
matplotlib.use('Agg')

cell_count = sum(1 for c in nb.cells if c.cell_type == 'code')
executed = 0
errors = 0

for i, cell in enumerate(nb.cells):
    if cell.cell_type != 'code':
        continue
    executed += 1
    if executed % 10 == 0 or executed == 1:
        print(f"  Executing code cell {executed}/{cell_count} ...", flush=True)
    cell.outputs = []
    source = cell.source

    old_stdout = sys.stdout
    sys.stdout = captured = io.StringIO()

    import matplotlib.pyplot as plt
    plt.close('all')

    try:
        exec(compile(source, f'<cell-{i}>', 'exec'), namespace)
    except Exception:
        sys.stdout = old_stdout
        tb = traceback.format_exc()
        errors += 1
        print(f"    ERROR in cell {executed}: {tb[:300]}")
        cell.outputs.append(new_output(output_type='stream', name='stderr', text=tb))
        continue
    finally:
        sys.stdout = old_stdout

    stdout_text = captured.getvalue()
    if stdout_text:
        cell.outputs.append(new_output(output_type='stream', name='stdout', text=stdout_text))

    for fig_num in plt.get_fignums():
        fig = plt.figure(fig_num)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=130)
        buf.seek(0)
        img_data = base64.b64encode(buf.read()).decode('ascii')
        cell.outputs.append(nbformat.v4.new_output(
            output_type='display_data',
            data={'image/png': img_data},
            metadata={'image/png': {'width': 900}}
        ))
        plt.close(fig)

nbformat.write(nb, nb_path)
print(f"\n[OK] Notebook executed: {executed} code cells, {errors} errors")
