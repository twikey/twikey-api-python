from datetime import datetime

class Document:
    __slots__ = [
        "mandate_id", "state", "local_instream", "sequence_type", "sign_date",
        "debtor_name", "debtor_street", "debtor_city", "debtor_zip", "debtor_country", "btw_nummer",
        "country_of_residence", "debtor_email", "customer_number", "debtor_iban", "Debtor_bic", "debtor_bank",
        "referenced_document", "supplementary_data"
    ]

    def __init__(self, **kwargs):
        mndt = kwargs.get("mandate", {})
        headers = kwargs.get("headers", {})

        self.mandate_id = mndt.get("MndtId")
        self.state = headers.get("X-STATE")
        self.local_instream = mndt.get("LclInstrm")

        ocrncs = mndt.get("Ocrncs", {})
        self.sequence_type = ocrncs.get("SeqTp")
        self.sign_date = ocrncs.get("Drtn", {}).get("FrDt")

        dbtr = mndt.get("Dbtr", {})
        addr = dbtr.get("PstlAdr", {})
        ctct = dbtr.get("CtctDtls", {})

        self.debtor_name = dbtr.get("Nm")
        self.debtor_street = addr.get("AdrLine")
        self.debtor_city = addr.get("TwnNm")
        self.debtor_zip = addr.get("PstCd")
        self.debtor_country = addr.get("Ctry")
        self.btw_nummer = dbtr.get("Id")
        self.country_of_residence = dbtr.get("CtryOfRes")
        self.debtor_email = ctct.get("EmailAdr")
        self.customer_number = ctct.get("Othr")

        self.debtor_iban = mndt.get("DbtrAcct")

        agent = mndt.get("DbtrAgt", {}).get("FinInstnId", {})
        self.Debtor_bic = agent.get("BICFI")
        self.debtor_bank = agent.get("Nm")

        self.referenced_document = mndt.get("RfrdDoc")

        # Convert SplmtryData into a dict for easier use
        self.supplementary_data = {
            item["Key"]: item["Value"]
            for item in mndt.get("SplmtryData", [])
        }

    def __str__(self):

        base_info = "\n".join(
            f"{slot:<22}: {getattr(self, slot, None)}" for slot in self.__slots__ if slot != "supplementary_data"
        )

        supp_info = "Supplimentary Data\n\n"
        for key, value in self.supplementary_data.items():
            supp_info += f"{key:<22}: {value}\n"

        return base_info + "\n\n" + supp_info

    def __repr__(self):
        return self.__str__()

class DocumentFeed:
    def start(self, position: str, number_of_updates: int):
        """
        Allow storing the start of the feed
        Useful for storing or logging the current feed position and the number of items
        :param position: position where the feed started returned by the 'X-LAST' header
        :param number_of_updates: number of items in the feed
        """
        pass

    def new_document(self, doc: Document, evt_time: datetime) -> bool:
        """
        Handle a newly available document
        :param doc: actual document
        :param evt_time: time of creation
        :return
        """
        pass

    def updated_document(self, original_doc_number: str, doc: Document, reason: str, author:str, evt_time: datetime) -> bool:
        """
        Handle an update of a document
        :param original_doc_number: original reference to the document
        :param doc: actual document
        :param reason: reason of change
        :param author: email of the author
        :param evt_time: time of creation
        """
        pass

    def cancelled_document(self, doc_number: str, reason: str, author:str, evt_time: datetime) -> bool:
        """
        Handle an cancelled document
        :param doc_number: reference to the document
        :param reason: reason of change
        :param author: email of the author
        :param evt_time: time of creation
        """
        pass

class InviteResponse:
    __slots__ = ["url", "key", "mndtId"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def __str__(self):
        return f"InviteResponse url={self.url}, key={self.key}, mndtId={self.mndtId}"


class SignResponse:
    __slots__ = ["MndtId","url"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def __str__(self):
        if self.url:
            return f"SignResponse url={self.url} mndtId={self.MndtId}\n"
        return f"SignResponse mndtId={self.MndtId}\n"


class QueryMandateResponse:
    __slots__ = [
        "id", "type", "state", "suspended", "pdf_available", "mandate_number",
        "contract_number", "ct", "sign_date", "iban", "bic"
    ]

    def __init__(self, data: dict):
        for key in self.__slots__:
            if "_" in key:
                prefix, suffix = key.split("_")
                datakey = f"{prefix}{suffix.title()}"
                setattr(self, key, data.get(datakey))
            else:
                setattr(self, key, data.get(key))

    def __str__(self):
        return "\n".join(f"{slot:<18}: {getattr(self, slot, None)}" for slot in self.__slots__)


class PdfResponse:
    def __init__(self, content: bytes, filename: str = None, content_type: str = "application/pdf"):
        self.content = content
        self.content_type = content_type
        self.filename = filename or "mandate.pdf"

    def save(self, path: str = None):
        path = path or self.filename
        with open(path, "wb") as f:
            f.write(self.content)
        return path

    def __str__(self):
        return f"PdfResponse(filename='{self.filename}', size={len(self.content)} bytes)"


class CustomerAccessResponse:
    __slots__ = ["token", "url"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def __str__(self):
        return f"InviteResponse url={self.url}, token={self.token}"