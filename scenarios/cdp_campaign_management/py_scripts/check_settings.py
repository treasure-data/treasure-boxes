import os
import sys
import json

def run(
        user_id,
        clicks_tables,
        conversions_tables,
        mta_settings):

    error_counter = 0

    user_ids = json.loads(user_id)
    print(user_ids)
    if len(user_ids) == 0:
        print("⚠ error: `user_id` is not set.")
        error_counter += 1
    for ps_id in user_ids:
        print(f"ⓘ {user_ids[ps_id]} is used in {ps_id} as the conversion journey identifier.")


    click_tables = json.loads(clicks_tables)
    for ps_id in click_tables:
        idx = 0

        for table_setting in click_tables[ps_id]:
            idx += 1
            for key in ('table','url_col','is_audience_table'):
                if key not in table_setting.keys():
                    print(f"⚠ error in `clicks_tables`: `{key}` is not set in the {idx}th table of ps_id={ps_id}.")
                    error_counter += 1

            if 'filter' not in table_setting.keys():
                print(f"ⓘ warning: `filter` is not set in the {idx}th click table of ps_id={ps_id}.")

            if 'is_audience_table' in table_setting.keys():
                is_audience_table = table_setting['is_audience_table']
                if type(is_audience_table) != bool:
                    print(f"⚠ error in `clicks_tables`: `is_audience_table` is not a boolean value in the {idx}th table of ps_id={ps_id}.")
                    error_counter += 1
                if not is_audience_table:
                    if 'db' not in table_setting:
                        print(f"⚠ error in `clicks_tables`: `db` is not set in the {idx}th table of ps_id={ps_id}.")
                        error_counter += 1
                    if 'time_col' not in table_setting:
                        print(f"⚠ error in `clicks_tables`: `time_col` is not set in the {idx}th table of ps_id={ps_id}.")
                        error_counter += 1

    conversions_tables = json.loads(conversions_tables)
    for ps_id in conversions_tables:
        idx = 0
        for table_setting in conversions_tables[ps_id]:
            idx += 1
            for key in ('table','val_col','cv_name','acquired_revenue_per_person','is_audience_table'):
                if key not in table_setting.keys():
                    print(f"⚠ error in `conversion_tables`: `{key}` is not set in the {idx}th table of ps_id={ps_id}.")
                    error_counter += 1

            if 'filter' not in table_setting.keys():
                print(f"ⓘ warning: `filter` is not set in the {idx}th conversion table of ps_id={ps_id}.")

            if 'is_audience_table' in table_setting.keys():
                is_audience_table = table_setting['is_audience_table']
                if type(is_audience_table) != bool:
                    print(f"⚠ error in `conversion_tables`: `is_audience_table` is not a boolean value in the {idx}th table of ps_id={ps_id}.")
                    error_counter += 1
                if not is_audience_table:
                    for key in ('db','time_col'):
                        if is_audience_table and key not in table_setting:
                            print(f"⚠ error in `conversion_tables`: `{key}` is not set in the {idx}th table of ps_id={ps_id}.")
                            error_counter += 1

    if error_counter > 0:
        print(f"⚠ ⚠ ⚠ There are {error_counter} configuration errors. ⚠ ⚠ ⚠ ")
        sys.exit(1)
