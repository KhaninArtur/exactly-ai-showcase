import base64
import json

from google.cloud import storage

from internal.settings import settings


def save_image_cloud(image_id: str, image_data: bytes):
    bucket = get_bucket()

    blob = bucket.blob(image_id)
    blob.upload_from_string(image_data, content_type="image/jpeg")


def get_bucket() -> storage.Bucket:
    bucket_name = settings.gs_bucket_name

    service_account = json.loads(
        base64.b64decode(settings.gcs_service_account_key_base64)
    )
    storage_client = storage.Client.from_service_account_info(service_account)
    return storage_client.get_bucket(bucket_name)
