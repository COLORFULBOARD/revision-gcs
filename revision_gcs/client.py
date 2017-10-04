# -*- coding: utf-8 -*-
"""
    revision_gcs.client
    ~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by COLORFUL BOARD Inc.
    :license: MIT, see LICENSE for more details.
"""

import datetime
import os

from google.cloud.exceptions import NotFound
from google.cloud.storage import Client as StorageClient

from revision.client import Client

__all__ = (
    "GcsClient",
)


class GcsClient(Client):

    gcs_client = None

    bucket = None

    @property
    def name(self):
        return "Google Cloud Storage"

    @property
    def client_key(self):
        return "gcs"

    def post_configure(self):
        keyfile_path = os.path.normpath(os.path.join(
            os.getcwd(),
            self.config.options.key_file
        ))

        try:
            self.gcs_client = StorageClient.\
                from_service_account_json(keyfile_path)
        except ValueError as e:
            raise RuntimeError(e.message)

        try:
            self.bucket = self.gcs_client.bucket(
                self.config.options.bucket_name
            )
        except NotFound as e:
            raise RuntimeError(e.message)

    def download(self):
        blob = self.bucket.blob(self.filename)

        if not blob.exists():
            raise RuntimeError("")

        #: download

        self.transfer.download(
            blob.public_url,
            self.tmp_file_path
        )

        #: unzip

        self.archiver.unarchive()

    def upload(self):
        blob = self.bucket.blob(self.filename)

        if not blob.exists():
            self._upload_tmp_zip(blob)

        #: zip

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
