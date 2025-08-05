import os
import time
import twikey
import unittest

from twikey.model.transaction_request import NewTransactionRequest, StatusRequest, ActionRequest, UpdateRequest, \
    RefundRequest, QueryTransactionsRequest, RemoveTransactionRequest
from twikey.model.transaction_response import Transaction

class TestTransaction(unittest.TestCase):
    _twikey = None

    ct = 1
    mndt_id = None

    @unittest.skipIf("TWIKEY_API_KEY" not in os.environ, "No TWIKEY_API_KEY set")
    def setUp(self):
        key = os.environ["TWIKEY_API_KEY"]
        base_url = "https://test.beta.twikey.com/api/creditor"
        if "TWIKEY_API_URL" in os.environ:
            base_url = os.environ["TWIKEY_API_URL"]

        if "MNDTNUMBER" in os.environ:
            self.mndt_id = os.environ["MNDTNUMBER"]
        else:
            self.skipTest("No MNDTNUMBER set")

        if "CT" in os.environ:
            self.ct = os.environ["CT"]
        else:
            self.skipTest("No CT set")
        self._twikey = twikey.TwikeyClient(key, base_url)

    def test_new_invite(self):
        tx = self._twikey.transaction.create(
            NewTransactionRequest(
                mndt_id = self.mndt_id,
                message = "Test Message",
                ref = "Merchant Reference",
                amount = 10.00,
                place = "Here",
            )
        )
        self.assertIsNotNone(tx)
        self._twikey.transaction.batch_send(self.ct)

    def test_tx_status(self):
        tx = self._twikey.transaction.status_details(
            StatusRequest(
                mndt_id=self.mndt_id,
                state="ERROR",
                include=["collection", "lastupdate", "links"]
            )
        )
        self.assertIsNotNone(tx)

    def test_action(self):
        self._twikey.transaction.action(
            ActionRequest(
                id="6302230",
                action="archive",
            )
        )

    def test_update(self):
        tx = self._twikey.transaction.create(
            NewTransactionRequest(
                mndt_id=self.mndt_id,
                message="Test Message",
                ref="Merchant Reference",
                amount=10.00,
                place="Here",
            )
        )

        self._twikey.transaction.update(
            UpdateRequest(
                id=tx.id,
                message="Test Message",
                ref="Merchant Reference",
                amount=10.00,
                place="Here",
            )
        )

    @unittest.skipIf("PAID_TX_ID" not in os.environ, "No PAID_TX_ID set")
    def test_refund(self):
        refund = self._twikey.transaction.refund(
            RefundRequest(
                id=os.environ["PAID_TX_ID"],
                message="Test message",
                amount=50.00,
            )
        )
        self.assertIsNotNone(refund)

    @unittest.skipIf("PAIN008_FILEPATH" not in os.environ, "No PAIN008_FILEPATH set")
    def test_batch_import(self):
        self._twikey.transaction.batch_import(self.ct, "PAIN008_FILEPATH")

    def test_query(self):
        tx = self._twikey.transaction.create(
            NewTransactionRequest(
                mndt_id=self.mndt_id,
                message="Test Message",
                ref="Merchant Reference",
                amount=50.00,
                place="Here",
            )
        )
        self._twikey.transaction.batch_send(self.ct)
        time.sleep(1)
        self._twikey.transaction.batch_send(self.ct)
        time.sleep(1)

        mandates = self._twikey.transaction.query(
            QueryTransactionsRequest(
                from_id=(tx.id-2),
            )
        )
        self.assertIsNotNone(mandates)

    def test_remove(self):
        tx = self._twikey.transaction.create(
            NewTransactionRequest(
                mndt_id=self.mndt_id,
                message="Test Message",
                ref="Merchant Reference",
                amount=50.00,
                place="Here",
            )
        )

        self._twikey.transaction.remove(
            RemoveTransactionRequest(
                id=tx.id
            )
        )

    @unittest.skipIf("CAMT053" not in os.environ, "No CAMT053 (file) set")
    def test_import_camt053(self):
        try:
            self._twikey.transaction.reporting_import(os.environ["CAMT053"])
        except twikey.TwikeyError as e:
            self.assertEqual("invalid_file", e.get_code())

    def test_feed(self):
        self._twikey.transaction.feed(MyFeed())


class MyFeed(twikey.TransactionFeed):
    def transaction(self, transaction: Transaction):
        state = transaction.state
        final = transaction.final
        ref = transaction.ref
        if not ref:
            ref = transaction.msg
        _state = state
        _final = ""
        if state == "PAID":
            _state = "is now paid"
        elif state == "ERROR":
            _state = f"failed due to '#{transaction.bkmsg}'"
            if final:
                # final means Twikey has gone through all dunning steps, but customer still did not pay
                _final = "with no more dunning steps"
        print(f"Transaction update #{transaction.amount} euro with #{ref} #{_state} #{_final}")

if __name__ == "__main__":
    unittest.main()
