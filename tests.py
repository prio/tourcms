from __future__ import print_function
import unittest
import os
import sys
from tourcms import Connection


if os.getenv('TOURCMS_PRIVATE_KEY', None) is None:
    print("You must set the 'TOURCMS_PRIVATE_KEY' environment variable to run tests", file=sys.stderr)
    sys.exit(1)

if os.getenv('TOURCMS_CHANNEL_KEY', None) is None:
    print("You need to set 'TOURCMS_CHANNEL_KEY' to run tests", file=sys.stderr)
    sys.exit(1)


class TestConnection(unittest.TestCase):
    def setUp(self):
        self.conn = Connection(0, os.getenv('TOURCMS_PRIVATE_KEY'))

    def test_generate_signature(self):
        verb = 'GET'
        channel = 1234
        outbound_time = 325234534
        test_strings = {
            ('/index.xml', verb, channel, outbound_time): 'Y9Q4RxaAzC6pRHJq9etfj3219Y440V3kU9tIAnymsQY%3D',
            ('/foo.xml', verb, channel, outbound_time): 'c5FX7dLAMLZCj2NvuU4Q166T77jbYuBkh9%2Fta%2Bm%2FaIY%3D',
            ('/bar.xml', 'POST', channel, outbound_time): 'xMXPzacqAdYyY%2BDBxVA8c9Gd%2Bkpb18bjmBcmMkfwWDs%3D',
            ('/foo-bar/index.xml', verb, channel, outbound_time): 'pVP5MLjLcPltHPpt7klBon8ggb5Iwj7gRbUQor1Odj0%3D',
        }
        for args, output in test_strings.items():
            signed_str = self.conn._generate_signature(*args)
            self.assertEqual(
                signed_str, output, 
                "Failed for '{}'. '{}' != '{}'".format(args[0], signed_str, output)
            )

    def test_i_can_authenticate(self):
        try:
            resp = self.conn.api_rate_limit_status(os.getenv('TOURCMS_CHANNEL_KEY'))
        except Exception, e:
            self.fail("Unable to check api rate limit: {}".format(e))
