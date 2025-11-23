#!/usr/bin/env python3
"""
Alternative build script using cx_Freeze for creating executable
This is a backup option if PyInstaller doesn't work well
"""

import sys
import os
from cx_Freeze import setup, Executable

# Define the main script
main_script = "main_exe.py"

# Define packages to include
packages = [
    "django",
    "tensorflow",
    "keras_self_attention", 
    "keras_multi_head",
    "PIL",
    "numpy",
    "scikit_learn",
    "matplotlib",
    "seaborn",
    "visualkeras",
    "myapp",
    "minor"
]

# Define files to include
include_files = [
    ("minor/", "minor/"),
    ("hair-diseases.h5", "hair-diseases.h5"),
    ("frontend/", "frontend/"),
]

# Define excludes (packages that cause issues)
excludes = [
    "tkinter",
    "unittest",
    "email",
    "http",
    "urllib",
    "xml",
    "pydoc",
    "doctest",
    "argparse",
    "difflib",
    "calendar",
    "pdb",
    "profile",
    "pstats",
    "tabnanny",
    "timeit",
    "trace",
    "distutils",
    "setuptools",
    "pip",
    "wheel"
]

# Build options
build_exe_options = {
    "packages": packages,
    "excludes": excludes,
    "include_files": include_files,
    "optimize": 2,
    "build_exe": "dist_cx_freeze"
}

# Create executable
executable = Executable(
    main_script,
    base="Console",
    target_name="HairDiseasePrediction.exe",
    icon=None
)

# Setup
setup(
    name="Hair Disease Prediction",
    version="1.0",
    description="Hair Disease Prediction Application",
    options={"build_exe": build_exe_options},
    executables=[executable]
)
