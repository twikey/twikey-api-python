class NewRefundRequest:
    """
    Model om een terugbetaling (credit transfer) aan te maken.

    Attributes:
        customer_number (str): Klantnummer (sterk aanbevolen).
        iban (str): IBAN van de begunstigde.
        message (str): Bericht aan de begunstigde (max 140 karakters).
        amount (float): Bedrag van de terugbetaling.
        ref (str): Interne referentie.
        date (str): Gewenste uitvoeringsdatum (ReqdExctnDt).
        place (str): Plaats van betaling.
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
    Model voor het aanmaken van een batch met terugbetalingen.

    Attributes:
        ct (str): Profiel met afzenderrekening.
        iban (str): Afwijkend afzenderrekeningnummer (optioneel).
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
    Model om details op te vragen van een batch terugbetalingen.

    Attributes:
        id (str): Batch ID.
        pmtinfid (str): Payment Info ID van de batch.
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
    Model om een begunstigde toe te voegen aan een contract.

    Attributes:
        customer_number (str): Klantnummer.
        name (str): Naam.
        email (str): E-mailadres.
        l (str): Taalcode.
        mobile (str): GSM-nummer.
        address (str): Adres.
        city (str): Stad.
        zip (str): Postcode.
        country (str): Land.
        company_name (str): Bedrijfsnaam.
        vatno (str): BTW-nummer.
        iban (str): IBAN van begunstigde (verplicht).
        bic (str): BIC-code (optioneel).
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
    Model om een begunstigde te deactiveren op basis van IBAN.

    Attributes:
        iban (str): IBAN van de begunstigde (verplicht).
        customer_number (str): Klantnummer ter verduidelijking (optioneel).
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
