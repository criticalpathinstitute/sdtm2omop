# SDTM to OMOP via UMLS

I ended up using SQLite for most of this work, so see the "sqlite" directory for everything.

## SDTM Term from NIH

To start, I downloaded the [SDTM terminology](https://evs.nci.nih.gov/ftp1/CDISC/SDTM/SDTM%20Terminology.txt) from NIH.
There is a "make sdtm" shortcut for this.
Here is the structure of this file:

```
$ csvchk data/sdtm_terms.txt
// ****** Record 1 ****** //
Code                         : C141657
Codelist Code                :
Codelist Extensible (Yes/No) : No
Codelist Name                : 10-Meter Walk/Run Functional Test Test Code
CDISC Submission Value       : TENMW1TC
CDISC Synonym(s)             : 10-Meter Walk/Run Functional Test Test Code
CDISC Definition             : 10-Meter Walk/Run test code.
NCI Preferred Term           : CDISC Functional Test 10-Meter Walk/Run Test Code Terminology
```

## UMLS Concepts

Once I got a UMLS license, I was able to download the file MRCONSO.RRF containing UMLS concepts:

* [Metathesaurus](https://www.ncbi.nlm.nih.gov/books/NBK9685/)
* [Concept Names and Sources](https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.concept_names_and_sources_file_mr/?report=objectonly)

This is a pipe-delimited file with fields defined in the second link, and it contains 16,132,274 records.
I first wrote a Python program (sqlite/load_umls.py) to import these into an SQLite database.
It ran for a few hours and loaded ~5M, but then performance tanked.
I estimated it would probably run for days to finish.

I decided instead to attempt a direct load of the data by SQLite into a new table.
This requires CSV (comma-separated values) format, so I wrote a Python program to convert the MRCONSO.RRF to MRCONSO.csv (sqlite/pipe2csv.py).
This also has the benefit of naming the fields, so the output file has the following structure:

```
$ csvchk data/MRCONSO.csv
// ****** Record 1 ****** //
cui         : C0000005
language    : ENG
term_status : P
lui         : L0000005
string_type : PF
sui         : S0007492
atom_status : Y
aui         : A26634265
saui        :
scui        : M0019694
sdui        : D012711
source_name : MSH
term_type   : PEP
code        : D012711
string      : (131)I-Macroaggregated Albumin
srl         : 0
suppress    : N
cvf         : 256
```

I then used the SQLite interface to load this file into a new "umls_concept" table.
The following command finished loading the entire file in a minute or two:

```
sqlite> .mode csv
sqlite> .import ../data/MRCONSO.csv umls_concept
sqlite> select count(*) from umls_concept;
16132274
```

SQLite generated the following table.
Note that I added the two indexes to aid in searching:

```
sqlite> .schema umls_concept
CREATE TABLE umls_concept(
  "cui" TEXT,
  "language" TEXT,
  "term_status" TEXT,
  "lui" TEXT,
  "string_type" TEXT,
  "sui" TEXT,
  "atom_status" TEXT,
  "aui" TEXT,
  "saui" TEXT,
  "scui" TEXT,
  "sdui" TEXT,
  "source_name" TEXT,
  "term_type" TEXT,
  "code" TEXT,
  "string" TEXT,
  "srl" TEXT,
  "suppress" TEXT,
  "cvf" TEXT
);
CREATE INDEX cui on umls_concept (cui);
CREATE INDEX code on umls_concept (code);
```

## SNOMED Concepts

I downloaded the SNOMED Clinical Terms (IHTSDO) file from Athena/ohdsi.org.
I had to request the file and wait for an email that directed me to a link, so I cannot provide that here.
What I got was a zip file containing the following files:

* CONCEPT.tsv
* CONCEPT_ANCESTOR.csv
* CONCEPT_CLASS.csv
* CONCEPT_RELATIONSHIP.csv
* CONCEPT_SYNONYM.csv
* DOMAIN.csv
* DRUG_STRENGTH.csv
* RELATIONSHIP.csv
* VOCABULARY.csv

I loaded the 1,242,709 records in CONCEPT.tsv file into the "snomed_concept" table in the same SQLite database as the UMLS terms using a Python program (sqlite/load_snomed.py).

## Linking SDTM Terms

The Python program sqlite/link.py will link the data/sdtm_terms.txt to their SNOMED concepts using the SQLite database that contains the UMLS/SNOMED terms.
The "make link" shortcut in the "sqlite" director will run this.
By default, it will create the output file "umls_snomed_concepts.tsv" which finds 6530 SDTM terms with SNOMED concepts.
This file has the following structure:

```
$ csvchk umls_snomed_concepts.tsv
// ****** Record 1 ****** //
sdtm_ct_code           : C101940
cdisc_submission_value : AVL01-List A Recall 3 Word 11
cui                    : C0530839
snomed_code            : 707173007
concept_id             : 45768690
```

## Author

Ken Youens-Clark <kyclark@c-path.org>
