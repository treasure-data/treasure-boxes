import os

EXPORT_DIR_BASE = 'tfmodels'


def get_export_dir():
    models = [int(i) for i in os.listdir(EXPORT_DIR_BASE)]
    if not models:
        raise ValueError('no models found')

    export_dir = '{}/{}'.format(EXPORT_DIR_BASE, max(models))
    print('Latest export dir {}'.format(export_dir))
    return export_dir
