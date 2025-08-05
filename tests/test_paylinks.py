import os
import twikey
import unittest

from twikey.model.paylink_request import PaymentLinkRequest, PaymentLinkStatusRequest, PaymentLinkRefundRequest
from twikey.model.paylink_response import Paylink

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
        pl = self._twikey.paylink.create(
            PaymentLinkRequest(
                email= "no-repy@twikey.com",
                title= "Test Message",
                ref= "Merchant Reference",
                amount= 10.00,
            )
        )
        self.assertIsNotNone(pl)
        print("New link to be paid @ " + pl.url)

    def test_status(self):
        pl = self._twikey.paylink.status_details(
            PaymentLinkStatusRequest(id="644722")
        )
        self.assertIsNotNone(pl)

    @unittest.skipIf("PAID_PAYLINK_ID" not in os.environ, "No PAID_PAYLINK_ID set")
    def test_refund(self):
        refund = self._twikey.paylink.refund(
            PaymentLinkRefundRequest(
                id=os.environ["PAID_PAYLINK_ID"],
                message="hello",
                iban="BE51561419613262",
                bic="GKCCBEBB",
            )
        )
        self.assertIsNotNone(refund.id)
        self.assertIsNotNone(refund.amount)
        self.assertIsNotNone(refund.msg)
        print(refund)

    def test_remove(self):
        pl = self._twikey.paylink.create(
            PaymentLinkRequest(
                email="no-reply@twikey.com",
                title="Test Message",
                amount=10.00,
            )
        )
        self.assertIsNotNone(pl.id)
        self._twikey.paylink.remove(link_id=pl.id)

    def test_feed(self):
        self._twikey.paylink.feed(MyFeed())


class MyFeed(twikey.PaylinkFeed):
    def paylink(self, paylink:Paylink):
        print(f"Paylink update #{paylink.id} {paylink.amount} Euro with new state={paylink.state}")


if __name__ == "__main__":
    unittest.main()
