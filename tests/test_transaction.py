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
        self._twikey.transaction.feed(MyFeed())


class MyFeed(twikey.TransactionFeed):
    def transaction(self, transaction):
        state = transaction["state"]
        final = transaction["final"]
        ref = transaction["ref"]
        if not ref:
            ref = transaction["msg"]
        _state = state
        _final = ""
        if state == "PAID":
            _state = "is now paid"
        elif state == "ERROR":
            _state = "failed due to '" + transaction["bkmsg"] + "'"
            if final:
                # final means Twikey has gone through all dunning steps, but customer still did not pay
                _final = "with no more dunning steps"
        print(
            "Transaction update",
            transaction["amount"],
            "euro with",
            ref,
            _state,
            _final,
        )


if __name__ == "__main__":
    unittest.main()
