import os
import twikey
import unittest
import uuid


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

    def test_new_beneficiary(self):
        customer_number = str(uuid.uuid4())
        benef = self._twikey.refund.create_beneficiary_account(
            {
                "customerNumber": customer_number,
                "email": "info@twikey.com",
                "firstname": "Info",
                "lastname": "Twikey",
                "l": "en",
                "address": "Abby road",
                "city": "Liverpool",
                "zip": "1526",
                "country": "BE",
                "mobile": "",
                "iban": "NL46ABNA8910219718",
                "bic": "ABNANL2A",
            }
        )
        self.assertIsNotNone(benef)

        refund = self._twikey.refund.create(
            customer_number,
            {
                "iban": "NL46ABNA8910219718",
                "message": "Refund faulty item",
                "ref": "My internal reference",
                "amount": "10.99",
            },
        )
        self.assertIsNotNone(refund)

    def test_feed(self):
        self._twikey.refund.feed(MyFeed())


class MyFeed(twikey.RefundFeed):
    def refund(self, refund):
        print(
            "Refund update #{0} {1} Euro with new state={2}".format(
                refund["id"], refund["amount"], refund["state"]
            )
        )


if __name__ == "__main__":
    unittest.main()
