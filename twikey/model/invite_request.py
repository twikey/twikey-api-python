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

class InviteResponse:
    __slots__ = ["url", "key", "mndtId"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))