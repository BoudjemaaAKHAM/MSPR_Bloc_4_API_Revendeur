from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("revendeurapi/__init__.py") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.strip().split("=")[-1].strip(" '\"")
            break
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name='revendeurapi',
    version=version,
    description='Revendeur API',
    author='EPSI Grenoble I1 Dev Groupe 3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements
)
