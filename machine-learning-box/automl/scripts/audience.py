__all__ = ['CdpAudience']

import sys, os
import requests 
import json
import pytd
import re
from typing import Tuple

from requests.models import Response
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests import Session


class CdpApiClient:
    def __init__(self, endpoint, headers: dict) -> None:
        retry_strategy = Retry(
            total=3, status_forcelist=[429, 500, 502, 503, 504], backoff_factor=2
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        s = Session()
        s.headers = headers 
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        self.endpoint = f"https://{endpoint}"
        self.client: Session = s

    def get(self, path, **kwargs) -> Response:
        return self.client.get(url=self.endpoint+path, **kwargs)

    def put(self, path: str, data=None, **kwargs) -> Response:
        return self.client.put(url=self.endpoint+path, data=data, **kwargs)

    def post(self, path: str, data=None, json=None, **kwargs) -> Response:
        return self.client.post(url=self.endpoint+path, data=data, json=json, **kwargs)


def to_boolean(o) -> bool:
    if o == None:
        return False
    s = str(o)

    try:
        from distutils.util import strtobool
        return bool(strtobool(s))
    except ValueError as e:
        return False


def validate_db_resource_name(name: str) -> str:
    '''
    Validate DB_NAME or TABLE_NAME
    '''
    # https://docs.treasuredata.com/display/public/PD/Naming+Requirements+and+Restrictions+for+Treasure+Data+Entities
    TD_DB_RESOURCE_REGEX = "[a-z0-9_]+"
    assert re.fullmatch(rf"^{TD_DB_RESOURCE_REGEX}$", name) is not None, f"Invalid DB resource name: {name}"
    return name


def parse_table(table: str) -> Tuple[str, str]:
    '''
    Parse DB_NAME.TABLE_NAME to DB_NAME, TABLE_NAME
    '''
    assert table.count(".") == 1, f"Invalid table name {table}, DB_NAME.TABLE_NAME is expected."
    database, table = table.split(".")
    validate_db_resource_name(database)
    validate_db_resource_name(table)
    return database, table


def resolve_type(table, column_name: str):
    # workaround for ValueError: not enough values to unpack (expected 3, got 2)
    schema = [c if len(c) == 3 else [c[0], c[1], ""] for c in table.schema]
    # column_name:str, column_type:str, alias:str
    for (c_name, c_type, _) in schema:
        if c_name == column_name:
            # Note: Only string, number, timestamp, string_array, or number_array is accepted for attr_type
            # https://github.com/treasure-data/td-cdp-api/blob/master/app/models/audience_attribute.rb#L9
            # https://docs.treasuredata.com/display/PD/Using+TD+CLI+to+Annotate+Schema+-+Legacy
            if c_type in ['int', 'long', 'double', 'float']:
                return 'number'
            else:
                return 'string'
    raise KeyError(f"column {column_name} not found in {table.schema}")


class CdpAudience:
    '''
    Usage: 
      cdp = CdpAudience()
      cdp.add_attribute(audience_name=audience_name, attr_db=attr_db, attr_table=attr_table, attr_column=attr_column, join_key=join_key, foreign_key=foreign_key, replace_attr_if_exists=True)
    '''

    def __init__(self):
        TD_API_KEY = os.environ["TD_API_KEY"]
        TD_ENDPOINT = os.environ["TD_API_SERVER"]

        CDP_ENDPOINT = TD_ENDPOINT.replace('api', 'api-cdp')
        HEADERRS = {'Authorization': f'TD1 {TD_API_KEY}', 'Content-Type': 'application/json'}
        self.cdp_api = CdpApiClient(endpoint=CDP_ENDPOINT, headers=HEADERRS)
        self.td_api = pytd.Client(retry_post_requests=True).api_client

    def add_attribute(
        self, *, audience_id: str=None, audience_name: str=None, attr_db: str=None, attr_table: str, attr_column: str, join_key: str, foreign_key: str, 
        attr_alias: str=None, attr_group: str="AutoML", rerun_master_segment: bool=True, replace_attr_if_exists: bool=False,
        **kwargs
    ):
        if attr_alias is None:
            attr_alias = attr_column

        if attr_db is None:
            attr_db, attr_table = parse_table(attr_table)

        if audience_id is None:
            assert audience_name is not None, "Either audience_id or audience_name argument is required"
            audience_id = self.get_parent_segment_id(audience_name)

        table = self.td_api.table(attr_db, attr_table)
        attr_type = resolve_type(table, attr_column)

        res = self.cdp_api.put(f"/audiences/{audience_id}")
        if not res.ok:
            raise RuntimeError(res.text)
        audience = res.json()
        attributes = audience['attributes'] if 'attributes' in audience else []

        new_attr = {
            'audienceId': audience_id,        # ID of Master Segment for this attribute
            'name': attr_column,              # Column name to be defined on Master Segment
            'type': attr_type,                # Type of the column 
            'parentDatabaseName': attr_db,    # Database name of the attribute table
            'parentTableName': attr_table,    # Table name of the attribute table
            'parentColumn': attr_column,      # Column name of the attribute table which is imported into customer table
            'parentKey': join_key,            # Join key of the attribute table
            'foreignKey': foreign_key,        # Foreign key of the master table
            'groupingName': attr_group,       # Group name of the attribute
        }

        append_attr = False
        for i, attr in enumerate(attributes):
            if 'name' in attr and attr['name'] == attr_column:
                if replace_attr_if_exists:
                    attributes[i] = new_attr
                    append_attr = False
                    print(f"⚠ Repalce '{attr_column}' in Master Segment {audience_id}", file=sys.stderr) 
                    break
                else:
                    print(f"⚠ skip adding an attribute because the attribute column '{attr_column}' already exists", file=sys.stderr) 
                    return
        if append_attr == True:
            attributes.append(new_attr)

        res = self.cdp_api.put(f"/audiences/{audience_id}", json=audience)
        if res.ok:
            print(f"ⓘ Successfully added an attribute table '{attr_table}' to master segment {audience_id}", file=sys.stderr) 
        else:
            try: 
                'not unique' in res.json()['base'][0]
                print(f"⚠ Attribute '{attr_column}' already exists in Parent Segment and thus skip adding an attribue.", file=sys.stderr) 
                return
            except:
                print(f"failed to PUT /audiences/{audience_id}: {new_attr}")
                raise RuntimeError(f"{res.status_code} error on PUT /audiences/{audience_id}: {res.json()}")

        if rerun_master_segment:
            res = self.cdp_api.post(f"/audiences/{audience_id}/run")
            if res.ok:
                print(f"ⓘ Successfully triggered rerun of Master Segment: {audience_id}", file=sys.stderr) 
            else:
                raise RuntimeError(f"{res.status_code} error on POST /audiences/{audience_id}/run: {res.json()}")


    def get_parent_segment_id(self, name: str) -> str:
        '''
            Retrive parent segment ID if exists. Otherwise, return None
        '''

        assert name is not None

        # Get all the audience configurations 
        res = self.cdp_api.get('/audiences')
        if not res.ok:
            raise RuntimeError(res.text)
        audiences = json.loads(res.text)

        for audience in audiences:
            if 'name' in audience and name == audience['name']:
                if 'id' in audience:
                    return audience['id']

        raise ValueError(f"Cannot find parent segment: {name}")


def parse_arguments(kwargs: dict) -> dict:
    assert os.environ.get('TD_API_KEY') is not None, "TD_API_KEY ENV variable is required"
    assert os.environ.get('TD_API_SERVER') is not None, "TD_API_SERVER ENV variable is required"

    ret = {}

    audience = kwargs.pop('audience', None)
    assert audience is not None, "audience argument is required"
    audience_id = audience.pop('id', None)
    if audience_id is not None: ret['audience_id'] = audience_id
    audience_name = audience.pop('name', None)
    if audience_name is not None: ret['audience_name'] = audience_name
    foreign_key = audience.pop('foreign_key', None)
    assert foreign_key is not None, "foreign_key argument is required"
    ret['foreign_key'] = foreign_key
    ret['rerun_master_segment'] = to_boolean(audience.pop('rerun', 'False'))

    attribute = kwargs.pop('attribute', None)
    assert attribute is not None, "attribute argument is required"
    attr_table = attribute.pop('table', None)
    assert attr_table is not None, "attr_table argument is required"
    ret['attr_table'] = attr_table
    attr_column =  attribute.pop('attr_column', None)
    assert attr_column is not None, "attr_column argument is required"
    ret['attr_column'] = attr_column
    join_key =  attribute.pop('join_key', None)
    assert join_key is not None, "join_key argument is required"
    ret['join_key'] = join_key
    attr_db = attribute.pop('database', None)
    if attr_db is not None: ret['attr_db'] = attr_db
    attr_alias = attribute.pop('attr_alias', None)
    if attr_alias is not None: ret['attr_alias'] = attr_alias
    attr_group = attribute.pop('attr_group', "AutoML")
    ret['attr_group'] = attr_group
    replace_attr_if_exists = to_boolean(attribute.pop('replace_if_exists', 'False'))
    ret['replace_attr_if_exists'] = replace_attr_if_exists

    return ret


def add_attribute(**kwargs):
    import faulthandler
    faulthandler.enable()

    try:
        params = parse_arguments(kwargs)
        cdp = CdpAudience()
        cdp.add_attribute(**params)
    finally:
        # force flush
        sys.stdout.flush()
        sys.stderr.flush()
