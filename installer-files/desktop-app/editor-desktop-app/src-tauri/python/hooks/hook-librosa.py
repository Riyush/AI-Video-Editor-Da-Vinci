from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Include all librosa submodules (like librosa.core, librosa.feature, etc.)
hiddenimports = collect_submodules('librosa')

# Include librosa's data files (like example audio, metadata, etc.)
datas = collect_data_files('librosa')