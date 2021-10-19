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
poetry build
poetry publish

#echo Dokumentation erstellen und hochladen
#doxygen
# TODO Move doc into repo
# python3 setup.py upload_docs --upload-dir doc/html
