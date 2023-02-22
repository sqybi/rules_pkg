# Copyright 2015 The Bazel Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Testing for build_tar."""

import os
import unittest

from bazel_tools.tools.python.runfiles import runfiles
from pkg.private.tar import build_tar
from tests.tar import helper


class TarFileUnitTest(unittest.TestCase):
  """Unit testing for TarFile class."""

  def setUp(self):
    super(TarFileUnitTest, self).setUp()
    self.tempfile = os.path.join(os.environ["TEST_TMPDIR"], "test.tar")
    self.data_files = runfiles.Create()
    test_file_name = "world"
    self.directory = self.data_files.Rlocation("rules_pkg/tests/testdata/build_tar/" + test_file_name)
    # Remove the file name to get directory.
    if (self.directory.endswith(test_file_name)):
      self.directory = self.directory[:-len(test_file_name)]
    # Keep the trailing slash stripped. Add slash manually when needed.
    self.directory = self.directory.rstrip("/")

  def tearDown(self):
    super(TarFileUnitTest, self).tearDown()
    if os.path.exists(self.tempfile):
      os.remove(self.tempfile)

  def test_add_tree(self):
    with build_tar.TarFile(self.tempfile, "/", "", "", None) as tar_file_obj:
      tar_file_obj.add_tree(self.directory + "/", "/")
    helper.assertTarFileContent(self, self.tempfile, [
        {"name": "./world", "data": "Hello, world!\n".encode("utf-8")},
    ])


if __name__ == "__main__":
  unittest.main()