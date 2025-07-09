from setuptools import setup, find_packages


setup(
    name='informatik_sem2',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',      # Abhängigkeiten hier
        'pandas',
        "sympy",
        "matplotlib"
    ],
    author='Marlon E.',
    description='Tools für das 2. Semester in "Angewante Informatik" & "Data Science"',
    url='https://github.com/Marlon1325/informatik_sem2',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.12',
)
