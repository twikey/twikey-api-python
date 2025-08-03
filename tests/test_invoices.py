import os
import twikey
import unittest
import time
import uuid
from datetime import date, timedelta

from model.invoice_request import Customer, InvoiceRequest
from model.invoice_response import Invoice


class TestInvoices(unittest.TestCase):
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
        invoice = self._twikey.invoice.create(
            InvoiceRequest(
                id = uuid.uuid4(),
                number = "Inv-" + str(round(time.time())),
                title = "Invoice " + date.today().strftime("%B"),
                remittance = "596843697521",
                ct = 1988,
                amount = 100,
                date = date.today(),
                duedate = (date.today() + timedelta(days=7)),
                customer = Customer(
                    customer_number = "customer123",
                    email = "no-reply@twikey.com",
                    first_name = "Twikey",
                    last_name = "Support",
                    address = "Derbystraat 43",
                    city = "Gent",
                    zip = "9000",
                    country = "BE",
                    lang = "nl",
                    mobile = "32498665995",
                )
                # "pdf": "JVBERi0xLj....RU9GCg=="
            )
        )
        self.assertIsNotNone(invoice)
        print("New invoice to be paid @ " + invoice.url)

    def test_feed(self):
        self._twikey.invoice.feed(MyFeed(), False, "meta", "include", "lastpayment")


class MyFeed(twikey.InvoiceFeed):
    def invoice(self, invoice:Invoice):
        new_state = ""
        if invoice.state == "PAID":
            lastpayment_ = invoice.payment_events
            if lastpayment_:
                new_state = "PAID via " + lastpayment_[0].method
        else:
            new_state = "now has state " + invoice.state
        print(
            "Invoice update with number {0} {1} euro {2}".format(
                invoice.number, invoice.amount, new_state
            )
        )


if __name__ == "__main__":
    unittest.main()
