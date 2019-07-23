import sys

os.system(f"{sys.executable} -m pip install -U pytd")

import pytd.pandas_td as td
import requests
import json
import pandas as pd
import urllib.parse
from pandas.io.json import json_normalize
import re
import itertools


##############################
# カラム名変換(kintone -> TD)
## 大文字を__upper_x__に
## '$' -> __dollar__
## '.' -> __dot__
## マルチバイトをurl encode
def column_encode(s):
    s = "".join(["__upper_{}__".format(c.lower()) if c.isupper() else c for c in s])
    s = s.replace("$", "__dollar__").replace(".", "__dot__")
    return urllib.parse.quote(s)


##############################

##############################
# カラム名変換(TD -> kintone)
## __upper_x__を大文字に
## __dollar__ -> '$'
## __dot__ -> '.'
## マルチバイトをdecode
def column_decode(s):
    m = re.findall("__upper_.__", s)
    for a in range(len(m)):
        s = re.sub(m[a], m[a][8].upper(), s)
    # フィールドコードに％は含まれないとする
    column_type = ".".join(
        [s.split("_dot_")[a] for a in range(1, len(s.split("_dot_")))]
    )
    t = (
        urllib.parse.unquote(
            "%"
            + (
                s.split("_dot_")[0]
                .replace("__dot__", ".")
                .replace("__dollar__", "$")
                .replace("_", "%")
            )
        ).replace("%", "")
        + "."
        + column_type.replace("_", "")
    )
    return t


##############################

##############################
# KintoneからGET recordsしてTDに格納
def get_records(api, basic, org, app_id, database, table, fields, query, id_field_code):
    # APIリスト読み込み
    api_list = eval(api)
    # TDへのコネクションを作成
    con = td.connect()
    # アプリ番号でループ
    for a in api_list:
        # app_idでアプリを指定
        if a["id"] == app_id:
            # kintone APIの設定
            url = f"https://{org}.cybozu.com/k/v1/records.json"
            headers = {"X-Cybozu-API-Token": a["key"], "Authorization": basic}
            payload = {"app": 1, "query": query, "fields": fields, "totalCount": "true"}
            r = requests.get(url, headers=headers, params=payload)
            count = int(json.loads(r.text)["totalCount"])
            print(count)
            # GETしたデータをキャッシュするdf
            for i in itertools.islice(range(0, count), 0, None, 100):
                splited_query = (
                    query
                    + " order by "
                    + id_field_code
                    + " asc limit 100 offset "
                    + f"{i}"
                )
                print(splited_query)
                payload = {"app": 1, "query": splited_query, "fields": fields}
                r = requests.get(url, headers=headers, params=payload)
                if r.status_code != 200:
                    sys.exit(1)
                else:
                    data = json.loads(r.text)
                    df = pd.DataFrame.from_dict(data)
                    df = json_normalize(df["records"])
                    df = df.rename(columns=column_encode)
                # KintoneからGETしたアプリID = X のrecordsをTDのTableに格納
                td.to_td(
                    df,
                    ".".join([database, table]),
                    con,
                    if_exists="append",
                    index=False,
                )


##############################


##############################
# KintoneをDELETE records
def delete_records(api, basic, org, app_id, ids, content_type):
    # APIリスト読み込み
    api_list = eval(api)
    for a in api_list:
        # app_idでアプリを指定
        if a["id"] == app_id:
            url = f"https://{org}.cybozu.com/k/v1/records.json"
            headers = {
                "X-Cybozu-API-Token": a["key"],
                "Authorization": basic,
                "Content-Type": content_type,
            }
            ids_str = str(ids)
            payload = '{"app":' + f"{app_id}" + ',"ids":' + ids_str + "}"
            r = requests.delete(url, data=payload, headers=headers)
            if r.status_code != 200:
                sys.exit(1)


##############################

##############################
# TDからrecordsを取得しKintoneにPUT
def put_records(api, basic, org, app_id, c, content_type, database, query):
    # APIリスト読み込み
    api_list = eval(api)
    for a in api_list:
        # app_idでアプリを指定
        if a["id"] == app_id:
            # クエリエンジン起動
            engine = td.create_engine(f"presto:{database}")
            c = eval(c)
            c = [d["name"] for d in c]
            # TDのデータを取得
            df = td.read_td(query, engine)
            df = df.rename(columns=column_decode)
            df = df[
                [s for s in list(df.columns) if re.match(".*?(value)\Z", s)]
            ].rename(columns=lambda s: s.replace(".value", ""))
            df = df[c]
            l_records = df.to_dict(orient="records")
            bucket = 100
            splited_records = [
                l_records[idx : idx + bucket]
                for idx in range(0, len(l_records), bucket)
            ]
            id_column = c.pop(0)
            for r in splited_records:
                payload = ""
                for s in r:
                    r_id = '{"id": ' + f"{s[id_column]}" + ', "record": {'
                    kv = "".join(
                        [
                            '"' + f"{k}" + '": {"value": "' + f"{s[k]}" + '"},'
                            if k in c
                            else ""
                            for k in s
                        ]
                    )
                    record = r_id + kv[:-1] + "}},"
                    payload = payload + record
                payload = '{"app":' + f"{app_id}" + ',"records":[' + payload[:-1] + "]}"
                data = json.loads(payload)
                url = f"https://{org}.cybozu.com/k/v1/records.json"
                headers = {
                    "X-Cybozu-API-Token": a["key"],
                    "Authorization": basic,
                    "Content-Type": content_type,
                }
                r = requests.put(url, data=payload.encode("utf-8"), headers=headers)
                if r.status_code != 200:
                    sys.exit(1)
        else:
            break


##############################

##############################
# TDからrecordsを取得しKintoneにPOST
def post_records(api, basic, org, app_id, c, content_type, database, query):
    # APIリスト読み込み
    api_list = eval(api)
    for a in api_list:
        # app_idでアプリを指定
        if a["id"] == app_id:
            # クエリエンジン起動
            engine = td.create_engine(f"presto:{database}")
            c = eval(c)
            c = [d["name"] for d in c]
            # TDのデータを取得
            df = td.read_td(query, engine)
            df = df.rename(columns=column_decode)
            df = df[
                [s for s in list(df.columns) if re.match(".*?(value)\Z", s)]
            ].rename(columns=lambda s: s.replace(".value", ""))
            df = df[c]
            l_records = df.to_dict(orient="records")
            bucket = 100
            splited_records = [
                l_records[idx : idx + bucket]
                for idx in range(0, len(l_records), bucket)
            ]
            for r in splited_records:
                payload = ""
                for s in r:
                    kv = "".join(
                        [
                            '"' + f"{k}" + '": {"value": "' + f"{s[k]}" + '"},'
                            if k in c
                            else ""
                            for k in s
                        ]
                    )
                    record = "{" + kv[:-1] + "},"
                    payload = payload + record
                payload = '{"app":' + f"{app_id}" + ',"records":[' + payload[:-1] + "]}"
                data = json.loads(payload)
                url = f"https://{org}.cybozu.com/k/v1/records.json"
                headers = {
                    "X-Cybozu-API-Token": a["key"],
                    "Authorization": basic,
                    "Content-Type": content_type,
                }
                r = requests.post(url, data=payload.encode("utf-8"), headers=headers)
                if r.status_code != 200:
                    sys.exit(1)
        else:
            break


##############################
