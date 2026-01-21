class NewRefundRequest:
    """
    model for creating a refund (credit transfer).

    Attributes:
        customer_number (str): The customer number (strongly recommended).
        iban (str): Iban of the beneficiary.
        message (str): Message to the creditor.
        amount (float): Amount to be refunded.
        ref (str): Intern reference.
        date (str): execution date of the transaction (ReqdExctnDt).
        place (str): Optional place.
    """
    __slots__ = ["customer_number", "iban", "message", "amount", "ref", "date", "place"]

    def __init__(self, **kwargs):
        unknown_keys = set(kwargs) - set(self.__slots__)
        if unknown_keys:
            raise TypeError(f"Unknown parameter(s): {', '.join(unknown_keys)}")
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value not in [None, ""]:
                parts = attr.split("_")
                key = parts[0] + ''.join(p.title() for p in parts[1:])
                retval[key] = value
        return retval


class NewRefundBatchRequest:
    """
    Model for creating a batch of refunds.

    Attributes:
        ct (str): Profile containing the originating account.
        iban (str): Originating account, if different from ct account (optional).
    """
    __slots__ = ["ct", "iban"]

    def __init__(self, **kwargs):
        unknown_keys = set(kwargs) - set(self.__slots__)
        if unknown_keys:
            raise TypeError(f"Unknown parameter(s): {', '.join(unknown_keys)}")
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        return {attr: getattr(self, attr) for attr in self.__slots__ if getattr(self, attr) is not None}


class RefundBatchStatusRequest:
    """
    Model for requesting details of a batch of refunds.

    Attributes:
        id (str): Batch ID.
        pmtinfid (str): Payment Info ID of the batch.
    """
    __slots__ = ["id", "pmtinfid"]

    def __init__(self, **kwargs):
        unknown_keys = set(kwargs) - set(self.__slots__)
        if unknown_keys:
            raise TypeError(f"Unknown parameter(s): {', '.join(unknown_keys)}")
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        return {attr: getattr(self, attr) for attr in self.__slots__ if getattr(self, attr) is not None}


class NewBeneficiaryRequest:
    """
    Model for adding a beneficiary.

    Attributes:
        customer_number (str): The customer number.
        name (str): Firstname & lastname of the debtor.
        email (str): Email of the debtor.
        l (str): language of the customer.
        mobile (str): Mobile number.
        address (str): Address.
        city (str): City of debtor.
        zip (str): Zipcode of debtor.
        country (str): ISO format.
        company_name (str): The company name.
        vatno (str): The enterprise number.
        iban (str): IBAN of the beneficiary (required).
        bic (str): BIC of the beneficiary (optional).
    """
    __slots__ = [
        "customer_number", "name", "email", "l", "mobile", "address",
        "city", "zip", "country", "company_name", "vatno", "iban", "bic"
    ]

    def __init__(self, **kwargs):
        unknown_keys = set(kwargs) - set(self.__slots__)
        if unknown_keys:
            raise TypeError(f"Unknown parameter(s): {', '.join(unknown_keys)}")
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value not in [None, ""]:
                parts = attr.split("_")
                key = parts[0] + ''.join(p.title() for p in parts[1:])
                retval[key] = value
        return retval


class DisableBeneficiaryRequest:
    """
    Model for disabling a beneficiary based on IBAN.

    Attributes:
        iban (str): IBAN of the beneficiary (required).
        customer_number (str): The customer number (optional).
    """
    __slots__ = ["iban", "customer_number"]

    def __init__(self, **kwargs):
        unknown_keys = set(kwargs) - set(self.__slots__)
        if unknown_keys:
            raise TypeError(f"Unknown parameter(s): {', '.join(unknown_keys)}")
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value not in [None, ""]:
                parts = attr.split("_")
                key = parts[0] + ''.join(p.title() for p in parts[1:])
                retval[key] = value
        return retval
