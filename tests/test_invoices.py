import os
import twikey
import unittest
import time
import uuid
from datetime import date, timedelta


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
        invoice = self._twikey.invoice.create(
            {
                "id": str(uuid.uuid4()),
                "number": "Inv-" + str(round(time.time())),
                "title": "Invoice " + date.today().strftime("%B"),
                "remittance": "596843697521",
                "ct": 1988,
                "amount": 100,
                "date": date.today().isoformat(),
                "duedate": (date.today() + timedelta(days=7)).isoformat(),
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
                    "mobile": "32498665995",
                },
                # "pdf": "JVBERi0xLj....RU9GCg=="
            }
        )
        self.assertIsNotNone(invoice)
        print("New invoice to be paid @ " + invoice["url"])

    def test_feed(self):
        self._twikey.invoice.feed(MyFeed(), "meta", "include", "lastpayment")


class MyFeed(twikey.InvoiceFeed):
    def invoice(self, invoice):
        if invoice["state"] == "PAID":
            newState = "PAID via " + invoice["lastpayment"]["method"]
        else:
            newState = "now has state " + invoice["state"]
        print(
            "Invoice update with number {0} {1} euro {2}".format(
                invoice["number"], invoice["amount"], newState
            )
        )


if __name__ == "__main__":
    unittest.main()
