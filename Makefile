all:
	@echo "Be reasonable, check available targets!"

deploy: jemdoc
	mv src/*.html .
	rm -rf eqs
	mv src/eqs .

jemdoc:
	cd src && make jemdoc

docker-build:
	docker build -t jemdoc .
