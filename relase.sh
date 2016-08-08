#!/bin/sh

echo Tests laufen lassen
python3 setup.py test

echo Tests OK?
read

echo Release erstellen und hochladen
python3 setup.py sdist upload

echo Release OK?
read

echo Dokumentation erstellen
doxygen

echo Dokumentation hochladen
python3 setup.py upload_docs
