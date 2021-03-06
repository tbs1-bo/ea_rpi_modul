#!/bin/sh

echo Tests laufen lassen
python3 setup.py test
echo Unit Tests OK?
read

for f in eapi/*py;
do
	python3 -m doctest $f
	echo Doctests $f ok?
	read
done

echo Release erstellen und hochladen
python3 setup.py sdist upload
echo Release OK?
read

echo Dokumentation erstellen und hochladen
doxygen
python3 setup.py upload_docs --upload-dir doc/html

echo git commit?
read
git commit -av

echo Tag erstellen und pushen?
git tag -a v`python3 -c 'import eapi;print(eapi.VERSION)'`
git push --tags
