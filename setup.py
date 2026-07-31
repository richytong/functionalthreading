from setuptools import setup
from tomllib import load

with open('pyproject.toml', 'rb') as file:
    pyproject = load(file)

    setup(
        name='functionalthreading',
        version=pyproject['project']['version'],
        description='Functional programming with thread-based parallelism',
        packages=[
            'functionalthreading',
            'functionalthreading.classes',
            'functionalthreading.functions',
        ],
    )
