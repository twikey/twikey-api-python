class MandateActionRequest:
    """
    MandateActionRequest holds parameters to perform actions on a mandate
    via the Twikey API.

    Attributes:
        mndtId (str): Mandate reference (Twikey internal ID). Required.
        invite (bool, optional): If True, send an invitation email to the customer.
        reminder (bool, optional): If True, send a reminder email to the customer.
        access (bool, optional): If True, send the customer a link to access their mandate.
        automaticCheck (bool, optional): If True, enable automatic validation for B2B mandates.
        manualCheck (bool, optional): If True, disable automatic validation for B2B mandates.
    """

    __slots__ = ["mndtId", "invite", "reminder", "access", "automaticCheck", "manualCheck"]

    def __init__(
            self,
            mndtId: str,
            invite: bool = False,
            reminder: bool = False,
            access: bool = False,
            automaticCheck: bool = False,
            manualCheck: bool = False,
    ):
        self.mndtId = mndtId
        self.invite = invite
        self.reminder = reminder
        self.access = access
        self.automaticCheck = automaticCheck
        self.manualCheck = manualCheck

    def to_request(self) -> dict:
        """
        Converts the MandateActionRequest to a dictionary
        for sending as request parameters to the Twikey API.

        Returns:
            dict: Dictionary with keys mapped to API parameters,
                  including only True flags.
        """
        retval = {"mndtId": self.mndtId}

        # Only include parameters set to True
        for attr in self.__slots__:
            if attr == "mndtId":
                continue
            value = getattr(self, attr)
            if value:
                retval[attr] = "true"

        return retval
