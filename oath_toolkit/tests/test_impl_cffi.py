# -*- coding: utf-8 -*-
#
# Copyright 2013, 2014 Mark Lee
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

from ..impl_cffi import OATH
from . import unittest
import time

DEFAULT_TIME_STEP_SIZE = 30
DIGITS = 6
WINDOW = 2


class CFFITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.oath = OATH()

    def setUp(self):
        self.secret = b'CFFITestCase secret'

    def test_totp(self):
        now = time.time()
        time_step_size = None
        time_offset = 0
        otp = self.oath.totp_generate(self.secret, now, time_step_size,
                                      time_offset, DIGITS)
        otp2 = self.oath.totp_generate(self.secret, now, time_step_size,
                                       time_offset, DIGITS)
        self.assertEqual(otp, otp2)
        otp3 = self.oath.totp_generate(self.secret, now, time_step_size,
                                       time_offset + DEFAULT_TIME_STEP_SIZE,
                                       DIGITS)
        self.assertNotEqual(otp, otp3)
        result = self.oath.totp_validate(self.secret, now, time_step_size,
                                         time_offset, WINDOW, otp)
        self.assertTrue(result)

    def test_hotp(self):
        moving_factor = 12
        otp = self.oath.hotp_generate(self.secret, moving_factor, DIGITS)
        otp2 = self.oath.hotp_generate(self.secret, moving_factor, DIGITS)
        self.assertEqual(otp, otp2)
        otp3 = self.oath.hotp_generate(self.secret, moving_factor + 1, DIGITS)
        self.assertNotEqual(otp, otp3)
        result = self.oath.hotp_validate(self.secret, moving_factor,
                                         WINDOW, otp)
        self.assertTrue(result)

    def test_hotp_fail(self):
        moving_factor = 12
        otp = self.oath.hotp_generate(self.secret, moving_factor + 1, DIGITS)
        with self.assertRaises(RuntimeError):  # outside of window
            self.oath.hotp_validate(self.secret, moving_factor, 0, otp)

    def test_totp_fail(self):
        now = time.time()
        otp = self.oath.totp_generate(self.secret, now, 30, 0, DIGITS)
        with self.assertRaises(RuntimeError):  # outside of window
            self.oath.totp_validate(self.secret, now + 60, None, 30, 0, otp)

    def test_library_version(self):
        version = self.oath.library_version
        self.assertIsNotNone(version)
        self.assertNotEqual(self.oath._ffi.NULL, version)

    def test_check_library_version(self):
        self.assertTrue(self.oath.check_library_version('0'))
        self.assertFalse(self.oath.check_library_version('999'))

    def test_base32_decode(self):
        # From oath-toolkit, liboath/tests/tst_coding.c
        with self.assertRaises((RuntimeError, TypeError)):
            self.oath.base32_decode(None)
        with self.assertRaises((RuntimeError, TypeError)):
            self.oath.base32_decode('')
        with self.assertRaises((RuntimeError, TypeError)):
            self.oath.base32_decode('NIXnix')
        self.assertEqual(b'foo', self.oath.base32_decode(b'MZXW6==='))
        self.assertEqual(b'foo', self.oath.base32_decode(b'MZ XW 6'))
        self.assertEqual(b'foo', self.oath.base32_decode(b'MZ XW 6==='))
        dropbox = b'gr6d 5br7 25s6 vnck v4vl hlao re'
        self.assertEqual(16, len(self.oath.base32_decode(dropbox)))

    def test_base32_encode(self):
        # From oath-toolkit, liboath/tests/tst_coding.c
        self.assertEqual(b'', self.oath.base32_encode(None))
        self.assertEqual(b'', self.oath.base32_encode(''))
        self.assertEqual(b'MZXW6===', self.oath.base32_encode('foo'))
        base32_encoded = self.oath.base32_encode('foo',
                                                 human_readable=True)
        self.assertEqual(b'MZXW 6', base32_encoded)