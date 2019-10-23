import os
import sys
os.system(f"{sys.executable} -m pip install mbed-cloud-sdk")


def _cast(value):
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            value = str(value)
    return value


def pull_resource_values(device_id, database, table):
    import pytd
    import pandas as pd
    from mbed_cloud import ConnectAPI
    from prestodb.exceptions import PrestoUserError

    # see PDM Python client ConnectAPI examples:
    # https://www.pelion.com/docs/device-management/current/mbed-cloud-sdk-python/subscriptions.html
    # https://github.com/ARMmbed/mbed-cloud-sdk-python/blob/c2bc539856cc6932e367ed47f7c2e64ef6e3a77a/examples/connect/notifications.py#L25-L45
    api = ConnectAPI({
        'api_key': os.environ.get('PDM_API_KEY'),
        'host': os.environ.get('PDM_HOST')
    })

    # check device existence
    try:
        filters = {'id': {'$eq': device_id}}
        api.list_connected_devices(filters=filters).data
    except Exception:
        raise ValueError('cannot find the device: {}'.format(device_id))

    column_names, row = [], []
    for r in api.list_resources(device_id):
        # observable resources whose values can change over time:
        # https://www.pelion.com/docs/device-management/current/connecting/collecting-resources.html
        if r.type is None or not r.observable:
            continue

        try:
            value = api.get_resource_value(device_id, r.path)
        except Exception as e:
            print('skipped resource path {} due to {}'.format(r.path, e))
            continue
        value = _cast(value)
        row.append(value)

        column_names.append(r.type)

        print('path: {}, type: {}, value: {}'.format(r.path, r.type, value))

    if len(row) == 0:
        sys.exit("no resource values from device: {}".format(device_id))

    client = pytd.Client(apikey=os.environ.get('TD_API_KEY'),
                         endpoint=os.environ.get('TD_API_SERVER'),
                         database=database)
    df = pd.DataFrame(**{'columns': column_names, 'data': [row]})

    try:
        client.load_table_from_dataframe(df, table, writer='insert_into',
                                         if_exists='append')
    except PrestoUserError:
        raise RuntimeError("inserted record does not match to current schema "
                           "of table `{}`. Make sure a list of available "
                           "resources is same as previous execution, or "
                           "change `writer` to `spark` or `bulk_import` to "
                           "take advantage of schemaless record insertion."
                           "".format(table))
