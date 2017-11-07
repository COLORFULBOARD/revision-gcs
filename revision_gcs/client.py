# -*- coding: utf-8 -*-
"""
    revision_gcs.client
    ~~~~~~~~~~~~~~~~~~~

    Implements Google Cloud Storage support for Revision.

    :copyright: (c) 2017 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

import datetime
import os

from google.cloud.exceptions import NotFound
from google.cloud.storage import Client as StorageClient

from revision.client import Client

__all__ = (
    "GCSClient",
)


class GCSClient(Client):

    gcs_client = None

    bucket = None

    prefix = ""

    @property
    def name(self):
        return "Google Cloud Storage"

    @property
    def client_key(self):
        return "gcs"

    def post_configure(self):
        if os.path.isabs(self.config.options.key_file):
            keyfile_path = self.config.options.key_file
        else:
            keyfile_path = os.path.normpath(os.path.join(
                os.getcwd(),
                self.config.options.key_file
            ))

        if not os.path.exists(keyfile_path):
            raise RuntimeError("GCP key file does not exist.")

        try:
            self.gcs_client = StorageClient.\
                from_service_account_json(keyfile_path)
        except ValueError as e:
            raise RuntimeError(e.message)

        bucket = ""

        if "gs://" in self.config.remote_path:
            path_items = self.config.remote_path[5:]

            if "/" in path_items:
                bucket, prefix = path_items.split('/', 1)
            else:
                bucket, prefix = path_items, ""

            self.prefix = prefix
        else:
            bucket = self.config.options.bucket_name

        try:
            self.bucket = self.gcs_client.bucket(bucket)
        except NotFound as e:
            raise RuntimeError(e.message)

    def download(self):
        blob_path = os.path.join(self.prefix, self.filename)
        blob = self.bucket.blob(blob_path)

        if not blob.exists():
            raise RuntimeError("The file to be downloaded does not exist.")

        blob.make_public()

        #: download

        self.transfer.download(
            blob.public_url,
            self.tmp_file_path
        )

        #: unzip

        self.archiver.unarchive()

        blob.acl.all().revoke_read()
        blob.acl.save(client=self.gcs_client)

    def upload(self):
        blob_path = os.path.join(self.prefix, self.filename)
        blob = self.bucket.blob(blob_path)

        if not blob.exists():
            self._upload_tmp_zip(blob)

        #: zip

        self.archiver.zip_path = self.tmp_file_path
        self.archiver.archive()

        #: upload

        signed_url = blob.generate_signed_url(
            datetime.timedelta(minutes=10),
            method="PUT"
        )

        self.transfer.upload(
            signed_url,
            method="PUT",
            file_path=self.tmp_file_path
        )

    def _upload_tmp_zip(self, blob):
        """
        :param blob:
        :type blob: :class:`google.cloud.storage.blob.Blob`
        """
        blob.upload_from_string("", "application/zip")
        blob.make_public()
