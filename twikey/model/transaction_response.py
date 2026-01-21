class Transaction:
    """
    Represents a single transaction

    Attributes reflect the fields returned by the API.
    """

    __slots__ = [
        "id", "amount", "contract", "contractId", "date", "mndtId", "msg", "place", "ref", "state",
        "reqcolldt", "admincharge", "final", "bkerror", "bkmsg", "bkdate", "lastupdate", "collection", "link"
    ]

    def __init__(self, raw: dict):
        for key in self.__slots__:
            setattr(self, key, raw.get(key))

    def is_paid(self):
        """
        :return: whether this transaction was paid or not, note that this can change at any time
        """
        return self.state == 'PAID'

    def is_error(self):
        return self.state == 'ERROR'

    def __str__(self):
        return f"Transaction ID: {self.id}, Amount: {self.amount}, State: {self.state}"

class TransactionFeed:
    def transaction(self, transaction: Transaction):
        """
        Handle a transaction from the feed.

        :param: transaction: The updated transaction
        :return: Return True if an error occurred, else return False
        """
        pass


class TransactionStatusResponse:
    """
    Represents a list of transaction status entries.
    """

    __slots__ = ["entries"]

    def __init__(self, raw: dict):
        self.entries = [Transaction(entry) for entry in raw.get("Entries", [])]

    def __str__(self):
        return "\n".join(str(entry) for entry in self.entries)


class RefundResponse:
    """
    Represents a single entry in a transaction status response.

    Attributes reflect the fields returned by the API.
    """

    __slots__ = [
        "id", "iban", "bic", "amount", "message", "place", "ref", "date"
    ]

    def __init__(self, raw: dict):
        for key in self.__slots__:
            setattr(self, key, raw.get(key))

    def __str__(self):
        return f"Refunded Transaction ID: {self.id}, Amount: {self.amount}, From: {self.iban}"