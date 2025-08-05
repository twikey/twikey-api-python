import requests

from .model.refund_request import NewBeneficiaryRequest, DisableBeneficiaryRequest, NewRefundRequest, \
    NewRefundBatchRequest
from .model.refund_response import Refund, RefundBatch, GetbeneficiarieResponse, RefundFeed, Beneficiary


class RefundService(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    def create_beneficiary_account(self, request: NewBeneficiaryRequest) -> Beneficiary:
        """
        See https://www.twikey.com/api/#add-a-beneficiary-account

        Create a new beneficiary account via a POST request to the API.

        This method sends the provided request payload to the corresponding endpoint
        and parses the JSON response into a response model. Typically used to initiate
        actions like inviting a customer, creating a mandate, or generating a payment link.
        Raises an error if the API response contains an error code or the request fails.

        Args:
            request (NewBeneficiaryRequest): An object representing the payload to send.

        Returns:
            Beneficiary: A structured response object representing the server’s reply.

        Raises:
            TwikeyAPIError: If the API returns an error or the request fails.
        """

        url = self.client.instance_url("/transfers/beneficiaries")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url,
                data=data,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Create beneficiary", response)
            return Beneficiary(response.json())
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Create beneficiary", e)

    def create(self, request: NewRefundRequest) -> Refund:
        """
        See https://www.twikey.com/api/#createadd-a-new-credit-transfer

        Create a new credit transfer via a POST request to the API.

        This method sends the provided request payload to the corresponding endpoint
        and parses the JSON response into a response model. Typically used to initiate
        actions like inviting a customer, creating a mandate, or generating a payment link.
        Raises an error if the API response contains an error code or the request fails.

        Args:
            request (NewRefundRequest): An object representing the payload to send.

        Returns:
            Refund: A structured response object representing the server’s reply, if there are entries.

        Raises:
            TwikeyAPIError: If the API returns an error or the request fails.
        """

        url = self.client.instance_url("/transfer")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url,
                data=data,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Create refund", response)
            _links = response.json()["Entries"]
            if _links and len(_links) > 0:
                return Refund(_links[0])
            raise self.client.raise_error("Missing refund")
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Create refund", e)

    def details(self, refund_id: str) -> Refund:
        """
        See https://www.twikey.com/api/#details-of-a-credit-transfer

        Retrieves refund status by ID, ref, or mandate ID.

        This method queries the Twikey API for the latest details related to the mandate, invoice, etc. for the
        provided identifier. Typically used for querying status based on ID, reference, or mandate.

        Args:
            refund_id (str): The unique identifier of the refund to retrieve.

        Returns:
            Refund: A structured response object representing the server’s reply.

        Raises:
            TwikeyError: If the API call fails or the identifier is invalid.
        """

        url = self.client.instance_url("/transfer/detail")
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers("application/json")
            response = requests.get(url=url, params={"id": refund_id}, headers=headers, timeout=15)
            if response.status_code != 200:
                raise self.client.raise_error("Transfer detail", response)
            _links = response.json()["Entries"]
            if _links and len(_links) > 0:
                return Refund(_links[0])
            raise self.client.raise_error("Missing entry")
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Transaction detail", e)

    def remove(self, refund_id: str):
        """
        See https://www.twikey.com/api/#remove-a-credit-transfer

        Sends a DELETE request to delete a refund that has not yet been sent to the bank on the Twikey API.

        This method allows the creditor to cancel/delete a resource by providing the unique ID.
        Typically used to delete/cancel object like an agreement, an invoice, or a payment link.
        Raises an error if the API response contains an error code or the request fails.

        Args:
            refund_id (str): The unique identifier of the refund to remove.

        Returns:
            None

        Raises:
            TwikeyAPIError: If the request fails or the response contains an API error code.
        """

        url = self.client.instance_url(f"/transfer?id={refund_id}")
        try:
            self.client.refresh_token_if_required()
            response = requests.delete(url=url, headers=self.client.headers(), timeout=15)
            response.raise_for_status()
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Remove Refund", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Remove Refund", e)

    def create_batch(self, request: NewRefundBatchRequest) -> RefundBatch:
        """
        See https://www.twikey.com/api/#batch-creation

        Create a new credit transfer batch via a POST request to the API.

        This method sends the provided request payload to the corresponding endpoint
        and parses the JSON response into a response model. Typically used to initiate
        actions like inviting a customer, creating a mandate, or generating a payment link.
        Raises an error if the API response contains an error code or the request fails.

        Args:
            request (NewRefundBatchRequest): An object representing the payload to send.

        Returns:
            RefundBatch: A structured response object representing the server’s reply.

        Raises:
            TwikeyAPIError: If the API returns an error or the request fails.
        """

        url = self.client.instance_url("/transfer/complete")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url,
                data=data,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Create batch refunds", response)
            _links = response.json()["CreditTransfers"]
            if _links and len(_links) > 0:
                return RefundBatch(_links[0])
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Create batch refunds", e)

    def batch_detail(self, request: NewRefundBatchRequest) -> RefundBatch:
        """
        See https://www.twikey.com/api/#batch-details

        Retrieves the status by ID, ref, or mandate ID of a batch of refunds.

        This method queries the Twikey API for the latest details related to the mandate, invoice, etc. for the
        provided identifier. Typically used for querying status based on ID, reference, or mandate.

        Args:
            request (NewRefundBatchRequest): The unique identifier of the batch to retrieve. An object representing the payload to send.

        Returns:
            RefundBatch: A structured response object representing the server’s reply.

        Raises:
            TwikeyError: If the API call fails or the identifier is invalid.
        """

        url = self.client.instance_url("/transfer/complete")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.get(
                url=url,
                params=data,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Batch detail", response)
            _links = response.json()["CreditTransfers"]
            if _links and len(_links) > 0:
                return RefundBatch(_links[0])
            raise self.client.raise_error("Missing link")
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Batch detail", e)

    def get_beneficiary_accounts(self, with_address: bool) -> GetbeneficiarieResponse:
        """
        See https://www.twikey.com/api/#get-beneficiary-accounts

        Retrieves all beneficiary accounts.

        This method queries the Twikey API for the latest details related to the mandate, invoice, etc. for the
        provided identifier.

        Args:
            with_address (bool): if the address needs to be included.

        Returns:
            GetbeneficiarieResponse: A structured response object representing the server’s reply.

        Raises:
            TwikeyError: If the API call fails or the identifier is invalid.
        """

        url = self.client.instance_url("/transfers/beneficiaries")
        try:
            self.client.refresh_token_if_required()
            response = requests.get(
                url=url,
                data={"withAddress": with_address},
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("get beneficiaries", response)
            return GetbeneficiarieResponse(response.json()['beneficiaries'])
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("get beneficiaries", e)

    def disable_beneficiary_accounts(self, request: DisableBeneficiaryRequest):
        """
        See https://www.twikey.com/api/#disable-a-beneficiary-account

        Sends a DELETE request to disable a beneficiary account on the Twikey API.

        This method allows the creditor to cancel/delete a resource by providing the unique ID.
        Typically used to delete/cancel object like an agreement, an invoice, or a payment link.
        Raises an error if the API response contains an error code or the request fails.

        Args:
            request (DisableBeneficiaryRequest): An object representing information for identifying the beneficiary.

        Returns:
            None

        Raises:
            TwikeyAPIError: If the request fails or the response contains an API error code.
        """

        url = self.client.instance_url(f"/transfers/beneficiaries/{request.iban}?customerNumber={request.customer_number}")
        try:
            self.client.refresh_token_if_required()
            response = requests.delete(
                url=url,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("disable beneficiaries", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("disable beneficiaries", e)

    def feed(self, refund_feed: RefundFeed):
        """
        See https://www.twikey.com/api/#get-credit-transfer-feed

        Fetches the latest refund feed including new, updated, or cancelled refunds.

        This method retrieves events from Twikey since the last sync. These events may concern
        mandates, invoices, payment link, etc. It's typically
        used to synchronize your CRM or ERP system with the current state on the Twikey
        platform. Can be triggered periodically or via webhook.

        Args:
            refund_feed (RefundFeed): Custom handler class with methods for processing
                new, updated, or cancelled refund events.

        Returns:
            None

        Raises:
            Exception: If the request to the feed endpoint fails or response is invalid.
        """

        url = self.client.instance_url("/transfer")
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers()
            response = requests.get(
                url=url,
                headers=headers,
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Feed refunds", response)
            feed_response = response.json()
            while len(feed_response["Entries"]) > 0:
                for msg in feed_response["Entries"]:
                    refund_feed.refund(Refund(msg))
                response = requests.get(
                    url=url,
                    headers=self.client.headers(),
                    timeout=15,
                )
                if "ApiErrorCode" in response.headers:
                    raise self.client.raise_error("Feed refunds", response)
                feed_response = response.json()
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Feed refunds", e)
