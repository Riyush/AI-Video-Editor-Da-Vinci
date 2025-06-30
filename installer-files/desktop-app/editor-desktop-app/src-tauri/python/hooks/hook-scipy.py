from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_data_files

hiddenimports = collect_submodules('scipy') + ['scipy.special._cdflib']

datas = collect_data_files('scipy')