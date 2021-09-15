CREATE = create.sql
DB = concepts.db

db:
	rm -f $(DB) && sqlite3 $(DB) < $(CREATE)

orm:
	pwiz.py -e sqlite $(DB) > concepts.py

umlsload:
	./load_umls.py -d $(DB) ../data/MRCONSO.RRF

snoload:
	./load_snomed.py -d $(DB) ../data/snomed/CONCEPT.tsv

link:
	./link.py -d $(DB) ../data/sdtm_terms.txt

install:
	python3 -m pip install -r requirements.txt
