class FetchMandateRequest:
    """
    FetchMandateRequest holds the parameters required to fetch
    the details of a specific mandate from the Twikey API.

    Attributes:
        mndtId (str): Mandate reference (Twikey's internal ID). Required.
        force (bool, optional): If True, include non-signed mandate states in the response.
                                Defaults to False.
    """

    __slots__ = ["mndt_id", "force"]

    def __init__(self, mndt_id: str, force: bool = False):
        self.mndt_id = mndt_id
        self.force = force

    def to_request(self) -> dict:
        """
        Converts the FetchMandateRequest object to a dictionary
        suitable for sending as query parameters in the Twikey API.

        Returns:
            dict: Dictionary with keys mapped to API parameters.
        """
        retval = {"mndtId": self.mndt_id}
        if self.force:
            retval["force"] = "true"
        return retval
