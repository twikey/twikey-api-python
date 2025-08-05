from enum import Enum
from uuid import UUID
from datetime import date

class InvoiceRequest:
    """
    Invoice holds the full set of fields used to create an invoice via the Twikey API.

    Attributes:
    id (str): UUID of the invoice
    number (str): Invoice number (unique identifier). (required)
    title (str): Title or description for the invoice.
    remittance (str): Payment message, defaults to title if not specified.
    ref (str): Internal reference for your system.
    ct (str): Contract template identifier.
    amount (float): Amount to be billed. (required)
    date (date): Invoice issue date (YYYY-MM-DD). (required)
    duedate (date): Due date for payment (YYYY-MM-DD). (required)
    locale (str): Language of the invoice (e.g., 'nl', 'fr', 'de').
    manual (bool): Whether the invoice should be collected automatically.
    pdf (str): Base64-encoded PDF content.
    pdf_url (str): URL pointing to a downloadable PDF.
    redirect_url (str): Redirect URL after payment.
    email (str): Custom email address for invoicing.
    related_invoice_number (str): Reference to link a credit note to an invoice.
    cc (str): Comma-separated CC emails.
    customer (Customer): Nested Customer details.
    lines (list[LineItem]): Optional invoice line items.
    """

    __slots__ = [
        "id", "number", "title", "remittance", "ref", "ct", "amount", "date", "duedate", "locale",
        "manual", "pdf", "pdf_url", "redirect_url", "email", "related_invoice_number", "cc",
        "customer", "lines"
    ]

    _field_map = {
        "id": "id",
        "number": "number",
        "title": "title",
        "remittance": "remittance",
        "ref": "ref",
        "ct": "ct",
        "amount": "amount",
        "date": "date",
        "duedate": "duedate",
        "locale": "locale",
        "manual": "manual",
        "pdf": "pdf",
        "pdf_url": "pdfUrl",
        "redirect_url": "redirectUrl",
        "email": "email",
        "related_invoice_number": "relatedInvoiceNumber",
        "cc": "cc",
        "customer": "customer",
        "lines": "lines",
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
                key = self._field_map.get(attr, attr)
                if isinstance(value, bool):
                    retval[key] = "true" if value else "false"
                elif isinstance(value, UUID):
                    retval[key] = str(value)
                elif isinstance(value, date):
                    retval[key] = value.isoformat()
                elif isinstance(value, list):
                    retval[key] = [item.to_dict() for item in value]
                elif hasattr(value, "to_dict"):
                    retval[key] = value.to_dict()
                else:
                    retval[key] = value
        return retval

class Customer:
    """
    Customer contains customer information used in an invoice.

    Attributes:
        customer_number (str): Unique customer ID. (required if object is passed or email)
        email (str): Email address. (required if object is passed or customer_number)
        first_name (str): First name.
        last_name (str): Last name.
        company_name (str): Optional company name.
        coc (str): Chamber of commerce number.
        lang (str): Language.
        address (str): Street address.
        city (str): City.
        zip (str): Postal code.
        country (str): Country code.
        mobile (str): Mobile number.
        customer_by_document (str): Mandate number.
        customer_by_ref (str): Alternative reference.
    """
    __slots__ = [
        "customer_number", "email", "first_name", "last_name", "company_name", "coc", "lang",
        "address", "city", "zip", "country", "mobile", "customer_by_document", "customer_by_ref"
    ]

    _field_map = {
        "customer_number": "customerNumber",
        "email": "email",
        "first_name": "firstname",
        "last_name": "lastname",
        "company_name": "companyName",
        "coc": "coc",
        "lang": "lang",
        "address": "address",
        "city": "city",
        "zip": "zip",
        "country": "country",
        "mobile": "mobile",
        "customer_by_document": "customerByDocument",
        "customer_by_ref": "customerByRef",
    }

    def __init__(self, **kwargs):
        unknown_keys = set(kwargs) - set(self.__slots__)
        if unknown_keys:
            raise TypeError(f"Unknown parameter(s): {', '.join(unknown_keys)}")
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_dict(self):
        data = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is not None and value != "":
                key = self._field_map.get(attr, attr)
                data[key] = value
        return data


class LineItem:
    """
    LineItem represents a line in the invoice.

    Attributes:
        code (str): Code of the item.
        description (str): Description of the item.
        quantity (float): Number of units.
        uom (str): Unit of measurement.
        unitprice (float): Price per unit.
        vatcode (str): VAT code.
        vatsum (float): VAT amount.
    """
    __slots__ = [
        "code", "description", "quantity", "uom", "unitprice", "vatcode", "vatsum", "vatrate"
    ]

    _field_map = {
        "code": "code",
        "description": "description",
        "quantity": "quantity",
        "uom": "uom",
        "unitprice": "unitprice",
        "vatcode": "vatcode",
        "vatsum": "vatsum",
        "vatrate": "vatrate",
    }

    def __init__(self, **kwargs):
        unknown_keys = set(kwargs) - set(self.__slots__)
        if unknown_keys:
            raise TypeError(f"Unknown parameter(s): {', '.join(unknown_keys)}")
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_dict(self):
        data = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is not None and value != "":
                key = self._field_map.get(attr, attr)
                data[key] = value
        return data


class UpdateInvoiceRequest:
    """
        InvoiceRequest represents the data required to create or manage an invoice via the Twikey API.

        Attributes:
            id (str): id of the invoice
            title (str): Title of the invoice.
            date (str): Invoice date in format YYYY-MM-DD. (required)
            duedate (str): Invoice due date in format YYYY-MM-DD. (required)
            ref (str): Invoice reference (internal or external).
            pdf (str): Base64-encoded PDF document.
            status (str): Optional status of the invoice. Can be "booked", "archived", or "paid".
            extra (dict or str): Custom attributes to be passed with the invoice.
        """

    __slots__ = ["id", "title", "date", "duedate", "ref", "pdf", "status", "extra", ]

    _field_map = {
        "id": "id",
        "title": "title",
        "date": "date",
        "duedate": "duedate",
        "ref": "ref",
        "pdf": "pdf",
        "status": "state",
        "extra": "extra",
    }

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        """
        Converts the InvoiceRequest instance into a dictionary ready to be sent to the API.

        Returns:
            dict: Dictionary representation with appropriate field mappings and conversions.
        """
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is not None and value != "":
                key = self._field_map.get(attr, attr)
                if isinstance(value, date):
                    retval[key] = value.isoformat()
                else:
                    retval[key] = value
        return retval

class DetailsRequest:
    """
    InvoiceDetailsRequest is used to request the details of a specific invoice.

    Attributes:
        id (str): The unique invoice ID or invoice number. (required)
        include_lastpayment (bool): Whether to include last payment info.
        include_meta (bool): Whether to include invoice metadata.
        include_customer (bool): Whether to include full customer info.
    """

    __slots__ = ["id", "include_lastpayment", "include_meta", "include_customer"]

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.include_lastpayment = kwargs.get("include_lastpayment", False)
        self.include_meta = kwargs.get("include_meta", False)
        self.include_customer = kwargs.get("include_customer", False)

    def to_request(self) -> dict:
        """
        Returns the GET parameters to include in the API request.

        Returns:
            dict: Dictionary of query parameters (e.g. ?include=meta&include=lastpayment).
        """
        includes = []
        if self.include_lastpayment:
            includes.append("lastpayment")
        if self.include_meta:
            includes.append("meta")
        if self.include_customer:
            includes.append("customer")

        return {"include": includes} if includes else {}


class ActionRequest:
    """
    Attributes:
        id (str): UUID van de factuur die verwijderd moet worden. (required)

    """

    __slots__ = ["id", "type"]

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.type = kwargs.get("type")

    def to_request(self) -> dict:
        """
        Zet de ActionRequest om naar een dictionary geschikt voor API-verzending.

        Returns:
            dict: De request payload met juiste veldnamen.
        """
        retval = {}
        if self.id is not None and self.id != "":
            retval["id"] = self.id
        if self.type is not None and self.type != "":
            retval["type"] = self.type.value
        return retval


class ActionType(Enum):
    EMAIL = "email"
    SMS = "sms"
    REMINDER = "reminder"
    SMSREMINDER = "smsreminder"
    LETTER = "letter"
    LETTERWITHINVOICE = "letterWithInvoice"
    INVOICE = "invoice"
    REOFFER = "reoffer"
    PEPPOL = "peppol"
    PAYMENTPLAN = "paymentplan"


class UblUploadRequest:
    """
    UblUploadRequest represents the data needed to upload a UBL invoice to Twikey.

    Attributes:
        xml_content (str): The UBL invoice as a raw XML string. (required)
        manual (bool): If True, disables automatic collection. Sets X-MANUAL: true.
        invoice_id (str): Optional custom UUID for the invoice. Sets X-INVOICE-ID.
    """

    __slots__ = ["xml_path", "manual", "invoice_id"]

    def __init__(self, **kwargs):
        self.xml_path = kwargs.get("xml_path")  # required
        self.manual = kwargs.get("manual", False)
        self.invoice_id = kwargs.get("invoice_id")  # optional

    def to_headers(self) -> dict:
        headers = {
            "Content-Type": "application/xml"
        }
        if self.manual:
            headers["X-MANUAL"] = True
        if self.invoice_id:
            headers["X-INVOICE-ID"] = self.invoice_id
        return headers


class BulkInvoiceRequest:
    """
    BulkInvoiceRequest represents a list of invoice requests to be created in a single batch.

    Attributes:
        invoices (list[InvoiceRequest]): A list of InvoiceRequest objects.
    """

    __slots__ = ["invoices"]

    def __init__(self, invoices: list[InvoiceRequest]):
        self.invoices = invoices

    def to_request(self) -> list:
        """
        Converts the bulk invoice request to a JSON array.

        Returns:
            list: A list of dictionaries representing each invoice request.
        """
        return [inv.to_request() for inv in self.invoices]
