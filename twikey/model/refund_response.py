class Refund:
    """
    Represents a single entry in a Refund status response.

    Attributes reflect the fields returned by the API.
    """

    __slots__ = [
        "id", "iban", "bic", "amount", "msg", "place", "ref", "date", "state", "bkdate"
    ]

    def __init__(self, raw: dict):
        for key in self.__slots__:
            setattr(self, key, raw.get(key))

    def __str__(self):
        return f"Refund ID: {self.id}, Amount: {self.amount}, Message: {self.msg}"


class CreditTransferBatch:
    """
    Represents a single entry in a Batch details response.

    Attributes reflect the fields returned by the API.
    """

    __slots__ = [
        "id", "pmtinfid", "progress", "entries"
    ]

    def __init__(self, raw: dict):
        for key in self.__slots__:
            setattr(self, key, raw.get(key))

    def __str__(self):
        return f"Refund ID: {self.id}, pmtinfid: {self.pmtinfid}, entries: {self.entries}"


class BeneficiaryEntry:
    """
    Represents a single entry in a get Beneficiary response.

    Attributes reflect the fields returned by the API.
    """

    __slots__ = [
        "name", "iban", "bic", "available", "address"
    ]

    def __init__(self, raw: dict):
        for key in self.__slots__:
            if key != "address":
                setattr(self, key, raw.get(key))
            else:
                addressline = raw.get("address")
                if addressline is not None:
                    self.address = f"{addressline.get('country')} {addressline.get('zip')} {addressline.get('city')} {addressline.get('street')}"


    def __str__(self):
        return f"Name: {self.name}, Iban: {self.iban}, Available: {self.available}"


class GetbeneficiarieResponse:
    """
    GetbeneficiarieResponse represents the response of a get beneficiary call.

    Attributes:
        results (list[BeneficiaryEntry]): List of individual beneficiaries.
    """

    __slots__ = ["results"]

    def __init__(self, raw: list):
        self.results = [BeneficiaryEntry(item) for item in raw]

    def __str__(self):
        return "\n".join(str(item) for item in self.results)


class RefundFeed:
    def refund(self, refund: Refund):
        """
        :refund: – Class object containing
            * id: Twikey id
            * iban: IBAN of the beneficiary
            * bic: BIC of the beneficiary
            * amount: Amount of the refund
            * msg: Message for the beneficiary
            * place: Optional place
            * ref: Your reference
            * date: Date when the transfer was requested
            * state: Paid
            * bkdate: Date when the transfer was done
        """
        pass
