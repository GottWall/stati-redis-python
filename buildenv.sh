#!/bin/sh

py(){
	virtualenv --python=python2.7 --clear venv
	. venv/bin/activate
	./venv/bin/easy_install pip
}

case $1 in
	"py") py;;

	*) py;;
esac