import requests
import pandas as pd
import os

# utilize the pytd to load the data into TD
import pytd


td_endpoint = os.environ["TD_API_SERVER"]
td_api_key = os.environ["TD_API_KEY"]
td_database = os.environ["DATABASE"]
ot_profile_url = os.environ["OT_PROFILE_ENDPOINT"]
ot_collection_url = os.environ["OT_COLLECTION_ENDPOINT"]
ot_api_key = os.environ["OT_API_KEY"]


"""
uploads the dataframe to TD
"""


def uploadOTDataToTD(td_endpoint, td_api_key, dataframe, td_db, td_table):
    try:
        client = pytd.Client(
            apikey=td_api_key,
            endpoint=td_endpoint,
            database=td_db,
            default_engine="hive",
        )
        client.load_table_from_dataframe(dataframe, td_table, if_exists="overwrite")
    except:
        raise Exception("Error Connecting to TD database")


"""
returns dataframe per page
for profile end point
"""


def callOneTrustProfiles(ot_api_key, ot_profile_url, pagenumber):
    payload = {
        "page": pagenumber,
        "size": 50,
    }  # according to one trust 50 is max you can get from one call.
    header_payload = {"APIKey": ot_api_key}
    getresponse = requests.get(ot_profile_url, headers=header_payload, params=payload)
    try:
        api_response = getresponse.json()
        api_content = api_response["content"]  # get the content of the json response
        lst_id = []
        lst_identifier = []
        lst_name = []
        lst_status = []
        lst_status_pid = []
        lst_last_transaction_collection_id = []
        for each_response in api_content:
            for each_purpose in each_response["Purposes"]:
                lst_id.append(each_response["Id"])  # unique ID to identify a subject
                lst_identifier.append(
                    each_response["Identifier"]
                )  # subject email  example: johndoe@td.com
                lst_name.append(
                    each_purpose["Name"]
                )  # name of the purpose example: Terms and Conditions
                lst_status.append(
                    each_purpose["Status"]
                )  # whats the consent status : example  Terms and Conditions
                lst_status_pid.append(
                    each_purpose["Id"]
                )  # this is the ID which uniquely identifies the purpose, stored as pid in treasuere data
                lst_last_transaction_collection_id.append(
                    each_purpose["LastTransactionCollectionPointId"]
                )  # this identifies the last collecpoint where consent was given (Example : web form , newsletter subsciption page etc)
        df = pd.DataFrame(
            list(
                zip(
                    lst_id,
                    lst_identifier,
                    lst_name,
                    lst_status,
                    lst_status_pid,
                    lst_last_transaction_collection_id,
                )
            ),
            columns=[
                "id",
                "identifier",
                "name",
                "status",
                "pid",
                "lst_last_transaction_collection_id",
            ],
        )
        return df
    except:
        raise Exception(getresponse.status_code)


"""
returns dataframe per page
for collection end point
"""


def callOneTrustCollectionPoint(ot_api_key, ot_collection_url, pagenumber):
    payload = {"page": int(pagenumber), "size": 50}
    header_payload = {"APIKey": str(ot_api_key)}
    getresponse = requests.get(
        ot_collection_url, headers=header_payload, params=payload
    )
    try:
        api_response = getresponse.json()
        api_content = api_response["content"]
        lst_id = []
        lst_name = []
        lst_collection_point_type = []
        lst_label = []
        lst_pid = []
        lst_status = []
        lst_newversion_flag = []
        lst_version = []
        for each_response in api_content:
            for each_purpose in each_response["Purposes"]:
                lst_id.append(
                    each_response["Id"]
                )  # this id identifies the collection point
                lst_name.append(
                    each_response["Name"]
                )  # this id identifies the name of the collection point
                lst_collection_point_type.append(
                    each_response["CollectionPointType"]
                )  # indentifies the collection point type etc
                lst_label.append(
                    each_purpose["Label"]
                )  # purpose example: Terms and Conditions
                lst_pid.append(each_purpose["Id"])  # uniquely identifies the purpose
                lst_status.append(each_purpose["Status"])  # status of the purpose
                lst_version.append(each_purpose["Version"])  # version used
                lst_newversion_flag.append(
                    each_purpose["NewVersionAvailable"]
                )  # flag to check if a new version is avaliable

        df = pd.DataFrame(
            list(
                zip(
                    lst_id,
                    lst_name,
                    lst_collection_point_type,
                    lst_label,
                    lst_pid,
                    lst_status,
                    lst_version,
                    lst_newversion_flag,
                )
            ),
            columns=[
                "id",
                "name",
                "collectionPointType",
                "label",
                "pid",
                "status",
                "version",
                "new_version_flag",
            ],
        )
        return df
    except:
        raise Exception(getresponse.status_code)


"""
upload one trust collection
data into Treasure Data
"""


def getOneTrustCollectionData():

    header_payload = {"APIKey": str(ot_api_key)}
    payload = {"size": 50}
    getresponse = requests.get(
        ot_collection_url, headers=header_payload, params=payload
    )

    try:
        api_first_call = getresponse.json()
        # find the total number of pages in response
        total_pages = api_first_call["totalPages"]
        td_dataframe = pd.DataFrame()  # Empty dataframe
        for page in range(total_pages):
            df = callOneTrustCollectionPoint(ot_api_key, ot_collection_url, page)
            td_dataframe = td_dataframe.append(df)

        df_to_upload_td = td_dataframe
        uploadOTDataToTD(
            td_endpoint,
            td_api_key,
            df_to_upload_td,
            td_database,
            "onetrust_collection_data",
        )

    except:
        raise Exception(getresponse.status_code)


"""
upload onetrust profile data
into Treasure Data
"""


def getOneTrustProfileData():
    header_payload = {"APIKey": str(ot_api_key)}
    payload = {"size": 50}
    getresponse = requests.get(ot_profile_url, headers=header_payload, params=payload)
    try:
        api_first_call = getresponse.json()
        total_pages = api_first_call["totalPages"]
        td_dataframe = pd.DataFrame()  # Empty dataframe
        for page in range(total_pages):
            df = callOneTrustProfiles(ot_api_key, ot_profile_url, page)
            td_dataframe = td_dataframe.append(df)

        df_to_upload_td = td_dataframe
        uploadOTDataToTD(
            td_endpoint,
            td_api_key,
            df_to_upload_td,
            td_database,
            "onetrust_profiles_data",
        )

    except:
        raise Exception(getresponse.status_code)
