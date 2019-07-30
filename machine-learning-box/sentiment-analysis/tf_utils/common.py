import os

EXPORT_DIR_BASE = 'tfmodels'


def get_export_dir():
    models = [int(i) for i in os.listdir(EXPORT_DIR_BASE)]
    if not models:
        raise ValueError('no models found')

    export_dir = os.path.join(EXPORT_DIR_BASE, str(max(models)))
    print('Latest export dir {}'.format(export_dir))
    return export_dir
