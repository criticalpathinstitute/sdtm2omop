create table umls_concept (
    umls_concept_id integer primary key,
    cui text,
    language text,
    term_status text,
    lui text,
    string_type text,
    sui text,
    atom_status text,
    aui text,
    saui text,
    scui text,
    sdui text,
    source_name text,
    term_type text,
    code text,
    string text,
    srl text,
    suppress text,
    cvf text
);

create index cui on umls_concept (cui);
create index code on umls_concept (code);

create table snomed_concept (
    snomed_concept_id integer primary key,
    concept_id text,
    concept_name text,
    domain_id text,
    vocabulary_id text,
    concept_class_id text,
    standard_concept text,
    concept_code text,
    valid_start_date text,
    valid_end_date text,
    invalid_reason text
);

create index concept_code on snomed_concept (concept_code);
