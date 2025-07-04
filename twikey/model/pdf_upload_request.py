class PdfUploadRequest:
    """
    PdfUploadRequest holds the parameters to upload a PDF for a mandate via the Twikey API.

    Attributes:
        mndtId (str): Mandate reference (Twikey internal ID). Required.
        bankSignature (str, optional): Includes the bank signature, typically "true" or "false". Defaults to "true".
    """

    __slots__ = ["mndtId", "bankSignature"]

    def __init__(self, mndtId: str, bankSignature: str = "true"):
        self.mndtId = mndtId
        self.bankSignature = bankSignature

    def to_request(self) -> dict:
        """
        Converts the PdfUploadRequest to a dictionary
        for sending as request parameters to the Twikey API.

        Returns:
            dict: Dictionary of parameters for the PDF upload request.
        """
        retval = {"mndtId": self.mndtId}
        if self.bankSignature is not None:
            retval["bankSignature"] = self.bankSignature
        return retval