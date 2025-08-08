import os
import twikey
import unittest

from twikey.model.document_request import SignMethod, UpdateMandateRequest, PdfUploadRequest
from twikey.model.document_request import InviteRequest, SignRequest, FetchMandateRequest, QueryMandateRequest, \
    MandateActionRequest


class TestDocument(unittest.TestCase):
    _twikey = None
    ct = 1

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

    def test_new_invite(self):
        invite = self._twikey.document.create(
            InviteRequest(
                ct=self.ct,
                email="no-reply@twikey.com",
                first_name="Info",
                last_name="Twikey",
                l="en",
                address="Abby road",
                city="Liverpool",
                zip="1526",
                country="BE",
                mobile="",
                iban="",
                bic="",
            )
        )
        self.assertIsNotNone(invite)

    def test_sign(self):
        signed_mandate = self._twikey.document.sign(
            SignRequest(
                ct=self.ct,
                l="en",
                iban="NL46ABNA8910219718",
                bic="GKCCBEBB",
                customer_number="CUST001",
                email="joe.doe@gmail.com",
                last_name="Doe",
                first_name="John",
                mobile="+32499000001",
                address="Main Street 1",
                city="Brussels",
                zip="1000",
                country="BE",
                company_name="Acme Corp",
                vat_no="BE0123456789",
                campaign="Summer2025",
                prefix="Mr.",
                check=True,
                ed="2025-07-31",
                reminder_days=3,
                send_invite=False,
                token="abc123token",
                require_validation=False,
                transaction_amount=49.95,
                transaction_message="Welcome fee",
                transaction_ref="TXN001",
                plan="monthly",
                subscription_start="2025-08-01",
                subscription_recurrence="1m",
                subscription_stop_after=12,
                subscription_amount=9.99,
                subscription_message="Monthly membership",
                subscription_ref="SUB001",
                method=SignMethod.ITSME,
                # sign_date="2025-07-03T14:21:45",
                place="Brussels",
            )
        )
        print("Imported mandate:", signed_mandate)
        self.assertIsNotNone(signed_mandate)
        self.assertIsNotNone(signed_mandate.mandate_number)

    def test_fetch(self):
        fetched_mandate = self._twikey.document.fetch(
            FetchMandateRequest(
                mandate_number=os.environ["MNDTNUMBER"],
                force=True,
            )
        )
        self.assertIsNotNone(fetched_mandate)
        self.assertIsNotNone(fetched_mandate.mandate_number)
        self.assertIsNotNone(fetched_mandate.iban)

    def test_query(self):
        result_set = self._twikey.document.query(
            QueryMandateRequest(
                iban="BE51561419613262",
                customer_number="customer123",
                email="no-reply@twikey.com",
            )
        )
        self.assertIsNotNone(result_set)
        self.assertIsNotNone(result_set.mandates)

    def test_cancel(self):
        signed_mandate = self._twikey.document.sign(
            SignRequest(
                ct=self.ct,
                l="en",
                iban="BE51561419613262",
                bic="GKCCBEBB",
                customer_number="CUST001",
                email="joe.doe@gmail.com",
                last_name="Doe",
                first_name="John",
                mobile="+32499000001",
                address="Main Street 1",
                city="Brussels",
                zip="1000",
                country="BE",
                company_name="Acme Corp",
                vat_no="BE0123456789",
                campaign="Summer2025",
                prefix="Mr.",
                check=True,
                ed="2025-07-31",
                reminder_days=3,
                send_invite=False,
                token="abc123token",
                require_validation=False,
                transaction_amount=49.95,
                transaction_message="Welcome fee",
                transaction_ref="TXN001",
                plan="monthly",
                subscription_start="2025-08-01",
                subscription_recurrence="1m",
                subscription_stop_after=12,
                subscription_amount=9.99,
                subscription_message="Monthly membership",
                subscription_ref="SUB001",
                method=SignMethod.ITSME,
                # sign_date="2025-07-03T14:21:45",
                place="Brussels",
            )
        )
        self.assertIsNotNone(signed_mandate)
        self._twikey.document.cancel(signed_mandate.mandate_number,"reason for cancel")

    def test_action(self):
        self._twikey.document.action(
            MandateActionRequest(
                mandate_number=os.environ["MNDTNUMBER"],
                type="reminder",
                reminder="1"
            )
        )

    def test_update(self):
        invite = self._twikey.document.create(
            InviteRequest(
                ct=self.ct,
                email="no-reply@twikey.com",
                first_name="Info",
                last_name="Twikey",
                l="en",
                address="Abby road",
                city="Liverpool",
                zip="1526",
                country="BE",
                mobile="",
                iban="",
                bic="",
            )
        )
        self._twikey.document.update(
            invite.mandate_number,
            UpdateMandateRequest(
                ct=self.ct,
                state="active",
                mobile="+32499000001",
                iban="BE51561419613262",
                bic="GKCCBEBB",
                customer_number="CUST001",
                email="joe.doe@gmail.com",
                first_name="John",
                last_name="Doe",
                company_name="Acme Corp",
                coc="BE0123456789",
                l="en",
                address="Main Street 1",
                city="Brussels",
                zip="1000",
                country="BE",
            )
        )

    @unittest.skipIf("PDF_FILE" not in os.environ, "No PDF_FILE set")
    def test_upload_pdf(self):
        signed_mandate = self._twikey.document.sign(
            SignRequest(
                ct=self.ct,
                l="en",
                iban="BE51561419613262",
                bic="GKCCBEBB",
                customer_number="CUST001",
                email="joe.doe@gmail.com",
                last_name="Doe",
                first_name="John",
                mobile="+32499000001",
                address="Main Street 1",
                city="Brussels",
                zip="1000",
                country="BE",
                company_name="Acme Corp",
                vat_no="BE0123456789",
                campaign="Summer2025",
                prefix="Mr.",
                check=True,
                ed="2025-07-31",
                reminder_days=3,
                send_invite=False,
                token="abc123token",
                require_validation=False,
                transaction_amount=49.95,
                transaction_message="Welcome fee",
                transaction_ref="TXN001",
                plan="monthly",
                subscription_start="2025-08-01",
                subscription_recurrence="1m",
                subscription_stop_after=12,
                subscription_amount=9.99,
                subscription_message="Monthly membership",
                subscription_ref="SUB001",
                method=SignMethod.ITSME,
                # sign_date="2025-07-03T14:21:45",
                place="Brussels",
            )
        )
        self.assertIsNotNone(signed_mandate)
        self._twikey.document.upload_pdf(
            PdfUploadRequest(
                mandate_number=signed_mandate.MndtId,
                pdf_path=os.environ["PDF_FILE"],
                bank_signature=False,
            )
        )

    def test_retrieve_pdf(self):
        retrieved_pdf = self._twikey.document.retrieve_pdf("CORERECURRENTNL17192")
        retrieved_pdf.save("/tmp/pdf.pdf")
        self.assertIsNotNone(retrieved_pdf)

    def test_customer_access(self):
        signed_mandate = self._twikey.document.sign(
            SignRequest(
                ct=self.ct,
                l="en",
                iban="BE51561419613262",
                bic="GKCCBEBB",
                customer_number="CUST001",
                email="joe.doe@gmail.com",
                last_name="Doe",
                first_name="John",
                mobile="+32499000001",
                address="Main Street 1",
                city="Brussels",
                zip="1000",
                country="BE",
                company_name="Acme Corp",
                vat_no="BE0123456789",
                campaign="Summer2025",
                prefix="Mr.",
                check=True,
                ed="2025-07-31",
                reminder_days=3,
                send_invite=False,
                token="abc123token",
                require_validation=False,
                transaction_amount=49.95,
                transaction_message="Welcome fee",
                transaction_ref="TXN001",
                plan="monthly",
                subscription_start="2025-08-01",
                subscription_recurrence="1m",
                subscription_stop_after=12,
                subscription_amount=9.99,
                subscription_message="Monthly membership",
                subscription_ref="SUB001",
                method=SignMethod.IMPORT,
                # sign_date="2025-07-03T14:21:45",
                place="Brussels",
            )
        )
        self.assertIsNotNone(signed_mandate)

        access_url = self._twikey.document.customer_access(signed_mandate.mandate_number)
        self.assertIsNotNone(access_url)

    def test_feed(self):
        self._twikey.document.feed(MyDocumentFeed())


class MyDocumentFeed(twikey.DocumentFeed):
    def new_document(self, doc: twikey.Document, evt_time):
        print("Document created   ", doc.mandate_number, "@", evt_time)

    def updated_document(self, original_doc_number: str, doc: twikey.Document, reason: str, author: str, evt_time):
        print("Document updated   ", original_doc_number, "b/c", reason, "@", evt_time)

    def cancelled_document(self, doc_number: str, reason: str, author: str, evt_time):
        print("Document cancelled ", doc_number, "b/c", reason, "@", evt_time)


if __name__ == "__main__":
    unittest.main()
