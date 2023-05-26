__all__ = ['CdpAudience']

import sys, os
import requests
import json
import pytd
import re
import faulthandler
import warnings

from typing import List, Tuple

from requests.models import Response
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests import Session


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    import functools

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func

class ApiRequestError(Exception):
    def __init__(self, response: requests.Response, msg: str=None):
        if msg is None:
            msg = f"{response.status_code} ERROR\n{response.text}"
        super().__init__(msg)

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

@deprecated
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

    def create_master_segment(self, *, name: str, database: str, table: str, description: str=None, run:bool=False):
        payload = {}
        payload['name'] = name
        payload['description'] = "" if description is None else description
        payload['master'] = {}
        payload['master']['parentDatabaseName'] = database
        payload['master']['parentTableName'] = table

        res = self.cdp_api.post('/audiences', data=json.dumps(payload))
        if not res.ok:
            raise ApiRequestError(res)

        audience = json.loads(res.text)
        audience_id = audience['id']
        print(f"ⓘ Successfully created Master Segment '{name}':  {audience_id}", file=sys.stderr)

        if run:
            res = self.cdp_api.post(f"/audiences/{audience_id}/run")
            print(f"ⓘ Run Master Segment {name}", file=sys.stderr)

        return audience_id

    def add_attribute(
        self, *, audience_id: str=None, audience_name: str=None, attr_db: str=None, attr_table: str, attr_columns: List[str], join_key: str, foreign_key: str,
        attr_aliases: List[str]=None, attr_group: str="AutoML", rerun_master_segment: bool=True, replace_attr_if_exists: bool=False,
        **kwargs
    ):
        assert len(attr_columns) >= 1, "At least one element in attr_columns but it was empty"
        if attr_aliases is None:
            attr_aliases = attr_columns
        else:
            assert len(attr_aliases) == len(attr_columns), f"len(attr_aliases) {len(attr_aliases)} is expected to be equals to len(attr_columns) {len(attr_columns)}"

        if attr_db is None:
            attr_db, attr_table = parse_table(attr_table)

        if audience_id is None:
            assert audience_name is not None, "Either audience_id or audience_name argument is required"
            audience_id = self.get_parent_segment_id(audience_name)

        # table = self.td_api.table(attr_db, attr_table)
        # attr_type = resolve_type(table, "predicted_proba")

        res = self.cdp_api.put(f"/audiences/{audience_id}")
        if not res.ok:
            raise ApiRequestError(res)
        audience = res.json()

        attributes = audience['attributes'] if 'attributes' in audience else []
        existing_attr_names = [attr['name'] for attr in attributes]

        for i, attr_column in enumerate(attr_columns):
            attr_alias = attr_aliases[i]

            new_attr = {
                #'audienceId': audience_id,       # ID of Master Segment for this attribute
                'name': attr_alias,               # Column name to be defined on Master Segment
                #'type': attr_type,               # Type of the column
                'parentDatabaseName': attr_db,    # Database name of the attribute table
                'parentTableName': attr_table,    # Table name of the attribute table
                'parentColumn': attr_column,      # Column name of the attribute table which is imported into customer table
                'parentKey': join_key,            # Join key of the attribute table
                'foreignKey': foreign_key,        # Foreign key of the master table
                'groupingName': attr_group,       # Group name of the attribute
            }

            if attr_alias in existing_attr_names:
                if replace_attr_if_exists:
                    attributes[existing_attr_names.index(attr_alias)] = new_attr
                    print(f"⚠ Replace an attribute column '{attr_alias}' in Master Segment {audience_id}", file=sys.stderr)
                else:
                    print(f"⚠ Skip adding an attribute because the attribute column '{attr_alias}' already exists", file=sys.stderr)
            else:
                attributes.append(new_attr)

        # from IPython.core.debugger import Pdb; Pdb().set_trace()
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
                raise ApiRequestError(res, f"{res.status_code} error on PUT /audiences/{audience_id}: {res.json()}")

        if rerun_master_segment:
            res = self.cdp_api.post(f"/audiences/{audience_id}/run")
            if res.ok:
                print(f"ⓘ Successfully triggered rerun of Master Segment: {audience_id}", file=sys.stderr)
            else:
                raise ApiRequestError(res, f"{res.status_code} error on POST /audiences/{audience_id}/run: {res.json()}")


    def get_parent_segment_id(self, name: str) -> str:
        '''
            Retrive parent segment ID if exists.
        '''
        assert name is not None

        # Note: console-next (v5) uses different endpoints for listing audience
        res = self.cdp_api.get('/entities/parent_segments')
        if res.ok:
            v5_res = res.json()
            for audience in v5_res.get('data',{}):
                if audience.get('attributes',{}).get('name') == name:
                    return audience['id']

        # Fall back to v4
        res = self.cdp_api.get('/audiences')
        if not res.ok:
            raise ApiRequestError(res)

        audiences = res.json()
        for audience in audiences:
            if name == audience.get('name'):
                return audience['id']

        raise ValueError(f"Cannot find parent segment: {name}")


