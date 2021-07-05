import os
import twikey
import unittest


class TestTransaction(unittest.TestCase):
    _twikey = None

    ct = 1

    @unittest.skipIf("TWIKEY_API_KEY" not in os.environ, "No TWIKEY_API_KEY set")
    def setUp(self):
        key = os.environ["TWIKEY_API_KEY"]
        if "TWIKEY_API_CT" in os.environ:
            ct = os.environ["TWIKEY_API_CT"]
        baseUrl = "https://api.beta.twikey.com"
        if "TWIKEY_API_URL" in os.environ:
            baseUrl = os.environ["TWIKEY_API_URL"]
        self._twikey = twikey.TwikeyClient(key, baseUrl)

    def test_new_invite(self):
        tx = self._twikey.transaction.create(
            {
                "mndtId": "CORERECURRENTNL16318",
                "message": "Test Message",
                "ref": "Merchant Reference",
                "amount": 10.00,
                "place": "Here",
            }
        )
        self.assertIsNotNone(tx)

    def test_feed(self):
        self._twikey.document.feed(MyFeed())


class MyFeed(twikey.TransactionFeed):
    def transaction(self, transaction):
        print("new ", transaction.ref, transaction.state)


if __name__ == "__main__":
    unittest.main()
