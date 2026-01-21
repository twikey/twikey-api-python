class PaymentLinkRequest:
    """
    PaymentLinkRequest fungeert als model om een betalingslink aan te maken voor een klant of naam.

    Deze klasse bevat alle optionele en verplichte parameters die je via de API kunt meesturen
    naar Twikey om een gepersonaliseerde betalingslink te genereren.

    Attributes:
        title (str): Verplicht. Bericht dat de klant zal zien op het bankafschrift.
        amount (str): Verplicht. Te betalen bedrag.
        customerNumber (str): Klantnummer (sterk aanbevolen).
        email (str): E-mailadres van de debiteur.
        lastname (str): Achternaam van de klant.
        firstname (str): Voornaam van de klant.
        companyName (str): Naam van het bedrijf (indien van toepassing).
        coc (str): Ondernemingsnummer.
        l (str): Taalcode (bv. nl, fr, de...).
        mobile (str): GSM-nummer.
        ct (str): Contracttemplate (voor registratie van klant).
        remittance (str): Mededeling bij betaling. Indien leeg, wordt 'title' gebruikt.
        redirectUrl (str): URL om na betaling naartoe te sturen.
        place (str): Plaats van betaling.
        expiry (str): Vervaldatum (ISO-formaat of timestamp).
        sendInvite (str): Verzendwijze van uitnodiging ('email', 'sms').
        address (str): Straat en huisnummer.
        city (str): Stad.
        zip (str): Postcode.
        country (str): Landcode (ISO 2-letter formaat).
        txref (str): Referentie van bestaande transacties.
        method (str): Bepaalde betaalmethode om selectie over te slaan.
        invoice (str): Specifiek factuurnummer voor betaling.
        isTemplate (bool): Gebruik een aangepaste betalingspagina.
        custom (dict): Extra attributen gedefinieerd in je Twikey-template.
    """

    __slots__ = [
        "title", "amount", "customer_number", "email", "last_name", "first_name", "company_name",
        "coc", "l", "mobile", "ct", "remittance", "ref", "redirect_url", "place", "expiry", "send_invite",
        "address", "city", "zip", "country", "txref", "method", "invoice", "is_template", "custom"
    ]

    def __init__(self, **kwargs):
        unknown_keys = set(kwargs) - set(self.__slots__)
        if unknown_keys:
            raise TypeError(f"Unknown parameter(s): {', '.join(unknown_keys)}")
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        """
        Zet het object om naar een dictionary voor de API-call.
        Converteert attributen naar camelCase, voegt custom attributen toe,
        en verwijdert None of lege waarden.
        """
        retval = {}
        retval["title"]=self.title
        retval["amount"]=self.amount
        retval["customerNumber"]=self.customer_number
        retval["email"]=self.email
        retval["lastName"]=self.last_name
        retval["firstName"]=self.first_name
        retval["companyName"]=self.company_name
        retval["coc"]=self.coc
        retval["l"]=self.l
        retval["mobile"]=self.mobile
        retval["ct"]=self.ct
        retval["remittance"]=self.remittance
        retval["ref"]=self.ref
        retval["redirectUrl"]=self.redirect_url
        retval["place"]=self.place
        retval["expiry"]=self.expiry
        retval["sendInvite"]=self.send_invite
        retval["address"]=self.address
        retval["city"]=self.city
        retval["zip"]=self.zip
        retval["country"]=self.country
        retval["txref"]=self.txref
        retval["method"]=self.method
        retval["invoice"]=self.invoice
        retval["isTemplate"]=self.is_template
        retval["custom"]=self.custom
        return retval

class PaymentLinkStatusRequest:
    """
    Get the status of a payment link

    See https://www.twikey.com/api/#status-paymentlink

    :param id: The ID of the payment link (optional)
    :param ref: Your custom reference to the payment link (optional)
    :param include_meta: Whether to include meta info like sdd, method, tx... (optional)
    :param include_refunds: Whether to include refunds info (optional)
    """

    __slots__ = ["id", "ref", "include_meta", "include_refunds"]

    def __init__(
            self,
            id: str = None,
            ref: str = None,
            include_meta: bool = False,
            include_refunds: bool = False
    ):
        self.id = id
        self.ref = ref
        self.include_meta = include_meta
        self.include_refunds = include_refunds

    def to_request(self) -> dict:
        params = {}
        if self.id:
            params["id"] = self.id
        if self.ref:
            params["ref"] = self.ref

        includes = []
        if self.include_meta:
            includes.append("meta")
        if self.include_refunds:
            includes.append("refunds")
        if includes:
            # Repeated 'include' parameters (expected by Twikey)
            # You can pass it to requests like: `params=[('include', 'meta'), ('include', 'refunds')]`
            # Or flatten to dict for basic use
            params["include"] = includes if len(includes) > 1 else includes[0]

        return params

class PaymentLinkRefundRequest:
    """
    Refund the full or partial amount of a payment link

    See https://www.twikey.com/api/#refund-paymentlink

    :param id: Paymentlink ID (required)
    :param message: Refund message (required)
    :param amount: Refund amount (optional, full amount if not passed)
    :param iban: Iban from where the amount should be held (optional)
    :param bic: via which bic the amount should go (optional)
    """

    __slots__ = ["id", "message", "amount", "iban", "bic"]

    def __init__(self, **kwargs):
        unknown_keys = set(kwargs) - set(self.__slots__)
        if unknown_keys:
            raise TypeError(f"Unknown parameter(s): {', '.join(unknown_keys)}")
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        req = {}
        for key in self.__slots__:
            val = getattr(self, key)
            if val is not None:
                req[key] = val
        return req
