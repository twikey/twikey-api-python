import os
import twikey
import unittest

class TestInvoices(unittest.TestCase):
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
        invoice = self._twikey.invoice.create({
            "number": "Inv20200001",
            "title": "Invoice July",
            "remittance": "596843697521",
            "ct": 1988,
            "amount": 100,
            "date": "2020-01-31",
            "duedate": "2020-02-28",
            "customer": {
                "customerNumber": "customer123",
                "email": "no-reply@twikey.com",
                "firstname": "Twikey",
                "lastname": "Support",
                "address": "Derbystraat 43",
                "city": "Gent",
                "zip": "9000",
                "country": "BE",
                "l": "nl",
                "mobile": "32498665995"
            },
            # "pdf": "JVBERi0xLj....RU9GCg=="
        })
        self.assertIsNotNone(invoice)

    def test_feed(self):
        self._twikey.document.feed(MyFeed())


class MyFeed(twikey.TransactionFeed):

    def transaction(self, transaction):
        print("new ", transaction.ref, transaction.state)


if __name__ == '__main__':
    unittest.main()
