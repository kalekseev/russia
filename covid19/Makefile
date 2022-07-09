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

# pull.rosstat.05-2022
pull.rosstat.%:
	curl https://rosstat.gov.ru/storage/mediabank/edn_$(subst pull.rosstat.,,$@)-2022_t1_1.xlsx -O
