class UpdateMandateRequest:
    """
    UpdateMandateRequest holds the parameters for updating a mandate
    via the Twikey API.

    Attributes:
        mndtId (str): Mandate reference (Twikey internal ID). Required.
        ct (int, optional): Move the document to a different template ID (of the same type).
        state (str, optional): 'active' or 'passive' (activate or suspend mandate).
        mobile (str, optional): Customer's mobile number in E.164 format.
        iban (str, optional): Debtor's IBAN.
        bic (str, optional): Debtor's BIC code.
        customerNumber (str, optional): Customer number (add/update or move mandate).
        email (str, optional): Debtor's email address.
        firstname (str, optional): Debtor's first name.
        lastname (str, optional): Debtor's last name.
        companyName (str, optional): Company name on mandate.
        coc (str, optional): Enterprise number (only changeable if companyName is changed).
        l (str, optional): Language code on mandate.
        address (str, optional): Street address (required if updating address).
        city (str, optional): City of debtor (required if updating address).
        zip (str, optional): Zip code of debtor (required if updating address).
        country (str, optional): Country code in ISO format (required if updating address).
    """

    __slots__ = [
        "mndtId", "ct", "state", "mobile", "iban", "bic", "customerNumber",
        "email", "firstname", "lastname", "companyName", "coc", "l",
        "address", "city", "zip", "country"
    ]

    _field_map = {
        "mndtId": "mndtId",
        "ct": "ct",
        "state": "state",
        "mobile": "mobile",
        "iban": "iban",
        "bic": "bic",
        "customerNumber": "customerNumber",
        "email": "email",
        "firstname": "firstName",
        "lastname": "lastName",
        "companyName": "companyName",
        "coc": "coc",
        "l": "l",
        "address": "address",
        "city": "city",
        "zip": "zip",
        "country": "country",
    }

    def __init__(self, mndtId: str, **kwargs):
        self.mndtId = mndtId
        for attr in self.__slots__:
            if attr == "mndtId":
                continue
            setattr(self, attr, kwargs.get(attr, None))

    def to_request(self) -> dict:
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr)
            if value is not None:
                key = self._field_map.get(attr, attr)
                if isinstance(value, bool):
                    retval[key] = "true" if value else "false"
                else:
                    retval[key] = value
        return retval