from setuptools import setup, find_packages

setup(
    name='floras_helpers',       # Replace with your package name
    version='0.1.0',                # Initial release version
    description='A collection of utility functions for plotting, spike data, and video processing',
    author='Flora Takacs',            
    url='https://github.com/username/floras-helpers',  # Link to your repository (optional)
    packages=find_packages(where="src"),   # Automatically find packages in the "src" folder
    package_dir={'': 'src'},               # Define the source code directory
    install_requires=[                     # List of dependencies
        'numpy>=1.19.2',
        'matplotlib>=3.3.0',
        'pyperclip>=1.9.0',
        'scipy'
    ],
    classifiers=[                          # Optional metadata for PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',               # Specify the minimum Python version
)