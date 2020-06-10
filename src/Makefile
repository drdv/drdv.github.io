FILES = $(wildcard *.jemdoc)

all: jomdoc
	mv *.html ..
	rm -rf ../eqs
	mv eqs ..

jomdoc:
	./jemdoc.py ${FILES}
