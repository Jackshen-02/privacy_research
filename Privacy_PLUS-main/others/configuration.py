STANFORD_COFIGURATION = {
    "DEFAULT_MODEL_PATH": "StanfordAIMI/stanford-deidentifier-base",
    "PRESIDIO_SUPPORTED_ENTITIES": [
        "LOCATION",
        "PERSON",
        "ORGANIZATION",
        "AGE",
        "PHONE_NUMBER",
        "EMAIL",
        "DATE_TIME",
        "DEVICE",
        "ZIP",
        "PROFESSION",
        "USERNAME",
        "ID"

    ],
    "LABELS_TO_IGNORE": ["O"],
    "DEFAULT_EXPLANATION": "Identified as {} by the StanfordAIMI/stanford-deidentifier-base NER model",
    "SUB_WORD_AGGREGATION": "simple",
    "DATASET_TO_PRESIDIO_MAPPING": {
        "DATE": "DATE_TIME",
        "DOCTOR": "PERSON",
        "PATIENT": "PERSON",
        "HOSPITAL": "LOCATION",
        "MEDICALRECORD": "ID",
        "IDNUM": "ID",
        "ORGANIZATION": "ORGANIZATION",
        "ZIP": "ZIP",
        "PHONE": "PHONE_NUMBER",
        "USERNAME": "USERNAME",
        "STREET": "LOCATION",
        "PROFESSION": "PROFESSION",
        "COUNTRY": "LOCATION",
        "LOCATION-OTHER": "LOCATION",
        "FAX": "PHONE_NUMBER",
        "EMAIL": "EMAIL",
        "STATE": "LOCATION",
        "DEVICE": "DEVICE",
        "ORG": "ORGANIZATION",
        "AGE": "AGE",
    },
    "MODEL_TO_PRESIDIO_MAPPING": {
        "PER": "PERSON",
        "PERSON": "PERSON",
        "LOC": "LOCATION",
        "ORG": "ORGANIZATION",
        "AGE": "AGE",
        "PATIENT": "PERSON",
        "HCW": "PERSON",
        "HOSPITAL": "LOCATION",
        "PATORG": "ORGANIZATION",
        "DATE": "DATE_TIME",
        "PHONE": "PHONE_NUMBER",
        "VENDOR": "ORGANIZATION",
    },
    "CHUNK_OVERLAP_SIZE": 40,
    "CHUNK_SIZE": 600,
    "ID_SCORE_MULTIPLIER": 0.4,
    "ID_ENTITY_NAME": "ID"
}


BERT_DEID_CONFIGURATION = {
    "PRESIDIO_SUPPORTED_ENTITIES": [
        "PERSON",
        "PHONE_NUMBER",
        "EMAIL",
        "URL"
    ],
    "DEFAULT_MODEL_PATH": "obi/deid_roberta_i2b2",
    "LABELS_TO_IGNORE": ["O"],
    "DEFAULT_EXPLANATION": "Identified as {} by the obi/deid_roberta_i2b2 NER model",
    "SUB_WORD_AGGREGATION": "simple",
    "DATASET_TO_PRESIDIO_MAPPING": {
        "DATE": "DATE_TIME",
        "DOCTOR": "PERSON",
        "PATIENT": "PERSON",
        "HOSPITAL": "ORGANIZATION",
        "MEDICALRECORD": "O",
        "IDNUM": "O",
        "ORGANIZATION": "ORGANIZATION",
        "ZIP": "O",
        "PHONE": "PHONE_NUMBER",
        "USERNAME": "",
        "STREET": "LOCATION",
        "PROFESSION": "PROFESSION",
        "COUNTRY": "LOCATION",
        "LOCATION-OTHER": "LOCATION",
        "FAX": "PHONE_NUMBER",
        "EMAIL": "EMAIL",
        "STATE": "LOCATION",
        "DEVICE": "O",
        "ORG": "ORGANIZATION",
        "AGE": "AGE",
        "URL": "URL",
    },
    "MODEL_TO_PRESIDIO_MAPPING": {
        "PER": "PERSON",
        "LOC": "LOCATION",
        "ORG": "ORGANIZATION",
        "AGE": "AGE",
        "ID": "ID",
        "EMAIL": "EMAIL",
        "PATIENT": "PERSON",
        "STAFF": "PERSON",
        "HOSP": "ORGANIZATION",
        "PATORG": "ORGANIZATION",
        "DATE": "DATE_TIME",
        "PHONE": "PHONE_NUMBER",
        "URL": "URL",
    },
    "CHUNK_OVERLAP_SIZE": 40,
    "CHUNK_SIZE": 600,
    "ID_SCORE_MULTIPLIER": 0.4,
    "ID_ENTITY_NAME": "ID"
}