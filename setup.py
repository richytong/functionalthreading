from setuptools import setup
from package import version

setup(
    name='functionalthreading',
    version=version,
    description='Functional programming with thread-based parallelism.',
    packages=['package', 'functions'],
)
