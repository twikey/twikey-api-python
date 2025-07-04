from .invite_request import InviteRequest

class SignRequest(InviteRequest):

    """
    SignRequest holds the parameters needed to sign a mandate
    through various signing methods supported by the Twikey API.

    Attributes:
        method (str): Method to sign (e.g., "sms", "digisign", "import", "itsme", "emachtiging", "paper").
                      Required.
        digsig (str, optional): Wet signature as PNG image encoded in base64. Required if method is "digisign".
        key (str, optional): Shortcode from the invite URL. Use this instead of 'mandateNumber' to sign a prepared mandate directly.
                             Max length 36.
        bic (str, optional): BIC code. Required for methods "emachtiging" and "iDIN". Max length 11.
        signDate (str, optional): Date and time of signature in xsd:dateTime format (ISO 8601).
                                  For SMS, this uses the date of reply.
        place (str, optional): Place of signature.
        bankSignature (bool, optional): For B2B mandates only. Requires bank validation if True (default).
                                        Set to False to disable bank validation.
    """

    __slots__ = InviteRequest.__slots__ + [
        "method", "digsig", "key", "sign_date", "place", "bank_signature"
    ]

    _field_map = {**InviteRequest._field_map, **{
        "method": "method",
        "digsig": "digsig",
        "key": "key",
        "sign_date": "signDate",
        "place": "place",
        "bank_signature": "bankSignature"
    }}

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is not None and value != "":
                key = self._field_map.get(attr, attr)  # map attr name if exists
                # Convert boolean to "true"/"false" string if needed
                if isinstance(value, bool):
                    retval[key] = "true" if value else "false"
                else:
                    retval[key] = value
        return retval

class SignResponse:
    __slots__ = ["url", "MndtId"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))