all: pull.stopcoronavirus pull.rosstat parse

start:
	python -m http.server

pull.stopcoronavirus:
	curl https://raw.githubusercontent.com/alexei-kouprianov/COVID.2019.ru/master/data/momentary.txt | \
		grep deceased | \
		uniq | \
		sed 's|\s[^"]*||' | \
		grep -v '2020-03' | \
		tr '\t', '|' | \
		cut -d '|' -f1,5,6 | \
		tr '|' ',' | \
		sed 's|—|-|' | sed 's|АО|автономный округ|' | sed s'|область |область|' \
		> data/stopcoronavirus.csv

pull.rosstat:
	python fetch.py


parse:
	python parse.py
