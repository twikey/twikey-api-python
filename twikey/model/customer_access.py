class CustomerAccessRequest:
    """
    CustomerAccessRequest holds the parameter to request
    customer access to their mandate via the Twikey API.

    Attributes:
        mndtId (str): Mandate reference (Twikey internal ID). Required.
    """

    __slots__ = ["mndtId"]

    def __init__(self, mndtId: str):
        self.mndtId = mndtId

    def to_request(self) -> dict:
        """
        Converts the CustomerAccessRequest object to a dictionary
        suitable for sending as request parameters in the Twikey API.

        Returns:
            dict: Dictionary containing the mandate reference.
        """
        return {"mndtId": self.mndtId}
