from peewee import *

database = SqliteDatabase('concepts.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class SnomedConcept(BaseModel):
    concept_class_id = TextField(null=True)
    concept_code = TextField(index=True, null=True)
    concept_id = TextField(null=True)
    concept_name = TextField(null=True)
    domain_id = TextField(null=True)
    invalid_reason = TextField(null=True)
    snomed_concept_id = AutoField(null=True)
    standard_concept = TextField(null=True)
    valid_end_date = TextField(null=True)
    valid_start_date = TextField(null=True)
    vocabulary_id = TextField(null=True)

    class Meta:
        table_name = 'snomed_concept'

class UmlsConcept(BaseModel):
    atom_status = TextField(null=True)
    aui = TextField(null=True)
    code = TextField(null=True)
    cui = TextField(null=True)
    cvf = TextField(null=True)
    language = TextField(null=True)
    lui = TextField(null=True)
    saui = TextField(null=True)
    scui = TextField(null=True)
    sdui = TextField(null=True)
    source_name = TextField(null=True)
    srl = TextField(null=True)
    string = TextField(null=True)
    string_type = TextField(null=True)
    sui = TextField(null=True)
    suppress = TextField(null=True)
    term_status = TextField(null=True)
    term_type = TextField(null=True)

    class Meta:
        table_name = 'umls_concept'
        primary_key = False

