import setuptools


# gemäß der Beschreibung von
# https://packaging.python.org/distributing/
setuptools.setup(
    name="eapi",
    version="0.1.1",
    description="Modul zur Ansteuerung eines EA-Moduls fuer den Raspberry Pi.",
    author="Marco Bakera",
    packages=setuptools.find_packages())
