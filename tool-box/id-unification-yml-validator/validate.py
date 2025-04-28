# import os
# import sys
# os.system(f"{sys.executable} -m pip install pyyaml")
# os.system(f"{sys.executable} -m pip install cerberus")

import json
import yaml
from cerberus import Validator

def load_doc():
    unify_yml = '''name: production
keys:
  - name: td_client_id
    valid_regexp: "[0-9a-fA-F]{8}-..."
    invalid_texts: ['']
 
  - name: td_global_id
    valid_regexp: "[0-9a-fA-F]{8}-..."
    invalid_texts: ['', '0000000000-...']
 
  - name: email
    valid_regexp: ".*@.*"
 
tables:
  - database: prod
    table: pageviews
    incremental_columns: [updated_at, id]
    key_columns:
       - {column: td_client_id, key: td_client_id}

  - database: brand2
    table: pageviews
    as: brand2_pageviews
    key_columns:
      - {column: td_client_id, key: td_client_id}
      - {column: td_global_id, key: td_global_id}
      - {column: email, key: email}
 
  - database: prod
    table: contacts
    key_columns:
      - {column: email, key: email}
 
canonical_ids:
  - name: browser_id
    merge_by_keys: [td_client_id, td_global_id, td_ssc_id]
 
  - name: marketing_id
    merge_by_canonical_ids: [browser_id]
    merge_by_keys: [email]
    source_tables: [pageviews, contacts]
 
  - name: contact_id
    merge_by_canonical_ids: [browser_id]
    merge_by_keys: [membership_id, email]
    merge_iterations: 3
    incremental_merge_iterations: 2
 
master_tables:
  - name: marketing_master
    canonical_id: browser_id
 
    attributes:
      - name: browser_id
        source_canonical_id: browser_id
 
      - name: email
        source_columns:
          - {table: contacts, column: email}

      - name: email
        source_columns:
          - {table: contacts, column: email}'''
          
    
    try:
        return yaml.safe_load(unify_yml)
    except yaml.YAMLError as exception:
        print('UNIFICATION YML COULD NOT BE LOADED. DOCUMENT IS NOT IN YAML FORMAT:')
        print(exception.problem)
        print(exception.problem_mark)

schema = {
    "name": {"required": True, "type": "string"},
    "keys": {
        "required": True,
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"required": True, "type": "string"},
                "valid_regexp": {"type": "string"},
                "invalid_texts": {"type": "list"},
            },
        },
    },
    "tables": {
        "required": True,
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "database": {"required": True, "type": "string"},
                "table": {"type": "string"},
                "as": {"type": "string"},
                "incremental_columns": {"type": "list"},
                "key_columns": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "column": {"type": "string"},
                            "key": {"type": "string"},
                        },
                    },
                },
            },
        },
    },
    "canonical_ids": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string"},
                "merge_by_keys": {"type": "list"},
                "merge_by_canonical_ids": {"type": "list"},
                "source_tables": {"type": "list"},
                "merge_iterations": {"type": "integer", "min":0, "max":50},
                "incremental_merge_iterations": {"type": "integer", "min":0, "max":50},
            },
        },
    },
    "master_tables": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string"},
                "canonical_id": {"type": "string"},
                "attributes": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "name": {"type": "string"},
                            "source_canonical_id": {"type": "string"},
                            "source_columns": {
                                "type": "list",
                                "schema": {
                                    "type": "dict",
                                    "schema": {
                                        "table": {"type": "string"},
                                        "column": {"type": "string"},
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}

def main():
    v = Validator(schema)
    doc = load_doc()

    if doc is None:
        return None

    if v.validate(doc, schema):
        print("NO VALIDATION ERRORS FOUND")
    else:
        print("SCHEMA IS INVALID. ERRORS:")
        formatted = json.dumps(v.errors, indent=4)
        print(formatted)


main()