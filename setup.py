from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='revendeurapi',
    version='1.0.0',
    description='',
    author='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements
)
