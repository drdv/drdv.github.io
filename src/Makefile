FILES = $(wildcard *.jemdoc)

jemdoc:
	docker run -it --rm -w /home/site --volume ${PWD}:/home/site jemdoc jemdoc.py ${FILES}
