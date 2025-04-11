# pip install pyyaml
# pip install cerberus
import json
import yaml
from cerberus import Validator

def load_doc():
    with open('./yml/unify1.yml', 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exception:
            raise exception

schema = eval(open('./schema.py', 'r').read())
v = Validator(schema)
doc = load_doc()

if v.validate(doc, schema):
    print("yml is VALID")
else:
    print("yml is INVALID")
    formatted = json.dumps(v.errors, indent=4)
    print(formatted)