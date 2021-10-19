# Loading PostgreSQL

This directory contains the SQLite schema in the file _create.sqlite_. 
I generated a Pg version using SQL::Translator:

```
$ sqlt -f SQLite -t PostgreSQL create.sqlite > create.pg
```

I loaded that into Pg:

```
$ psql concepts < create.pg
```

Then I loaded the UMLS _MRCONSO.csv_ data using the `psql` console:

```
\COPY umls_concept from 'MRCONSO.csv' DELIMITER E',' CSV ENCODING 'UTF8';
```
