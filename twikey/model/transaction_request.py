class NewTransactionRequest:
    """
    NewTransactionRequest Allows you to create a new transaction

    Attributes:
        mndt_id (str): Mandate reference (required).
        date (str): Transaction date (optional, ISO format YYYY-MM-DD).
        reqcolldt (str): Desired collection date (optional).
        message (str): Message on bank statement (required, max. 140 characters).
        ref (str): Internal reference (optional).
        amount (float): Amount to be collected (required).
        place (str): Place of transaction (optional).
        refase2e (bool): Use ref as E2E ID (optional).
    """

    __slots__ = ["mndt_id", "date", "reqcolldt", "message", "ref", "amount", "place", "refase2e"]

    def __init__(self, **kwargs):
        unknown_keys = set(kwargs) - set(self.__slots__)
        if unknown_keys:
            raise TypeError(f"Unknown parameter(s): {', '.join(unknown_keys)}")
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        """
        Turns the request object into a dictionary for posting

        Returns:
            dict: request payload using the correct fieldnames
        """
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is not None and value != "":
                parts = attr.split("_")
                key = parts[0] + "".join(part.capitalize() for part in parts[1:])
                retval[key] = value
        return retval


class StatusRequest:
    """
    Represents a request to fetch transaction status details.

    Attributes:
        id (str): Optional transaction ID.
        ref (str): Optional transaction reference.
        mndt_id (str): Optional mandate reference.
        state (str): Optional filter for transaction state (OPEN, PAID, ERROR, UNPAID).
        include (list[str]): Optional list of includes (collection, lastupdate, link).
    """

    __slots__ = ["id", "ref", "mndt_id", "state", "include"]

    def __init__(self, id=None, ref=None, mndt_id=None, state=None, include=None):
        self.id = id
        self.ref = ref
        self.mndt_id = mndt_id
        self.state = state
        self.include = include or []

    def to_params(self):
        params = {}
        if self.id:
            params["id"] = self.id
        if self.ref:
            params["ref"] = self.ref
        if self.mndt_id:
            params["mndtId"] = self.mndt_id
        if self.state:
            params["state"] = self.state
        for inc in self.include:
            params.setdefault("include", []).append(inc)
        return params

    def to_request(self) -> dict:
        """
        Turns the object into a dictionary for posting

        Returns:
            dict: request payload using the correct fieldnames
        """
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is not None and value != "":
                parts = attr.split("_")
                key = parts[0] + "".join(part.capitalize() for part in parts[1:])
                retval[key] = value
        return retval


class ActionRequest:
    """
    ActionRequest object containing the values to run an action on a specific transaction.

    Attributes:
        id (str): The unique ID of the invoice on which the action is performed (required).
        action (str): The type of action to be performed (required).
    """

    __slots__ = ["id", "action"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        """
        Turns the object into a dictionary for posting

        Returns:
            dict: request payload using the correct fieldnames
        """
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is not None and value != "":
                parts = attr.split("_")
                key = parts[0] + "".join(part.capitalize() for part in parts[1:])
                retval[key] = value
        return retval


class UpdateRequest:
    """
    UpdateRequest contains the values to update an action on a specific transaction.

    Attributes:
        id (str): transaction ID.
        reqcolldt (str): Desired collection date (optional).
        message (str): Message on bank statement (optional, max. 140 characters).
        ref (str): Internal reference (optional).
        amount (float): Amount to be collected (optional).
        place (str): Place of transaction (optional).
    """

    __slots__ = ["id", "reqcolldt", "message", "ref", "amount", "place"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        """
        Turns the object into a dictionary for posting

        Returns:
            dict: request payload using the correct fieldnames
        """
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is not None and value != "":
                parts = attr.split("_")
                key = parts[0] + "".join(part.capitalize() for part in parts[1:])
                retval[key] = value
        return retval


class RefundRequest:
    """
    RefundRequest object containing the values to refund a specific transaction.

    Attributes:
        id (str): transaction ID.
        message (str): Message on bank statement (optional, max. 140 characters).
        amount (float): Amount to be collected (optional).
        ref (str): Reference (optional).
        place (str): Place of transaction (optional).
        iban (str): IBAN of the customer.
        bic (str): BIC/SWIFT code of the bank.
    """

    __slots__ = ["id", "message", "amount", "ref", "place", "iban", "bic"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        """
        Turns the object into a dictionary for posting

        Returns:
            dict: request payload using the correct fieldnames
        """
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is not None and value != "":
                parts = attr.split("_")
                key = parts[0] + "".join(part.capitalize() for part in parts[1:])
                retval[key] = value
        return retval


class RemoveTransactionRequest:
    """
    RemoveTransactionRequest models a DELETE request to remove a transaction
    that hasn't yet been sent to the bank. At least one of the parameters
    `id` or `ref` must be provided.

    Attributes:
        id (str): A transaction ID as returned in the POST response. Optional.
        ref (str): The transaction reference provided during creation. Optional.
    """

    __slots__ = ["id", "ref"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is not None and value != "":
                parts = attr.split("_")
                key = parts[0] + "".join(part.capitalize() for part in parts[1:])
                retval[key] = value
        return retval


class QueryTransactionsRequest:
    """
    QueryTransactionsRequest models a GET request to /creditor/transaction/query
    to retrieve a list of transactions, starting from a specific transaction ID.

    Attributes:
        from_id (int): The ID of the transaction to start from (required).
        mndt_id (str): The mandate reference (optional).
    """

    __slots__ = ["from_id", "mndt_id"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value not in [None, ""]:
                parts = attr.split("_")
                key = parts[0] + "".join(part.capitalize() for part in parts[1:])
                retval[key] = value
        return retval