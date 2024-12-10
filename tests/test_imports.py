import importlib

import pytest


def test_import_awhere() -> None:
    """Test that awhere package can be imported.

    We use the importlib to import the package.
    """
    try:
        importlib.import_module('awhere')
    except ImportError as e:
        pytest.fail(f'Failed to import awhere: {str(e)}')


def test_import_all_awhere_examples_modules() -> None:
    """Test importing all modules in apps/awhere_examples directory."""
    import os
    import pathlib

    # Get path relative to test file location
    test_dir = pathlib.Path(__file__).parent
    examples_dir = test_dir.parent / 'apps' / 'awhere_examples'
    if not examples_dir.exists():
        pytest.skip('apps/awhere_examples directory not found')

    failed_imports: list[str] = []

    for root, _, files in os.walk(examples_dir):
        for file in files:
            if (
                file.endswith('.py')
                and not file.startswith('_')
                and not file.startswith('.')
            ):
                rel_path = pathlib.Path(root).relative_to(examples_dir.parent)
                module_path = '.'.join(rel_path.parts + (file[:-3],))

                try:
                    importlib.import_module(module_path)
                except ImportError as e:
                    failed_imports.append(f'{module_path}: {str(e)}')

    if failed_imports:
        pytest.fail(
            'Failed to import the following modules:\n'
            + '\n'.join(f'  - {err}' for err in failed_imports)
        )
