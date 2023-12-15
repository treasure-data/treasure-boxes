import os, sys
import json
from functools import cached_property

packages = [
    'requests==2.28.1'
]

def installed_packages():
    import pkg_resources
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
        for i in installed_packages])
    return installed_packages_list

# Install required packages
for package in packages:
    if package not in installed_packages():
        os.system(f"{sys.executable} -m pip install -U {package}")

import requests

# Load environment variables
TD_API_KEY = os.environ['TD_API_KEY']
TD_ENDPOINT = os.environ['TD_ENDPOINT']
ENDPOINT_MAP = {
    'api.treasuredata.com': 'api-cdp.treasuredata.com',
    'api.treasuredata.co.jp': 'api-cdp.treasuredata.co.jp',
    'api.ap02.treasuredata.com': 'api-cdp.ap02.treasuredata.co.jp',
    'api.ap03.treasuredata.com': 'api-cdp.ap03.treasuredata.co.jp',
    'api.eu01.treasuredata.com': 'api-cdp.eu01.treasuredata.com'
}
CDP_ENDPOINT = ENDPOINT_MAP[TD_ENDPOINT]
headers = {'Authorization': f'TD1 {TD_API_KEY}'}


class Segment:
    def __init__(self, id_):
        self.id = id_

    @cached_property
    def info(self) -> dict:
        url = f'https://{CDP_ENDPOINT}/entities/segments/{self.id}'
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        return json.loads(res.text)

    @property
    def name(self) -> None:
        return self.info['data']['attributes']['name']

    def get_activations(self):
        url = f'https://{CDP_ENDPOINT}/entities/segments/{self.id}/syndications'
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        activations = [Activation(property_) for property_ in json.loads(res.text)['data']]
        return activations


    def _extract_conditions_with_typeof(self, rule: dict) -> list:
    # def _extract_conditions_with_typeof(self, rule: dict, types: list) -> list:
        conditions = []

        def extract_conditions(dict_: dict, source=None):
            for k, v in dict_.items():
                if k == 'leftValue' and v.get('source', {}).get('name'):
                    source = v['source']['name']
                if isinstance(v, list):
                    for _v in v:
                        if k == 'conditions':
                            conditions.append([_v, source])
                        if isinstance(_v, dict):
                            extract_conditions(_v, source=source)
                if isinstance(v, dict):
                    extract_conditions(v, source=source)
        extract_conditions(rule)
        return conditions


    def extract_columns_in_rule(self) -> list:
        '''
            Extract column list used in a specified segment
        '''

        customers_table = 'customers'

        # Get condition list of specified segment
        rule = self.info['data']['attributes']['rule']

        ## The case that its condition is not specified
        if not rule:
            return []
        conditions = self._extract_conditions_with_typeof(rule)
        # conditions = self._extract_conditions_with_typeof(rule, ['Value', 'Column'])

        # Extract columns
        columns = []
        for condition, table in conditions:
            # print(self.id, condition)
            # Attribute Table
            if condition['type'] == 'Value' and \
                   'filter' not in condition.get('leftValue').keys():
                
                column_ = condition['leftValue']['name']
                column = f"{customers_table}.{column_}"
                if column not in columns:
                    columns.append(column)


            # Behavior Table
            elif condition['type'] == 'Column':
                column_ = condition['column']
                column = f"{table}.{column_}"
                if column not in columns:
                    columns.append(column)
        return columns


class Folder:
    def __init__(self, id_):
        self.id = id_


    # @cached_property
    # def property(self):
    #     url = f'https://{CDP_ENDPOINT}/entities/folders/{self.id}'
    #     res = requests.get(url, headers=headers)
    #     res.raise_for_status()
    #     return json.loads(res.text)
        

    @cached_property
    def entities(self, depth: int = 32) -> dict:
        url = f'https://{CDP_ENDPOINT}/entities/by-folder/{self.id}?depth={depth}'
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        return json.loads(res.text)
        

    def list_batch_segments(self) -> list:
        segments = []
        for entity in self.entities['data']:
            if entity['type'] == 'segment-batch':
                segments.append(Segment(entity['id']))
        return segments


class ParentSegment:
    def __init__(self, id_):
        self.id = id_

    @cached_property
    def info(self) -> dict:
        url = f'https://{CDP_ENDPOINT}/entities/parent_segments/{self.id}'
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        return json.loads(res.text)

    @property
    def root_folder_id(self) -> int:
        return int(self.info['data']['relationships']['parentFolder']['data']['id'])


    def get_root_folder(self) -> Folder:
        return Folder(self.root_folder_id)


    def get_activations(self) -> list:
        url = f'https://{CDP_ENDPOINT}/entities/parent_segments/{self.id}/syndications'
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        activations = [Activation(property_) for property_ in json.loads(res.text)['data']]
        return activations
       
    

class Activation:
    def __init__(self, property: dict):
        self.property = property


    @property
    def id(self) -> int:
        return int(self.property['id'])

    @property
    def name(self) -> None:
        return self.property['attributes']['name']

    @property
    def all_columns(self) -> bool:
        return self.property['attributes']['allColumns']


    @property
    def segment(self) -> None:
        return Segment(self.property['relationships']['segment']['data']['id'])


    @property
    def columns(self) -> list:
        return [column['source']['column'] 
                    for column in self.property['attributes']['columns']
                    if column.get('source', {}).get('column')    
                ]
