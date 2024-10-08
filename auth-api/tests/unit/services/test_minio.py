# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the Minio service.

Test suite to ensure that the Minio service routines are working as expected.
"""

import os

import requests

from auth_api.services import MinioService


def test_create_signed_put_url(session):  # pylint:disable=unused-argument
    """Assert that the a PUT url can be pre-signed."""
    file_name = "affidavit-test.pdf"
    signed_url = MinioService.create_signed_put_url(file_name, prefix_key="Test")
    assert signed_url
    assert signed_url.get("key").startswith("Test/")
    assert signed_url.get("key").endswith(".pdf")


def test_create_signed_get_url(session, tmpdir):  # pylint:disable=unused-argument
    """Assert that a GET url can be pre-signed."""
    d = tmpdir.mkdir("subdir")
    fh = d.join("test-file.txt")
    fh.write("Test File")
    filename = os.path.join(fh.dirname, fh.basename)

    test_file = open(filename, "rb")
    files = {"upload_file": test_file}
    file_name = fh.basename
    signed_url = MinioService.create_signed_put_url(file_name, prefix_key="Test")
    key = signed_url.get("key")
    pre_signed_put = signed_url.get("preSignedUrl")
    requests.put(pre_signed_put, files=files)

    pre_signed_get = MinioService.create_signed_get_url(key)
    assert pre_signed_get
    get_response = requests.get(pre_signed_get)
    assert get_response
