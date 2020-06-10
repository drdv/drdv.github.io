FILES = $(wildcard *.jemdoc)

all: jomdoc
	mv *.html ..
	mv eqs ..

jomdoc:
	./jemdoc.py ${FILES}
