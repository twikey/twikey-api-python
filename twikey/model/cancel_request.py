class CancelMandateRequest:
    """
    CancelMandateRequest holds the parameters required to cancel a mandate/document
    via the Twikey API.

    Attributes:
        mndtId (str): Mandate reference (Twikey's internal ID). Required.
        rsn (str): Reason for cancellation. Required.
                   Can be a descriptive string or an R-Message code.
        notify (bool, optional): Whether to notify the customer by email. Defaults to False.
    """

    __slots__ = ["mndtId", "rsn", "notify"]

    def __init__(self, mndtId: str, rsn: str, notify: bool = False):
        self.mndtId = mndtId
        self.rsn = rsn
        self.notify = notify

    def to_request(self) -> dict:
        """
        Converts the CancelMandateRequest object to a dictionary suitable
        for sending as request parameters in the Twikey API.

        Returns:
            dict: Dictionary with keys mapped to API parameters.
        """
        retval = {
            "mndtId": self.mndtId,
            "rsn": self.rsn,
        }
        # Only include notify if it's True (optional param)
        if self.notify:
            retval["notify"] = "true"
        return retval
