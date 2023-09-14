import os
import twikey
import unittest


class TestTransaction(unittest.TestCase):
    _twikey = None

    ct = 1

    @unittest.skipIf("TWIKEY_API_KEY" not in os.environ, "No TWIKEY_API_KEY set")
    def setUp(self):
        key = os.environ["TWIKEY_API_KEY"]
        base_url = "https://test.beta.twikey.com/api/creditor"
        if "CT" in os.environ:
            self.ct = os.environ["CT"]
        if "TWIKEY_API_URL" in os.environ:
            base_url = os.environ["TWIKEY_API_URL"]
        self._twikey = twikey.TwikeyClient(key, base_url)

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
        self._twikey.transaction.batch_send(self.ct)
        try:
            self._twikey.transaction.batch_import("")
        except twikey.TwikeyError as e:
            self.assertEqual("invalid_file", e.get_code())
        try:
            self._twikey.transaction.reporting_import("")
        except twikey.TwikeyError as e:
            self.assertEqual("invalid_file", e.get_code())

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
