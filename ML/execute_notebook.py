"""Execute the assessment notebook with the active Python interpreter."""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory

import nbformat
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpec, KernelSpecManager
from nbclient import NotebookClient


def main():
    notebook_path = Path(__file__).resolve().with_name('blood_pressure_regression.ipynb')
    notebook = nbformat.read(notebook_path, as_version=4)
    with TemporaryDirectory(prefix='bioinf-kernel-') as resource_dir:
        specification = KernelSpec(
            argv=[sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
            display_name='BIOINF III', language='python', resource_dir=resource_dir)
        manager = KernelSpecManager(ensure_native_kernel=False)
        manager.get_kernel_spec = lambda name: specification
        kernel = KernelManager(kernel_name='bioinf-iii', kernel_spec_manager=manager)
        client = NotebookClient(notebook, km=kernel, timeout=1800,
                                resources={'metadata': {'path': str(notebook_path.parent)}})
        client.execute()
    nbformat.write(notebook, notebook_path)
    print(f'Executed {sum(cell.cell_type == "code" for cell in notebook.cells)} code cells.')


if __name__ == '__main__':
    main()
