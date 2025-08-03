class NewTransactionRequest:
    """
    NewTransactionRequest functioneert als model om een request voor een nieuwe transactie op te bouwen.

    Attributes:
        mndt_id (str): Mandaatreferentie (verplicht).
        date (str): Datum van de transactie (optioneel, ISO-formaat YYYY-MM-DD).
        reqcolldt (str): Gewenste incassodatum (optioneel).
        message (str): Bericht op bankafschrift (verplicht, max 140 tekens).
        ref (str): Interne referentie (optioneel).
        amount (float): Te innen bedrag (verplicht).
        place (str): Plaats van transactie (optioneel).
        refase2e (bool): Gebruik ref als E2E-id (optioneel).
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
        Zet de NewTransactionRequest om naar een dictionary geschikt voor API-verzending.

        Returns:
            dict: De request payload met juiste veldnamen.
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
        Zet de DeleteInvoiceRequest om naar een dictionary geschikt voor API-verzending.

        Returns:
            dict: De request payload met juiste veldnamen.
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
    ActionRequest fungeert als model voor het uitvoeren van een actie op een bestaande factuur.

    Attributes:
        id (str): Het unieke ID van de factuur waarop de actie wordt uitgevoerd (verplicht).
        action (str): Het type actie dat moet worden uitgevoerd (verplicht).
    """

    __slots__ = ["id", "action"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        """
        Zet de ActionRequest om naar een dictionary geschikt voor API-verzending.

        Returns:
            dict: De request payload met juiste veldnamen.
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
    NewTransactionRequest functioneert als model om een request voor een update op een transactie op te bouwen.

    Attributes:
        id (str): transaction ID.
        reqcolldt (str): Gewenste incassodatum (optioneel).
        message (str): Bericht op bankafschrift (optioneel, max 140 tekens).
        ref (str): Interne referentie (optioneel).
        amount (float): Te innen bedrag (optioneel).
        place (str): Plaats van transactie (optioneel).
    """

    __slots__ = ["id", "reqcolldt", "message", "ref", "amount", "place"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        """
        Zet de NewTransactionRequest om naar een dictionary geschikt voor API-verzending.

        Returns:
            dict: De request payload met juiste veldnamen.
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
    NewTransactionRequest functioneert als model om een request voor een update op een transactie op te bouwen.

    Attributes:
        id (str): transaction ID.
        message (str): Bericht op bankafschrift (optioneel, max 140 tekens).
        amount (float): Te innen bedrag (optioneel).
        ref (str): Interne referentie (optioneel).
        place (str): Plaats van transactie (optioneel).
        iban (str): IBAN of the customer.
        bic (str): BIC/SWIFT code of the bank.
    """

    __slots__ = ["id", "message", "amount", "ref", "place", "iban", "bic"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        """
        Zet de RefundRequest om naar een dictionary geschikt voor API-verzending.

        Returns:
            dict: De request payload met juiste veldnamen.
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