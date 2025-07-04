class LegalItemsRetrieveRequest:
    """
    LegalItemsRetrieveRequest holds the parameter to retrieve
    legal items localized for a specific locale via the Twikey API.

    Attributes:
        locale (str, optional): Locale code (e.g., "fr", "fr_FR", "nl_BE", "en").
                                Defaults to "en" if not provided.
    """

    __slots__ = ["locale"]

    def __init__(self, locale: str = "en"):
        self.locale = locale

    def to_request(self) -> dict:
        """
        Converts the LegalItemsRetrieveRequest object to a dictionary
        suitable for sending as request parameters in the Twikey API.

        Returns:
            dict: Dictionary containing the locale parameter if set.
        """
        if self.locale:
            return {"locale": self.locale}
        return {}