import os
import twikey
import unittest
import time
import uuid
from datetime import date, timedelta

from twikey.model.invoice_request import Customer, InvoiceRequest, LineItem, UpdateInvoiceRequest, DetailsRequest, \
    ActionRequest, ActionType, UblUploadRequest, BulkInvoiceRequest
from twikey.model.invoice_response import Invoice

class TestInvoices(unittest.TestCase):
    _twikey = None

    def setUp(self):
        key = os.environ["TWIKEY_API_KEY"]
        if key is None:
            self.skipTest("No TWIKEY_API_KEY set")

        base_url = "https://test.beta.twikey.com/api/creditor"
        if "TWIKEY_API_URL" in os.environ:
            base_url = os.environ["TWIKEY_API_URL"]

        if "CT" in os.environ:
            self.ct = os.environ["CT"]
        else:
            self.skipTest("No CT set")
        self._twikey = twikey.TwikeyClient(key, base_url)

    def test_new_invoice(self):
        invoice = self._twikey.invoice.create(
            InvoiceRequest(
                id = "58073359-7fd0-4683-a60f-8c08096a189e",
                number = "Inv-" + str(round(time.time())),
                title = "Invoice " + date.today().strftime("%B"),
                remittance = "596843697521",
                ct = self.ct,
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
                ),
                # "pdf": "JVBERi0xLj....RU9GCg=="
                lines=[
                    LineItem(
                        code="A100",
                        description="Gymnastiekpakje maat M",
                        quantity=1,
                        uom="st",
                        unitprice=41.32,
                        vatcode="21",
                        vatsum=8.68,
                        vatrate=21.0,
                    ),
                    LineItem(
                        code="A101",
                        description="Springtouw",
                        quantity=2,
                        uom="st",
                        unitprice=20.66,
                        vatcode="21",
                        vatsum=8.68,
                        vatrate=21.0,
                    )
                ]
            )
        )
        self.assertIsNotNone(invoice)
        print("New invoice to be paid @ " + invoice.url)


    def test_update(self):
        invoice = self._twikey.invoice.update(
            UpdateInvoiceRequest(
                id="58073359-7fd0-4683-a60f-8c08096a189e",
                title="Invoice " + date.today().strftime("%B"),
                date=(date.today() + timedelta(days=7)),
                duedate=(date.today() + timedelta(days=14)),
                state="BOOKED"
            )
        )
        self.assertIsNotNone(invoice)

    def test_delete(self):
        invoice = self._twikey.invoice.create(
            InvoiceRequest(
                id=str(uuid.uuid4()),
                number="Inv-" + str(round(time.time())),
                title="Invoice " + date.today().strftime("%B"),
                remittance="596843697521",
                ct=self.ct,
                amount=100,
                date=(date.today() + timedelta(days=7)),
                duedate=(date.today() + timedelta(days=14)),
                customer=Customer(
                    customer_number="customer2",
                    email="no-reply@twikey.com",
                    first_name="Twikey",
                    last_name="Support",
                    address="Derbystraat 43",
                    city="Gent",
                    zip="9051",
                    country="BE",
                    lang="en",
                    mobile="32498665995",
                ),
                # "pdf": "JVBERi0xLj....RU9GCg=="
            )
        )
        self.assertIsNotNone(invoice)
        self._twikey.invoice.delete(invoice.id)

    def test_details(self):
        invoice = self._twikey.invoice.details(
            DetailsRequest(
                id="89946636-373f-4011-b13f-ac59f26a58cb",
                include_lastpayment=True,
                include_meta=True,
                include_customer=True,
            )
        )
        self.assertIsNotNone(invoice)

    def test_action(self):
        self._twikey.invoice.action(
            request=ActionRequest(
                id="1394e983-c6cd-4c58-98d9-6bf69c997547",
                type=ActionType.EMAIL,
            )
        )

    @unittest.skipIf("UBL_FILE" not in os.environ, "No UBL_FILE set")
    def test_UBL_upload(self):
        new_invoice = self._twikey.invoice.upload_ubl(
            UblUploadRequest(xml_path=os.environ["UBL_FILE"])
        )
        self.assertIsNotNone(new_invoice)

    def test_bulk_create_invoices(self):
        batch_invoices = self._twikey.invoice.bulk_create(
            BulkInvoiceRequest(
                invoices=[
                    InvoiceRequest(
                        id=str(uuid.uuid4()),
                        number="Inv-" + str(round(time.time()) + i),
                        title="Invoice " + date.today().strftime("%B"),
                        ct=self.ct,
                        amount=42.50,
                        date=(date.today() + timedelta(days=7)),
                        duedate=(date.today() + timedelta(days=14)),
                        customer=Customer(
                            customer_number="customer2",
                            email="no-reply@twikey.com",
                            first_name="Twikey",
                            last_name="Support",
                            address="Derbystraat 43",
                            city="Gent",
                            zip="9051",
                            country="BE",
                            lang="en",
                            mobile="32498665995",
                        ),
                    )
                    for i in range(5)
                ]
            )
        )
        self.assertIsNotNone(batch_invoices)

    def test_batch_details(self):
        batch_invoices = self._twikey.invoice.bulk_create(
            BulkInvoiceRequest(
                invoices=[
                    InvoiceRequest(
                        id=str(uuid.uuid4()),
                        number="Inv-" + str(round(time.time()) + i),
                        title="Invoice " + date.today().strftime("%B"),
                        ct=self.ct,
                        amount=42.50,
                        date=(date.today() + timedelta(days=7)),
                        duedate=(date.today() + timedelta(days=14)),
                        customer=Customer(
                            customer_number="customer2",
                            email="no-reply@twikey.com",
                            first_name="Twikey",
                            last_name="Support",
                            address="Derbystraat 43",
                            city="Gent",
                            zip="9051",
                            country="BE",
                            lang="en",
                            mobile="32498665995",
                        ),
                    )
                    for i in range(2)
                ]
            )
        )
        self.assertIsNotNone(batch_invoices)

        batch_info = self._twikey.invoice.bulk_details(batch_id=batch_invoices.batch_id)
        self.assertIsNotNone(batch_info)

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
