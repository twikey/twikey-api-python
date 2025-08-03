class CreatedPaylinkResponse:
    """
    Represents a single entry in a transaction status response.

    Attributes reflect the fields returned by the API.
    """

    __slots__ = [
        "id", "url", "amount", "msg"
    ]

    def __init__(self, raw: dict):
        for key in self.__slots__:
            setattr(self, key, raw.get(key))

    def __str__(self):
        return f"Transaction ID: {self.id}, Amount: {self.amount}, Url: {self.url}"


class CustomerInfo:
    __slots__ = [
        "id", "email", "firstname", "lastname", "address",
        "city", "zip", "country", "customerNumber", "l", "mobile"
    ]

    def __init__(self, raw: dict):
        for key in self.__slots__:
            setattr(self, key, raw.get(key))


class MetaInfo:
    __slots__ = ["active", "sdd", "tx", "method", "invoice"]

    def __init__(self, raw: dict):
        for key in self.__slots__:
            setattr(self, key, raw.get(key))

class TimeInfo:
    __slots__ = ["creation", "expiration", "lastupdate"]

    def __init__(self, raw: dict):
        for key in self.__slots__:
            setattr(self, key, raw.get(key))

class Paylink:
    """
    Represents a single entry for paylink responses.
    """

    __slots__ = ["id", "ct", "amount", "msg", "ref", "state", "customer", "meta", "time"]

    def __init__(self, raw: dict):
        for key in ["id", "ct", "amount", "msg", "ref", "state"]:
            setattr(self, key, raw.get(key))
        self.customer = CustomerInfo(raw["customer"]) if "customer" in raw else None
        self.meta = MetaInfo(raw["meta"]) if "meta" in raw else None
        self.time = TimeInfo(raw["time"]) if "time" in raw else None

    def __str__(self):
        return f"Paylink ID: {self.id}, Ref: {self.ref}, Amount: {self.amount}, State: {self.state}"

class PaylinkFeed:
    def paylink(self, paylink:Paylink) -> bool:
        """
        Custom logic for handeling the paylinks gained from the api call

        :param paylink: information about a singular paylink
        :return: in case of your business logic decides stop processing updates return True
        """
        pass