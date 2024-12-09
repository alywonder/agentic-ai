import importlib

import pytest

# def iter_modules(package_dir: Path) -> Iterator[str]:
#     """Iterate through all Python modules in the given directory."""
#     for item in package_dir.rglob('*.py'):
#         if item.is_file():
#             # Convert path to module name
#             relative_path = item.relative_to(package_dir.parent)
#             module_name = str(relative_path).replace('/', '.').replace('\\', '.')[:-3]
#             # Skip __init__.py files
#             if not module_name.endswith('__init__'):
#                 yield module_name


# def get_all_modules() -> list[str]:
#     """Get all Python modules in the project."""
#     modules: list[str] = []

#     root_dir = Path(__file__).parent.parent

#     # Add modules from apps directory
#     apps_dir = root_dir / 'apps'
#     if apps_dir.exists():
#         for app_dir in apps_dir.iterdir():
#             if app_dir.is_dir() and not app_dir.name.startswith('.'):
#                 modules.extend(iter_modules(app_dir))

#     # Add modules from libs directory
#     libs_dir = root_dir / 'libs'
#     if libs_dir.exists():
#         for lib_dir in libs_dir.iterdir():
#             if lib_dir.is_dir() and not lib_dir.name.startswith('.'):
#                 modules.extend(iter_modules(lib_dir / 'src'))

#     return modules


# @pytest.mark.parametrize('module_name', get_all_modules())
# def test_module_can_be_imported(module_name: str) -> None:
#     """Test that each module can be imported without errors."""
#     try:
#         importlib.import_module(module_name)
#     except ImportError as e:
#         pytest.fail(f'Failed to import {module_name}: {str(e)}')


def test_import_awhere() -> None:
    """Test that awhere package can be imported."""
    try:
        importlib.import_module('awhere')
    except ImportError as e:
        pytest.fail(f'Failed to import awhere: {str(e)}')


def test_import_awhere_examples() -> None:
    """Test that awhere_examples package can be imported."""
    try:
        importlib.import_module('awhere_examples')
    except ImportError as e:
        pytest.fail(f'Failed to import awhere_examples: {str(e)}')
