PYTHON = python

all: server

server:
	nohup $(PYTHON) Backend/manage.py runserver opendsa.cc.vt.edu:8090 &
