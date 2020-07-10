import os
import sys
import requests
from logging import INFO, StreamHandler, getLogger
import digdag

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False


def generate(
    yahoo_api_url,
    tag_definition_guid,
    vendor_guid,
    entity_id,
    uid_key,
    brand_guid,
    tag_fields,
):

    post_data = {
        "tagDefinitionGuid": tag_definition_guid,
        "vendorGuid": vendor_guid,
        "entityId": entity_id,
        "uidKey": uid_key,
        "brandGuid": brand_guid,
        "tagFields": tag_fields,
    }

    headers = {"x-api-key": os.getenv("x_api_key")}
    response = requests.post(yahoo_api_url, json=post_data, headers=headers)

    if response.status_code != 201:
        logger.error(
            f"Failed to call Yahoo API with http status code {response.status_code}"
        )
        sys.exit(os.EX_DATAERR)

    r_json = response.json()

    if r_json["status"] != "CREATED":
        logger.error(f'Yahoo API respond with status {r_json["status"]}')
        sys.exit(os.EX_DATAERR)

    logger.info(f'preSignedS3Url = {r_json["preSignedS3Url"]}')
    logger.info(f'guid = {r_json["guid"]}')
    digdag.env.store(
        {"presigned_url": r_json["preSignedS3Url"], "guid": r_json["guid"]}
    )
