# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# Get the current directory
current_dir = Path.cwd()

# Define paths
django_dir = current_dir / "minor"
model_file = current_dir / "hair-diseases.h5"

# Collect all Django files
django_files = []
for root, dirs, files in os.walk(django_dir):
    for file in files:
        if file.endswith(('.py', '.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico')):
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, current_dir)
            django_files.append((src_path, os.path.dirname(rel_path)))

# Collect model file
model_files = []
if model_file.exists():
    model_files.append((str(model_file), '.'))

# Collect frontend files
frontend_files = []
frontend_dir = current_dir / "frontend"
if frontend_dir.exists():
    for root, dirs, files in os.walk(frontend_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, current_dir)
            frontend_files.append((src_path, os.path.dirname(rel_path)))

block_cipher = None

a = Analysis(
    ['main_exe.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=django_files + model_files + frontend_files,
    hiddenimports=[
        'django',
        'django.core',
        'django.core.management',
        'django.core.management.commands',
        'django.core.management.commands.runserver',
        'django.core.management.commands.migrate',
        'django.db',
        'django.db.models',
        'django.contrib',
        'django.contrib.auth',
        'django.contrib.auth.models',
        'django.contrib.auth.forms',
        'django.contrib.admin',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'django.contrib.sessions.backends.db',
        'django.contrib.auth.backends',
        'django.contrib.auth.backends.ModelBackend',
        'django.contrib.sessions.models',
        'django.contrib.contenttypes.models',
        'django.contrib.sites.models',
        'django.contrib.admin.apps',
        'django.contrib.auth.apps',
        'django.contrib.contenttypes.apps',
        'django.contrib.sessions.apps',
        'django.contrib.sites.apps',
        'django.contrib.staticfiles.apps',
        'django.contrib.messages.apps',
        'django.contrib.messages.storage',
        'django.contrib.messages.storage.fallback',
        'django.contrib.messages.storage.session',
        'django.contrib.messages.storage.cookie',
        'django.contrib.messages.context_processors',
        'django.contrib.messages.middleware',
        'django.contrib.messages.utils',
        'django.contrib.messages.constants',
        'django.contrib.messages.api',
        'django.contrib.messages.models',
        'django.contrib.messages.views',
        'django.contrib.messages.forms',
        'django.contrib.messages.templatetags',
        'django.contrib.messages.templatetags.messages',
        'django.contrib.messages.templatetags.messages_extras',
        'django.contrib.messages.templatetags.messages_extras.messages',
        'django.contrib.messages.templatetags.messages_extras.messages_extras',
        'django.contrib.messages.templatetags.messages_extras.messages_extras_extras',
        'tensorflow',
        'tensorflow.keras',
        'tensorflow.keras.models',
        'tensorflow.keras.layers',
        'tensorflow.keras.utils',
        'tensorflow.keras.applications',
        'tensorflow.keras.preprocessing',
        'tensorflow.keras.preprocessing.image',
        'tensorflow.keras.backend',
        'tensorflow.keras.optimizers',
        'tensorflow.keras.losses',
        'tensorflow.keras.metrics',
        'tensorflow.keras.callbacks',
        'tensorflow.keras.initializers',
        'tensorflow.keras.regularizers',
        'tensorflow.keras.constraints',
        'tensorflow.keras.activations',
        'tensorflow.keras.utils.generic_utils',
        'tensorflow.keras.utils.data_utils',
        'tensorflow.keras.utils.io_utils',
        'tensorflow.keras.utils.layer_utils',
        'tensorflow.keras.utils.model_utils',
        'tensorflow.keras.utils.np_utils',
        'tensorflow.keras.utils.tf_utils',
        'tensorflow.keras.utils.vis_utils',
        'tensorflow.keras.utils.conv_utils',
        'tensorflow.keras.utils.generic_utils',
        'tensorflow.keras.utils.data_utils',
        'tensorflow.keras.utils.io_utils',
        'tensorflow.keras.utils.layer_utils',
        'tensorflow.keras.utils.model_utils',
        'tensorflow.keras.utils.np_utils',
        'tensorflow.keras.utils.tf_utils',
        'tensorflow.keras.utils.vis_utils',
        'tensorflow.keras.utils.conv_utils',
        'keras_self_attention',
        'keras_multi_head',
        'PIL',
        'PIL.Image',
        'numpy',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'visualkeras',
        'myapp',
        'myapp.models',
        'myapp.views',
        'myapp.ml_service',
        'myapp.apps',
        'myapp.admin',
        'myapp.tests',
        'myapp.middleware',
        'minor',
        'minor.settings',
        'minor.urls',
        'minor.wsgi',
        'minor.asgi',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='HairDiseasePrediction',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
