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
    def newDocument(self, doc, evt_time):
        print("Document created   ", doc["MndtId"], "@", evt_time)

    def updatedDocument(self, original_number, doc, reason, evt_time):
        print(
            "Document updated   ", original_number, "b/c", reason["Rsn"], "@", evt_time
        )

    def cancelDocument(self, number, reason, evt_time):
        print("Document cancelled ", number, "b/c", reason["Rsn"], "@", evt_time)


if __name__ == "__main__":
    unittest.main()
