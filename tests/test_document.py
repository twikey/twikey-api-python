import os
import twikey
import unittest


class TestDocument(unittest.TestCase):
    _twikey = None

    @unittest.skipIf("TWIKEY_API_KEY" not in os.environ, "No TWIKEY_API_KEY set")
    def setUp(self):
        key = os.environ["TWIKEY_API_KEY"]
        baseUrl = "https://api.beta.twikey.com"
        if "TWIKEY_API_URL" in os.environ:
            baseUrl = os.environ["TWIKEY_API_URL"]
        self._twikey = twikey.TwikeyClient(key, baseUrl)

    def test_new_invite(self):
        ct = 1
        if "CT" in os.environ:
            ct = os.environ["CT"]
        invite = self._twikey.document.create(
            {
                "ct": ct,
                "email": "info@twikey.com",
                "firstname": "Info",
                "lastname": "Twikey",
                "l": "en",
                "address": "Abby road",
                "city": "Liverpool",
                "zip": "1526",
                "country": "BE",
                "mobile": "",
                "iban": "",
                "bic": "",
                "mandateNumber": "",
                "contractNumber": "",
            }
        )
        self.assertIsNotNone(invite)

    def test_feed(self):
        self._twikey.document.feed(MyDocumentFeed())


class MyDocumentFeed(twikey.DocumentFeed):
    def newDocument(self, doc):
        print("new ", doc["MndtId"])

    def updatedDocument(self, doc, reason):
        print("update ", doc["MndtId"], "b/c", reason["Rsn"])

    def cancelDocument(self, docNumber, reason):
        print("cancelled ", docNumber, "b/c", reason["Rsn"])


if __name__ == "__main__":
    unittest.main()
