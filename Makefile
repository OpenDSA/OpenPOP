PYTHON = python

all: server

server:
	nohup $(PYTHON) Backend/manage.py runserver opendsa.cs.vt.edu:8090 &
