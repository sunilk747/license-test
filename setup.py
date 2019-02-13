
"""Setup Script."""

from setuptools import setup, find_packages
from pathlib import Path


def _get_requirements():
    with open('requirements.txt') as _file:
        return _file.readlines()


def _get_long_description():
    cur_dir = Path(__file__).absolute().parent
    readme_file = cur_dir.joinpath('README').with_suffix('.md')
    with open(str(readme_file)) as _file:
        return _file.read()


setup(
    name="emrtest",
    version='0.1',
    description="ML utility library for fabric8-analytics",
    long_description=_get_long_description(),
    author='Ravindra Ratnawat',
    author_email="ravindra@redhat.com",
    license='APACHE 2.0',
    url='https://github.com/sunilk747/license-test',
    keywords=['Fabric8-Analytics', 'Machine-Learning', 'Utility'],
    python_requires='>=3.4',
    packages=find_packages(exclude=['tests']),
    install_requires=_get_requirements(),
)

