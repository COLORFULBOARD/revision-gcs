# -*- coding: utf-8 -*-

import os

from revision.config import Config
from revision_gcs import GCSClient


def make_gcs_config():

    key_file_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'gcs_key_file.json'
    )

    if not os.path.exists(key_file_path):
        with open(key_file_path, 'w') as f:
            f.write('{ \
"type": "service_account", \
"project_id": "%s", \
"private_key_id": "%s",\
"private_key": "%s", \
"client_email": "%s", \
"client_id": "%s", \
"auth_uri": "https://accounts.google.com/o/oauth2/auth", \
"token_uri": "https://accounts.google.com/o/oauth2/token", \
"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", \
"client_x509_cert_url": "%s"  }' % (
                os.environ.get("GCS_PROJECT_ID"),
                os.environ.get("GCS_PRIVATE_KEY_ID"),
                os.environ.get("GCS_PRIVATE_KEY"),
                os.environ.get("GCS_CLIENT_EMAIL"),
                os.environ.get("GCS_CLIENT_ID"),
                os.environ.get("GCS_CERT_URL"),
            ))


make_gcs_config()


def test_client_name():
    client = GCSClient()
    assert client.name == "Google Cloud Storage"

def test_client_key():
    client = GCSClient()
    assert client.client_key == "gcs"

def test_config():
    client = GCSClient()
    assert client.config is None

    client = GCSClient(Config({
        "key": "test_key",
        "module": "revision_gcs.GCSClient",
        "local_path": "data",
        "remote_path": "gs://YOUR_BUCKET_NAME",
        "options": {
            "key_file": "tests/gcs_key_file.json"
        }
    }))
    assert client.config is not None
    assert client.config.key is "test_key"
    assert client.config.module is "revision_gcs.GCSClient"
    assert client.config.local_path is "data"
    assert client.config.remote_path is "CHANGELOG.md"

def test_blob_path():
    client = GCSClient()
    assert client.config is None

    client = GCSClient(Config({
        "key": "test_key",
        "module": "revision_gcs.GCSClient",
        "dir_path": "data",
        "local_path": "data",
        "remote_path": "gs://YOUR_BUCKET_NAME/TO/BLOB",
        "options": {
            "key_file": "tests/gcs_key_file.json"
        }
    }))

    assert client.prefix == "TO/BLOB"


if __name__ == '__main__':
    make_gcs_config()
