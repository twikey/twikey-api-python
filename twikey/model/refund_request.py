from dataclasses import dataclass, fields
from typing import Optional


@dataclass()
class CreateCreditTransferRequest:
    """
    :params:
        customer_number: str : The customer number (strongly recommended)
        iban: Optional[str] : Iban of the beneficiary (must be active)
        message: str : Message to the creditor (max 140 characters)
        amount: float : Amount to be refunded
        ref: Optional[str] : Reference of the transaction
        date: Optional[str] : Required execution date of the transaction (ReqdExctnDt)
        place: Optional[str] : Optional place
    :returns:
        dict : Payload for the POST /creditor/transfer request
    """
    customer_number: str
    message: str
    amount: float
    iban: Optional[str] = None
    ref: Optional[str] = None
    date: Optional[str] = None
    place: Optional[str] = None

    def to_request(self) -> dict:
        def to_camel(s):
            parts = s.split('_')
            return parts[0] + ''.join(w.title() for w in parts[1:])

        retval = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is not None:
                retval[to_camel(f.name)] = value
        return retval


# @dataclass()
# class GetCreditTransferFeedRequest:
#     """
#     :params:
#         include_seq: Optional[bool] : Whether to include sequence numbers
#     :returns:
#         dict : Query parameters for GET /creditor/transfer
#     """
#     include_seq: Optional[bool] = False


@dataclass()
class CreditTransferDetailRequest:
    """
    :params:
        id: str : ID (E2E identifier) of the created refund
    :returns:
        dict : Query parameters for GET /creditor/transfer/detail
    """
    id: str

    def to_request(self) -> dict:
        retval = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is not None:
                retval[f.name] = value
        return retval


@dataclass()
class RemoveCreditTransferRequest:
    """
    :params:
        id: str : ID of the created refund
    :returns:
        dict : Query parameters for DELETE /creditor/transfer
    """
    id: str

    def to_request(self) -> dict:
        retval = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is not None:
                retval[f.name] = value
        return retval


@dataclass()
class CreateTransferBatchRequest:
    """
    :params:
        ct: str : Profile containing the originating account
        iban: Optional[str] : Originating account if different from ct account
    :returns:
        dict : Query parameters for POST /creditor/transfer/complete
    """
    ct: str
    iban: Optional[str] = None

    def to_request(self) -> dict:
        retval = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is not None:
                retval[f.name] = value
        return retval


@dataclass()
class TransferBatchDetailsRequest:
    """
    :params:
        id: Optional[str] : Batch ID
        pmtinfid: Optional[str] : Payment Info ID of the batch
    :returns:
        dict : Query parameters for GET /creditor/transfer/complete
    """
    id: Optional[str] = None
    pmtinfid: Optional[str] = None

    def to_request(self) -> dict:
        retval = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is not None:
                retval[f.name] = value
        return retval


@dataclass()
class GetBeneficiariesRequest:
    """
    :params:
        with_address: bool : Whether to include addresses in the response
    :returns:
        dict : Query parameters for GET /creditor/transfers/beneficiaries
    """
    with_address: bool = True

    def to_request(self) -> dict:
        def to_camel(s):
            parts = s.split('_')
            return parts[0] + ''.join(w.title() for w in parts[1:])

        retval = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is not None:
                retval[to_camel(f.name)] = value
        return retval


@dataclass()
class AddBeneficiaryRequest:
    """
    :params:
        customer_number: Optional[str]
        name: Optional[str]
        email: Optional[str]
        l: Optional[str]
        mobile: Optional[str]
        address: Optional[str]
        city: Optional[str]
        zip: Optional[str]
        country: Optional[str]
        company_name: Optional[str]
        vatno: Optional[str]
        iban: str
        bic: Optional[str]
    :returns:
        dict : Payload for POST /creditor/transfers/beneficiaries
    """
    customer_number: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    l: Optional[str] = None
    mobile: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    company_name: Optional[str] = None
    vatno: Optional[str] = None
    iban: str = ""
    bic: Optional[str] = None

    def to_request(self) -> dict:
        def to_camel(s):
            parts = s.split('_')
            return parts[0] + ''.join(w.title() for w in parts[1:])

        retval = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is not None:
                retval[to_camel(f.name)] = value
        return retval


@dataclass()
class DisableBeneficiaryRequest:
    """
    :params:
        iban: str : IBAN of the beneficiary to disable
        customer_number: Optional[str] : Customer number for disambiguation
    :returns:
        dict : For DELETE /creditor/transfers/beneficiaries/{IBAN}?customerNumber={customerNumber}
    """
    iban: str
    customer_number: Optional[str] = None

    def to_request(self) -> dict:
        def to_camel(s):
            parts = s.split('_')
            return parts[0] + ''.join(w.title() for w in parts[1:])

        retval = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is not None:
                retval[to_camel(f.name)] = value
        return retval
