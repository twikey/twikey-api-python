from enum import Enum


class InviteRequest:
    """
    InviteRequest holds the full set of fields that can be used
    to initiate a mandate invitation via the Twikey API.

    Attributes:
    ct (str): Contract template ID.
    l (str): Language code (e.g., 'en', 'nl').
    iban (str): IBAN of the customer.
    bic (str): BIC/SWIFT code of the bank.
    mandateNumber (str): Custom mandate number (optional).
    customerNumber (str): Internal customer reference.
    email (str): Email address of the invitee.
    lastname (str): Last name of the invitee.
    first_name (str): First name of the invitee.
    mobile (str): Mobile phone number (international format).
    address (str): Street address.
    city (str): City name.
    zip (str): Postal code.
    country (str): Country code (e.g., 'BE').
    companyName (str): Name of the company (if business mandate).
    vatno (str): VAT number.
    contractNumber (str): External contract number.
    campaign (str): Campaign identifier for tracking.
    prefix (str): Honorific or title (e.g., Mr., Ms.).
    check (bool): Whether Twikey should verify the IBAN.
    ed (str): Execution date for the mandate.
    reminderDays (int): Number of days before sending reminder.
    sendInvite (bool): Whether to send the invitation immediately.
    token (str): Optional token to pre-fill or resume an invite.
    requireValidation (bool): Whether IBAN validation is required.
    document (str): Document reference or identifier.
    transactionAmount (float): One-time transaction amount.
    transactionMessage (str): Message for the transaction.
    transactionRef (str): Reference for the transaction.
    plan (str): Identifier of a predefined payment plan.
    subscriptionStart (str): Start date for the subscription (YYYY-MM-DD).
    subscriptionRecurrence (str): Recurrence rule (e.g., "monthly").
    subscriptionStopAfter (int): Number of times the subscription should run.
    subscriptionAmount (float): Amount to be charged in each cycle.
    subscriptionMessage (str): Description or message for the subscription.
    subscriptionRef (str): Reference for the subscription.
    """

    __slots__ = [
        "ct", "l", "iban", "bic", "mandate_number", "customer_number", "email", "last_name", "first_name", "mobile",
        "address", "city", "zip", "country", "company_name", "vat_no", "contract_number", "campaign", "prefix", "check",
        "ed", "reminder_days", "send_invite", "token", "require_validation", "document", "transaction_amount",
        "transaction_message", "transaction_ref", "plan", "subscription_start", "subscription_recurrence",
        "subscription_stop_after", "subscription_amount", "subscription_message", "subscription_ref"
    ]

    _field_map = {
        "ct": "ct",
        "l": "l",
        "iban": "iban",
        "bic": "bic",
        "email": "email",
        "first_name": "firstname",
        "last_name": "lastname",
        "mandate_number": "mandateNumber",
        "customer_number": "customerNumber",
        "mobile": "mobile",
        "address": "address",
        "city": "city",
        "zip": "zip",
        "country": "country",
        "company_name": "companyName",
        "vat_no": "vatno",
        "contract_number": "contractNumber",
        "campaign": "campaign",
        "prefix": "prefix",
        "check": "check",
        "ed": "ed",
        "reminder_days": "reminderDays",
        "send_invite": "sendInvite",
        "token": "token",
        "require_validation": "requireValidation",
        "document": "document",
        "transaction_amount": "transactionAmount",
        "transaction_message": "transactionMessage",
        "transaction_ref": "transactionRef",
        "plan": "plan",
        "subscription_start": "subscriptionStart",
        "subscription_recurrence": "subscriptionRecurrence",
        "subscription_stop_after": "subscriptionStopAfter",
        "subscription_amount": "subscriptionAmount",
        "subscription_message": "subscriptionMessage",
        "subscription_ref": "subscriptionRef",
    }

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
            if value is not None and value != "":
                key = self._field_map.get(attr, attr)  # map attr name if exists
                # Convert boolean to "true"/"false" string if needed
                if isinstance(value, bool):
                    retval[key] = "true" if value else "false"
                else:
                    retval[key] = value
        return retval

class SignMethod(Enum):
    SMS = "sms"
    DIGISIGN = "digisign"
    IMPORT = "import"
    ITSME = "itsme"
    EMACHTIGING = "emachtiging"
    PAPER = "paper"
    IDIN = "iDIN"


