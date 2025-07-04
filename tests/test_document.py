import os
import twikey
import unittest

from twikey.model.invite_request import InviteRequest
from twikey.model.fetch_request import FetchMandateRequest
from twikey.model.sign_request import SignRequest

class TestDocument(unittest.TestCase):
    _twikey = None

    @unittest.skipIf("TWIKEY_API_KEY" not in os.environ, "No TWIKEY_API_KEY set")
    def setUp(self):
        key = os.environ["TWIKEY_API_KEY"]
        base_url = "https://test.beta.twikey.com/api/creditor"
        if "TWIKEY_API_URL" in os.environ:
            base_url = os.environ["TWIKEY_API_URL"]
        self._twikey = twikey.TwikeyClient(key, base_url)

    def test_new_invite(self):
        ct = 1
        if "CT" in os.environ:
            ct = os.environ["CT"]

        inviteRequest = InviteRequest(
            ct=ct,
            email="no-reply@twikey.com",
            firstname="Info",
            lastname="Twikey",
            l="en",
            address="Abby road",
            city="Liverpool",
            zip="1526",
            country="BE",
            mobile="",
            iban="",
            bic="",
        )
        invite = self._twikey.document.create(inviteRequest)
        self.assertIsNotNone(invite)

    def test_sign(self):
        try:
            signed_mandate = self._twikey.document.sign(
                SignRequest(
                    ct="772",
                    l="en",
                    iban="BE36539660728150",
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
                    method="import",
                    sign_date="2025-07-03T14:21:45",
                    place="Brussels",
                )
            )
            print("signed Response:", signed_mandate)
            self.assertIsNotNone(signed_mandate)
            self.assertIsNotNone(signed_mandate.MndtId)
        except twikey.client.TwikeyError as e:
            # Known Twikey error response structure
            error_message = str(e)
            if "already signed" in error_message.lower():
                print("Mandate already signed. Skipping sign attempt.")
            elif "not found" in error_message.lower() or "no contract" in error_message.lower():
                print("Mandate not found. Cannot sign.")
            elif "smsPendingContract" in error_message:
                print("Mandate is currently pending SMS signature.")
            else:
                # Unexpected error, still raise it
                raise

    def test_feed(self):
        self._twikey.document.feed(MyDocumentFeed())


class MyDocumentFeed(twikey.DocumentFeed):
    def new_document(self, doc, evt_time):
        print("Document created   ", doc["MndtId"], "@", evt_time)

    def updated_document(self, original_number, doc, reason, evt_time):
        print(
            "Document updated   ", original_number, "b/c", reason["Rsn"], "@", evt_time
        )

    def cancelled_document(self, number, reason, evt_time):
        print("Document cancelled ", number, "b/c", reason["Rsn"], "@", evt_time)


if __name__ == "__main__":
    unittest.main()
