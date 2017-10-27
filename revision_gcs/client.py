# -*- coding: utf-8 -*-
"""
    revision_gcs.client
    ~~~~~~~~~~~~~~~~~~~

    Implements Google Cloud Storage support for Revision.

    :copyright: (c) 2017 by COLORFUL BOARD Inc.
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

        bucket_name = ""

        if "/" in self.config.options.bucket_name:
            bucket_name_items = self.config.options.bucket_name.split("/")
            bucket_name = bucket_name_items[0]

            self.prefix = "/".join(bucket_name_items[1:])
            self.prefix = os.path.normpath(
                os.path.join(self.prefix, self.filename)
            )
        else:
            bucket_name = self.config.options.bucket_name

        try:
            self.bucket = self.gcs_client.bucket(bucket_name)
        except NotFound as e:
            raise RuntimeError(e.message)

    def download(self):
        blob = self.bucket.blob(self.prefix + self.blob_path)

        if not blob.exists():
            raise RuntimeError("The file to be downloaded does not exist.")

        #: download

        self.transfer.download(
            blob.public_url,
            self.tmp_file_path
        )

        #: unzip

        self.archiver.unarchive()

    def upload(self):
        blob = self.bucket.blob(self.prefix + self.blob_path)

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

        blob.make_public()

    def _upload_tmp_zip(self, blob):
        """
        :param blob:
        :type blob: :class:`google.cloud.storage.blob.Blob`
        """
        blob.upload_from_string("", "application/zip")
        blob.make_public()
