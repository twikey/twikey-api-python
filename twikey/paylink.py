import requests

from .model.paylink_request import PaymentLinkRequest, PaymentLinkStatusRequest, PaymentLinkRefundRequest
from .model.paylink_response import CreatedPaylinkResponse, Paylink, PaylinkFeed


class PaylinkService(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    def create(self, request: PaymentLinkRequest) -> CreatedPaylinkResponse:
        """
        See https://www.twikey.com/api/#create-paymentlink

        Create a new payment link via a POST request to the API.

        This method sends the provided request payload to the corresponding endpoint
        and parses the JSON response into a response model. Typically used to initiate
        actions like inviting a customer, creating a mandate, or generating a payment link.
        Raises an error if the API response contains an error code or the request fails.

        Args:
            request (PaymentLinkRequest): An object representing the payload to send.

        Returns:
            CreatedPaylinkResponse: A structured response object representing the server’s reply.

        Raises:
            TwikeyAPIError: If the API returns an error or the request fails.
        """

        url = self.client.instance_url("/payment/link")
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
                raise self.client.raise_error("Create paylink", response)
            json_response = response.json()
            return CreatedPaylinkResponse(json_response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Create paylink", e)

    def status_details(self, request: PaymentLinkStatusRequest) -> Paylink:
        """
        See https://www.twikey.com/api/#status-paymentlink

        Retrieves paylink status by ID, ref, or mandate ID.

        This method queries the Twikey API for the latest details related to the mandate, invoice, etc. for the
        provided identifier. Typically used for querying status based on ID, reference, or mandate.

        Args:
            request (PaymentLinkStatusRequest): An object representing information for identifying the paylink.

        Returns:
            Paylink: A structured response object representing the server’s reply.

        Raises:
            TwikeyError: If the API call fails or the identifier is invalid.
        """

        params = request.to_request()
        url = self.client.instance_url("/payment/link")
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers("application/json")
            response = requests.get(url=url, params=params, headers=headers, timeout=15)
            if response.status_code != 200:
                raise self.client.raise_error("Transaction detail", response)
            _links = response.json()["Links"]
            if len(_links) > 0:
                return Paylink(_links[0])
            raise self.client.raise_error("Missing link")
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Transaction detail", e)

    def refund(self, request: PaymentLinkRefundRequest) -> Paylink:
        """
        See https://www.twikey.com/api/#refund-paymentlink

        Creates a refund for a given payment link via a POST request to the API.

        If the beneficiary account does not exist yet,
        it will be registered to the customer using the mandate IBAN or the one provided.

        Args:
            request (PaymentLinkRefundRequest): An object representing the payload to send.

        Returns:
            Paylink: Response payload containing refund entry details

        Raises:
            TwikeyError: If the request fails or the API returns an error.
        """

        data = request.to_request()
        url = self.client.instance_url("/payment/link/refund")
        try:
            self.client.refresh_token_if_required()
            response = requests.post(url=url, data=data, headers=self.client.headers(), timeout=15)
            response.raise_for_status()
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Update transaction", response)
            return Paylink(response.json())
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Update transaction", e)

    def remove(self, link_id: int):
        """
        See https://www.twikey.com/api/#remove-paymentlink

        Sends a DELETE request to delete a payment link that has not yet been sent to the bank on the Twikey API.

        This method allows the creditor to cancel/delete a resource by providing the unique ID.
        Typically used to delete/cancel object like an agreement, an invoice, or a payment link.
        Raises an error if the API response contains an error code or the request fails.

        Args:
            link_id (int): The unique identifier of the payment link to remove.

        Returns:
            None

        Raises:
            TwikeyAPIError: If the request fails or the response contains an API error code.
        """

        url = self.client.instance_url(f"/payment/link?id={link_id}")
        try:
            self.client.refresh_token_if_required()
            response = requests.delete(url=url, headers=self.client.headers(), timeout=15)
            response.raise_for_status()
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Update transaction", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Update transaction", e)

    def feed(self, paylink_feed: PaylinkFeed):
        """
        See https://www.twikey.com/api/#paymentlink-feed

        Fetches the latest paylink feed including new, updated, or cancelled payment links.

        This method retrieves events from Twikey since the last sync. These events may concern
        mandates, invoices, payment link, etc. It's typically
        used to synchronize your CRM or ERP system with the current state on the Twikey
        platform. Can be triggered periodically or via webhook.

        Args:
            paylink_feed (PaylinkFeed): Custom handler class with methods for processing
                new, updated, or cancelled paylink events.

        Returns:
            None

        Raises:
            Exception: If the request to the feed endpoint fails or response is invalid.
        """

        url = self.client.instance_url("/payment/link/feed")
        try:
            self.client.refresh_token_if_required()
            response = requests.get(
                url=url,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Feed paylink", response)
            feed_response = response.json()
            while len(feed_response["Links"]) > 0:
                error = False
                for msg in feed_response["Links"]:
                    error = paylink_feed.paylink(Paylink(msg))
                if error:
                    break
                response = requests.get(
                    url=url,
                    headers=self.client.headers(),
                    timeout=15,
                )
                if "ApiErrorCode" in response.headers:
                    raise self.client.raise_error("Feed paylink", response)
                feed_response = response.json()
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Feed paylink", e)

