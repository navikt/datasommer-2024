import setuptools

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")


setuptools.setup(
    name="lokal-pakke",
    version="0.1",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    author="NAV IKT",
    description="Lokal pythonpakke for demo-repo",
)