class SignRequest(InviteRequest):

    """
    SignRequest holds the parameters needed to sign a mandate
    through various signing methods supported by the Twikey API, on top of the Invite request parameters

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
        _ = InviteRequest  # To indicate intentional inheritance without call
        unknown_keys = set(kwargs) - set(self.__slots__)
        if unknown_keys:
            raise TypeError(f"Unknown parameter(s): {', '.join(unknown_keys)}")
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is not None and value != "":
                if attr == "method":
                    retval["method"] = value.value
                else:
                    key = self._field_map.get(attr, attr)  # map attr name if exists
                    # Convert boolean to "true"/"false" string if needed
                    if isinstance(value, bool):
                        retval[key] = "true" if value else "false"
                    else:
                        retval[key] = value
        return retval


class FetchMandateRequest:
    """
    FetchMandateRequest holds the parameters required to fetch
    the details of a specific mandate from the Twikey API.

    Attributes:
        mandate_number (str): Mandate reference (Twikey's internal ID). Required.
        force (bool, optional): If True, include non-signed mandate states in the response.
                                Defaults to False.
    """

    __slots__ = ["mandate_number", "force"]

    def __init__(self, mandate_number: str, force: bool = False):
        self.mandate_number = mandate_number
        self.force = force

    def to_request(self) -> dict:
        """
        Converts the FetchMandateRequest object to a dictionary
        suitable for sending as query parameters in the Twikey API.

        Returns:
            dict: Dictionary with keys mapped to API parameters.
        """
        retval = {"mndtId": self.mandate_number}
        if self.force:
            retval["force"] = "true"
        return retval


class QueryMandateRequest:
    """
    MandateQuery holds the parameters used to query mandates/contracts
    in the Twikey API.

    Attributes:
        iban (str): The IBAN of the contract. Required.
        customer_number (str): The customer number. Required.
        email (str): Email address of the customer. Required.
        state (str, optional): Filter mandates by state (e.g., "SIGNED"). Defaults to "SIGNED".
                               Should be uppercase if specified.
        page (int, optional): Page number for pagination.
    """

    __slots__ = ["iban", "customer_number", "email", "state", "page"]

    def __init__(self, iban: str, customer_number: str, email: str, state: str = "SIGNED", page: int = None):
        self.iban = iban
        self.customer_number = customer_number
        self.email = email
        self.state = state.upper() if state else None
        self.page = page

    def to_request(self) -> dict:
        """
        Converts the MandateQuery object to a dictionary suitable
        for sending as query parameters in the Twikey API request.

        Returns:
            dict: Dictionary with keys mapped to API parameters.
        """
        retval = {
            "iban": self.iban,
            "customerNumber": self.customer_number,
            "email": self.email,
        }
        if self.state:
            retval["state"] = self.state
        if self.page is not None:
            retval["page"] = str(self.page)
        return retval


class MandateActionRequest:
    """
    MandateActionRequest holds parameters to perform actions on a mandate
    via the Twikey API.

    Attributes:
        mandate_number (str): Mandate reference (Twikey internal ID). Required.
        type (str): The action type to execute. Required.
        reminder (str, values 1 to 4): If Type reminder is chosen, specifies which reminder is sent.
    """

    __slots__ = ["mandate_number", "type", "reminder"]

    def __init__(self, **kwargs):
        unknown_keys = set(kwargs) - set(self.__slots__)
        if unknown_keys:
            raise TypeError(f"Unknown parameter(s): {', '.join(unknown_keys)}")
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        retval = {"mndtId": self.mandate_number, "type": self.type}
        if self.reminder is not None and self.reminder != "":
            retval["reminder"]=self.reminder
        return retval


class UpdateMandateRequest:
    """
    UpdateMandateRequest holds the parameters for updating a mandate
    via the Twikey API.

    Attributes:
        mandate_number (str): Mandate reference (Twikey internal ID). Required.
        ct (int, optional): Move the document to a different template ID (of the same type).
        state (str, optional): 'active' or 'passive' (activate or suspend mandate).
        mobile (str, optional): Customer's mobile number in E.164 format.
        iban (str, optional): Debtor's IBAN.
        bic (str, optional): Debtor's BIC code.
        customer_number (str, optional): Customer number (add/update or move mandate).
        email (str, optional): Debtor's email address.
        first_name (str, optional): Debtor's first name.
        last_name (str, optional): Debtor's last name.
        company_name (str, optional): Company name on mandate.
        coc (str, optional): Enterprise number (only changeable if companyName is changed).
        l (str, optional): Language code on mandate.
        address (str, optional): Street address (required if updating address).
        city (str, optional): City of debtor (required if updating address).
        zip (str, optional): Zip code of debtor (required if updating address).
        country (str, optional): Country code in ISO format (required if updating address).
    """

    __slots__ = [
        "ct", "state", "mobile", "iban", "bic", "customer_number",
        "email", "first_name", "last_name", "company_name", "coc", "l",
        "address", "city", "zip", "country"
    ]

    _field_map = {
        "ct": "ct",
        "state": "state",
        "mobile": "mobile",
        "iban": "iban",
        "bic": "bic",
        "customer_number": "customerNumber",
        "email": "email",
        "first_name": "firstName",
        "last_name": "lastName",
        "company_name": "companyName",
        "coc": "coc",
        "l": "l",
        "address": "address",
        "city": "city",
        "zip": "zip",
        "country": "country",
    }

    def __init__(self, **kwargs):
        unknown_keys = set(kwargs) - set(self.__slots__)
        if unknown_keys:
            raise TypeError(f"Unknown parameter(s): {', '.join(unknown_keys)}")
        for attr in self.__slots__:
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


class PdfUploadRequest:
    """
    PdfUploadRequest holds the parameters to upload a PDF for a mandate via the Twikey API.

    Attributes:
        mndt_id (str): Mandate reference (Twikey internal ID). Required.
        pdf_path (str): Path to the pdf you want to upload. Required
        bankSignature (str, optional): Includes the bank signature, typically "true" or "false". Defaults to "true".
    """

    __slots__ = ["mandate_number", "pdf_path", "bank_signature"]

    def __init__(self, mandate_number: str, pdf_path: str, bank_signature: bool = "true"):
        self.mandate_number = mandate_number
        self.pdf_path = pdf_path
        self.bank_signature = bank_signature

    def to_request(self) -> dict:
        """
        Converts the PdfUploadRequest to a dictionary
        for sending as request parameters to the Twikey API.

        Returns:
            dict: Dictionary of parameters for the PDF upload request.
        """
        retval = {"mndtId": self.mandate_number, "pdfPath": self.pdf_path}
        if self.bank_signature is not None:
            retval["bankSignature"] = str(self.bank_signature)
        return retval
