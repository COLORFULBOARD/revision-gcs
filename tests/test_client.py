# -*- coding: utf-8 -*-

from revision.config import Config
from revision_gcs import GcsClient


def test_client_name():
    client = GcsClient()
    assert client.name == "Google Cloud Storage"

def test_client_key():
    client = GcsClient()
    assert client.client_key == "gcs"

def test_config():
    client = GcsClient()
    assert client.config is None

    client = GcsClient(Config({
        "key": "test_key",
        "module": "revision_gcs.GcsClient",
        "dir_path": "data",
        "revision_file": "CHANGELOG.md",
        "options": {
            "key_file": "tests/gcs_key_file.json",
            "bucket_name": "YOUR_BUCKET_NAME"
        }
    }))
    assert client.config is not None
    assert client.config.key is "test_key"
    assert client.config.module is "revision_gcs.GcsClient"
    assert client.config.dir_path is "data"
    assert client.config.revision_file is "CHANGELOG.md"