def add_attribute(**kwargs):
    faulthandler.enable()

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
        join_key =  attribute.pop('join_key', None)
        assert join_key is not None, "join_key argument is required"
        ret['join_key'] = join_key
        attr_db = attribute.pop('database', None)
        if attr_db is not None: ret['attr_db'] = attr_db

        attr_columns =  attribute.pop('attr_columns', None)
        if attr_columns is None:
            attr_column =  attribute.pop('attr_column', None)
            assert attr_column is not None, "Either attr_columns or attr_column is required"
            ret['attr_columns'] = [attr_column]
        else:
            ret['attr_columns'] = [s.strip() for s in attr_columns.split(',')]

        attr_aliases =  attribute.pop('attr_aliases', None)
        if attr_aliases is None:
            attr_alias =  attribute.pop('attr_alias', None)
            assert attr_alias is not None, "Either attr_aliases or attr_alias is required"
            ret['attr_aliases'] = [attr_alias]
        else:
            ret['attr_aliases'] = [s.strip() for s in attr_aliases.split(',')]

        attr_group = attribute.pop('attr_group', "AutoML")
        ret['attr_group'] = attr_group
        replace_attr_if_exists = to_boolean(attribute.pop('replace_if_exists', 'False'))
        ret['replace_attr_if_exists'] = replace_attr_if_exists

        return ret

    try:
        params = parse_arguments(kwargs)
        cdp = CdpAudience()
        cdp.add_attribute(**params)
    finally:
        # force flush
        sys.stdout.flush()
        sys.stderr.flush()


def create_master_segment(**kwargs):
    faulthandler.enable()

    def parse_arguments(kwargs: dict) -> dict:
        assert os.environ.get('TD_API_KEY') is not None, "TD_API_KEY ENV variable is required"
        assert os.environ.get('TD_API_SERVER') is not None, "TD_API_SERVER ENV variable is required"

        ret = {}

        name = kwargs.pop('name', None)
        assert name is not None, "name argument is required"
        ret['name'] = name
        description = kwargs.pop('description', None)
        if description is not None: ret['description'] = description

        master = kwargs.pop('master', None)
        assert master is not None, "audience argument is required"
        database = master.pop('database', None)
        assert database is not None, "master.database argument is required"
        ret['database'] = database
        table = master.pop('table', None)
        assert table is not None, "master.table argument is required"
        ret['table'] = table

        ret['run'] = to_boolean(kwargs.pop('run', None))
        return ret

    try:
        params = parse_arguments(kwargs)
        cdp = CdpAudience()
        audience_id = cdp.create_master_segment(**params)

        import digdag
        digdag.env.store({'audience_id': audience_id})
    finally:
        # force flush
        sys.stdout.flush()
        sys.stderr.flush()
