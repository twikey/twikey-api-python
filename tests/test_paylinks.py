import os
import twikey
import unittest

from model.paylink_request import PaymentLinkRequest
from model.paylink_response import Paylink

class TestPaylinks(unittest.TestCase):
    _twikey = None

    ct = 1

    @unittest.skipIf("TWIKEY_API_KEY" not in os.environ, "No TWIKEY_API_KEY set")
    def setUp(self):
        key = os.environ["TWIKEY_API_KEY"]
        base_url = "https://test.beta.twikey.com/api/creditor"
        if "TWIKEY_API_URL" in os.environ:
            base_url = os.environ["TWIKEY_API_URL"]
        self._twikey = twikey.TwikeyClient(key, base_url)

    def test_new_invite(self):
        pl = self._twikey.paylink.create(PaymentLinkRequest(
                email= "no-repy@twikey.com",
                message= "Test Message",
                ref= "Merchant Reference",
                amount= 10.00,
            )
        )
        self.assertIsNotNone(pl)
        print("New link to be paid @ " + pl.url)

    def test_feed(self):
        self._twikey.paylink.feed(MyFeed())


class MyFeed(twikey.PaylinkFeed):
    def paylink(self, paylink:Paylink):
        print(
            "Paylink update #{0} {1} Euro with new state={2}".format(
                paylink.id, paylink.amount, paylink.state
            )
        )


if __name__ == "__main__":
    unittest.main()
