import os
import sys
import pandas as pd
import math
import pytd
from dateutil import parser

pd.set_option('display.max_columns', None)
headers = {'Authorization': 'TD1 %s' % os.environ['TD_API_KEY']}
MAX_UNIONS = 25

def run(
        session_unixtime,
        time_from,
        time_to,
        user_id,
        input_db,
        input_table_master_activations,
        input_table_daily_activations_info,
        cdp_audience_db,
        input_table_customers,
        input_table_clicks,
        dest_db,
        dest_table,
        query_store_table,
        api_endpoint='api.treasuredata.com'):

    client = pytd.Client(apikey=os.environ['TD_API_KEY'], endpoint='https://%s' % api_endpoint, database=dest_db)

    try:
        tables_obj = client.list_tables(cdp_audience_db)
    except Exception as e:
        print(e)
        return

    input_tables = []
    for tbl in tables_obj:
        input_tables.append(tbl.name)

    res = client.query(
        f'SELECT journey_id, syndication_id, activation_step_id, activation_name, stage_no, step_id FROM {input_db}.{input_table_master_activations} WHERE syndication_id is not NULL'
    )
    df_1 = pd.DataFrame(**res)
    print(f"Searched {len(df_1)} activations. Create {math.ceil(len(df_1)/MAX_UNIONS)} queries in the process.")

    qry_union_all = ''
    l = []
    columns_q = ['time','db_name','table_name','query']

    for idx, row in df_1.iterrows():

        journey_table = 'journey_%s' % (row['journey_id'])
        syndication_id = row['syndication_id']
        activation_step_id = row['activation_step_id']
        activation_name = row['activation_name']
        stage_no = row['stage_no']
        step_id = row['step_id']
        column_id = 'intime_stage_%s_%s' % (stage_no, step_id)
        if stage_no < 0:  # If the value is missing, -1 is included.
            continue

        if not journey_table in input_tables:
            print(f'{cdp_audience_db}.{journey_table} does not exist, so skip this task.')
            continue

        inner_qry = ' '.join([
                f"SELECT \"{column_id}\" AS session_time, t2.{user_id}, t1.cdp_customer_id, '{syndication_id}' AS syndication_id, '{activation_step_id}' AS activation_step_id, '{activation_name}' AS activation_name",
                f"FROM {cdp_audience_db}.{journey_table} t1",
                f"LEFT OUTER JOIN {cdp_audience_db}.{input_table_customers} t2",
                f"ON t1.cdp_customer_id = t2.cdp_customer_id",
                f"WHERE \"{column_id}\" IS NOT NULL",
                f"AND TD_TIME_RANGE(\"{column_id}\",{time_from},{time_to}) "
        ])

        journey_reentry_history_table = f"{journey_table}_reentry_history"
        if not journey_reentry_history_table in input_tables:
            inner_qry += ' '.join([
                    f" UNION ALL",
                    f"SELECT \"{column_id}\" AS session_time, t2.{user_id}, t1.cdp_customer_id, '{syndication_id}' AS syndication_id, '{activation_step_id}' AS activation_step_id, '{activation_name}' AS activation_name",
                    f"FROM {cdp_audience_db}.{journey_reentry_history_table} t1",
                    f"LEFT OUTER JOIN {cdp_audience_db}.{input_table_customers} t2",
                    f"ON t1.cdp_customer_id = t2.cdp_customer_id",
                    f"WHERE \"{column_id}\" IS NOT NULL",
                    f"AND TD_TIME_RANGE(\"{column_id}\",{time_from},{time_to}) "
            ])

        journey_jump_history_table = f"{journey_table}_jump_history"
        if journey_jump_history_table in input_tables:
            inner_qry += ' '.join([
                    f" UNION ALL",
                    f"SELECT \"{column_id}\" AS session_time, t2.{user_id}, t1.cdp_customer_id, '{syndication_id}' AS syndication_id, '{activation_step_id}' AS activation_step_id, '{activation_name}' AS activation_name",
                    f"FROM {cdp_audience_db}.{journey_jump_history_table} t1",
                    f"LEFT OUTER JOIN {cdp_audience_db}.{input_table_customers} t2",
                    f"ON t1.cdp_customer_id = t2.cdp_customer_id",
                    f"WHERE \"{column_id}\" IS NOT NULL",
                    f"AND TD_TIME_RANGE(\"{column_id}\",{time_from},{time_to}) "
            ])

        qry = ' '.join([
            f"SELECT",
                f"s2.time_finished AS time",
                f",s1.{user_id}",
                f",s1.activation_step_id",
                f",s1.syndication_id",
                f",'journeyActivationStep' AS activation_type",
                f",s1.activation_name",
                f",cv_name",
                f",utm_campaign",
                f",utm_medium",
                f",utm_source",
                f",utm_content",
                f",utm_connector",
                f",utm_term",
            f"FROM({inner_qry}) s1",
            f"JOIN {input_db}.{input_table_daily_activations_info} s2",
            f"ON s1.session_time <= s2.time",
            f"AND s2.time < s1.session_time + 60*60*24*1",
            f"AND s1.syndication_id = s2.syndication_id",
            f"LEFT OUTER JOIN (",
                f"SELECT",
                    f"activation_step_id",
                    f",MAX_BY(cv_name,time) AS cv_name",
                    f",MAX_BY(utm_campaign,time) AS utm_campaign",
                    f",MAX_BY(utm_medium,time) AS utm_medium",
                    f",MAX_BY(utm_source,time) AS utm_source",
                    f",MAX_BY(utm_content,time) AS utm_content",
                    f",MAX_BY(utm_connector,time) AS utm_connector",
                    f",MAX_BY(utm_term,time) AS utm_term",
                f"FROM {input_db}.{input_table_clicks}",
                f"GROUP BY 1",
            f") s3",
            f"ON s1.activation_step_id = s3.activation_step_id",
        ])

        if qry_union_all == '':
            qry_union_all = qry
        else:
            qry_union_all = ' '.join([qry_union_all, ' UNION ALL ', qry])

        if (idx+1)%MAX_UNIONS == 0:
            print(qry_union_all)
            l.append([int(session_unixtime), dest_db, dest_table, qry_union_all])
            qry_union_all = ''

    if qry_union_all != '':
        print(qry_union_all)
        l.append([int(session_unixtime), dest_db, dest_table, qry_union_all])

    df_query_store = pd.DataFrame(data=l, columns=columns_q)
    print(df_query_store)
    if len(df_query_store)>0:
        # Don't use writer='insert_into' because it changes '' to "".
        client.load_table_from_dataframe(df_query_store, f"{dest_db}.{query_store_table}", writer='bulk_import', if_exists='overwrite', fmt='msgpack')
