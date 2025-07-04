class MandateQuery:
    """
    MandateQuery holds the parameters used to query mandates/contracts
    in the Twikey API.

    Attributes:
        iban (str): The IBAN of the contract. Required.
        customerNumber (str): The customer number. Required.
        email (str): Email address of the customer. Required.
        state (str, optional): Filter mandates by state (e.g., "SIGNED"). Defaults to "SIGNED".
                               Should be uppercase if specified.
        page (int, optional): Page number for pagination.
    """

    __slots__ = ["iban", "customerNumber", "email", "state", "page"]

    def __init__(self, iban: str, customerNumber: str, email: str, state: str = "SIGNED", page: int = None):
        self.iban = iban
        self.customerNumber = customerNumber
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
            "customerNumber": self.customerNumber,
            "email": self.email,
        }
        if self.state:
            retval["state"] = self.state
        if self.page is not None:
            retval["page"] = self.page
        return retval
