import logging

import requests

from .model.invoice_request import InvoiceRequest, UpdateInvoiceRequest, DetailsRequest, ActionRequest, \
    UblUploadRequest, BulkInvoiceRequest
from .model.invoice_response import Invoice, BulkInvoiceResponse, \
    BulkBatchDetailsResponse, InvoiceFeed

class InvoiceService(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        self.logger = logging.getLogger(__name__)

    def create(self, request: InvoiceRequest, origin=False, purpose=False, manual=False) -> Invoice:
        """
        See https://www.twikey.com/api/#create-invoice

        Create a new invoice via a POST request to the API.

        This method sends the provided request payload to the corresponding endpoint
        and parses the JSON response into a response model. Typically used to initiate
        actions like inviting a customer, creating a mandate, or generating a payment link.
        Raises an error if the API response contains an error code or the request fails.

        Args:
            request (InvoiceRequest): A model representing the payload to send.

        Returns:
            Invoice: A structured response object representing the server’s reply.

        Raises:
            TwikeyAPIError: If the API returns an error or the request fails.
        """

        url = self.client.instance_url("/invoice")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers("application/json")
            if origin:
                headers["X-PARTNER"] = origin
            if purpose:
                headers["X-Purpose"] = purpose
            if manual:
                headers["X-MANUAL"] = "true"
            response = requests.post(
                url=url,
                json=data,
                headers=headers,
                timeout=15,
            )
            json_response = response.json()
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Create invoice", response)
            self.logger.debug("Added invoice : %s" % json_response["url"])
            return Invoice(**json_response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Create invoice", e)

    def update(self, request: UpdateInvoiceRequest) -> Invoice:
        """
        See https://www.twikey.com/api/#update-invoice

        Send a PUT request to update existing invoice details.

        This endpoint allows modifying invoice information such as title,
        pdf, or linked references. Only provide parameters for fields you
        wish to update. Some fields may have special behavior or limitations depending on the object state.

        Args:
            request (UpdateInvoiceRequest): A model representing the payload to send.

        Returns:
            Invoice: A structured response object representing the server’s reply.

        Raises:
            TwikeyError: If the API returns an error or the request fails.
        """

        data = request.to_request()
        url = self.client.instance_url("/invoice/" + data.get("id"))
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers("application/json")
            response = requests.put(url=url, json=data, headers=headers, timeout=15)
            json_response = response.json()
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Update invoice", response)
            self.logger.debug("Updated invoice : %s" % json_response["url"])
            return Invoice(**json_response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Update invoice", e)

    def details(self, request: DetailsRequest) -> Invoice:
        """
        See https://www.twikey.com/api/#invoice-details

        Retrieves the details of a specific invoice by ID or number,
        optionally including lastpayment, meta, or customer data.

        This method queries the Twikey API for the latest details related to the mandate, invoice, etc. for the
        provided identifier. Typically used for querying status based on ID, reference, or mandate.

        Args:
            request (DetailsRequest): An object representing information for identifying the invoice.

        Returns:
            Invoice: A structured response object representing the server’s reply.

        Raises:
            TwikeyError: If the API call fails or the identifier is invalid.
        """

        data = request.to_request()
        url = self.client.instance_url(f"/invoice/{request.id}")
        includes = data.get("include")
        if includes:
            query_string = "&".join(f"include={param}" for param in includes)
            url += f"?{query_string}"
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers("application/json")
            response = requests.get(url=url, headers=headers, timeout=15)
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("details invoice", response)
            self.logger.debug("details invoice: %s", response.text)
            return Invoice(**response.json())
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("details invoice", e)

    def action(self, request: ActionRequest):
        """
        See https://www.twikey.com/api/#action-on-invoice

        Trigger a specific action on an existing invoice.

        This endpoint allows initiating predefined actions related to an invoice, such as sending
        an invitation or reminder. The action type must be explicitly provided in the request.

        Args:
            request (ActionRequest): The action request with invoice ID and type.

        Returns:
            None

        Raises:
            TwikeyError: If the API returns an error or the request fails.
        """

        invoice_id = request.id
        url = self.client.instance_url(f"/invoice/{invoice_id}/action")
        payload = request.to_request()
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers("application/x-www-form-urlencoded")
            response = requests.post(url=url, data=payload, headers=headers, timeout=15)
            if response.status_code != 204:
                raise self.client.raise_error("action invoice", response)
            self.logger.debug("action invoice [%s]: %s", invoice_id, payload["type"])
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("action invoice", e)

    def upload_ubl(self, request: UblUploadRequest) -> Invoice:
        """
        See https://www.twikey.com/api/#upload-ubl

        add new invoices via an UBL file during a POST request to the API.

        Args:
            request (UblUploadRequest): object representing the payload for the request containing the file

        Returns:
            Invoice: A structured response object representing the server’s reply.

        Raises:
            Exception: If the request to the feed endpoint fails or response is invalid.
        """

        url = self.client.instance_url("/invoice/ubl")
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers("application/x-www-form-urlencoded")
            headers.update(request.to_headers())
            with open(request.xml_path, "rb") as file:
                response = requests.post(
                    url=url,
                    headers=headers,
                    data=file,
                    timeout=15
                )
            if response.status_code != 200:
                raise self.client.raise_error("UBL upload", response)
            self.logger.debug("UBL upload response: %s", response.text)
            return Invoice(**response.json())
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("UBL upload", e)

    def delete(self, invoice_id: str):
        """
        See https://www.twikey.com/api/#delete-invoice

        Sends a DELETE request to delete an invoice on the Twikey API.

        This method allows the creditor to cancel/delete a resource by providing the unique ID.
        Typically used to delete/cancel object like an agreement, an invoice, or a payment link.
        Raises an error if the API response contains an error code or the request fails.

        Args:
            invoice_id (str): The unique identifier of the invoice to cancel.

        Returns:
            None

        Raises:
            TwikeyAPIError: If the request fails or the response contains an API error code.
        """

        url = self.client.instance_url("/invoice/" + invoice_id)
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers("application/json")
            response = requests.delete(url=url, headers=headers, timeout=15)
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("delete invoice", response)
            self.logger.debug("delete invoice : %s")
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("delete invoice", e)

    def bulk_create(self, request: BulkInvoiceRequest):
        """
        See https://www.twikey.com/api/#bulk-create-invoices

        Creates multiple invoices in a single batch upload.

        Args:
            request (BulkInvoiceRequest): A list of invoice requests.

        Returns:
            BulkInvoiceResponse: Contains the batchId of the created batch.

        Raises:
            TwikeyError: If the bulk creation fails or the server returns an error.
        """

        url = self.client.instance_url("/invoice/bulk")
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers("application/json")
            data = request.to_request()
            response = requests.post(
                url=url,
                headers=headers,
                json=data,
                timeout=30
            )
            if response.status_code != 200:
                raise self.client.raise_error("bulk create invoices", response)
            self.logger.debug("bulk create invoices response: %s", response.text)
            return BulkInvoiceResponse(**response.json())
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("bulk create invoices", e)

    def bulk_details(self, batch_id: str) -> BulkBatchDetailsResponse:
        """
        See https://www.twikey.com/api/#bulk-batch-details

        Retrieves the result of a bulk invoice upload by batch ID.

        Args:
            batch_id (str): The batch ID.

        Returns:
            BulkBatchDetailsResponse: Contains a list of statuses per invoice.

        Raises:
            TwikeyError: If the request fails or returns an unexpected status.
        """
        url = self.client.instance_url(f"/invoice/bulk?batchId={batch_id}")
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers("application/json")
            response = requests.get(
                url=url,
                headers=headers,
                timeout=15
            )
            if response.status_code == 409:
                self.logger.debug("bulk batch still processing: %s", batch_id)
                return None
            elif response.status_code == 200:
                self.logger.debug("bulk batch details response: %s", response.text)
                return BulkBatchDetailsResponse(response.json())
            else:
                raise self.client.raise_error("bulk batch details", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("bulk batch details", e)

    def feed(self, invoice_feed: InvoiceFeed, start_position=False, *includes):
        """
        See https://www.twikey.com/api/#invoice-feed

        Fetches the latest invoice feed including new, updated, or cancelled invoices.

        This method retrieves events from Twikey since the last sync. These events may concern
        mandates, invoices, payment link, etc. It's typically
        used to synchronize your CRM or ERP system with the current state on the Twikey
        platform. Can be triggered periodically or via webhook.

        Args:
            invoice_feed (InvoiceFeed): Custom handler class with methods for processing
                new, updated, or cancelled invoice events.

        Returns:
            None

        Raises:
            Exception: If the request to the feed endpoint fails or response is invalid.
        """

        _includes = ""
        for include in includes:
            _includes += "&include=" + include

        url = self.client.instance_url("/invoice?include=customer" + _includes)
        try:
            self.client.refresh_token_if_required()
            initheaders = self.client.headers()
            if start_position:
                initheaders["X-RESUME-AFTER"] = str(start_position)
            response = requests.get(
                url=url,
                headers=initheaders,
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Feed invoice", response)
            feed_response = response.json()
            while len(feed_response["Invoices"]) > 0:
                number_of_invoices = len(feed_response["Invoices"])
                last_invoice = response.headers["X-LAST"]
                self.logger.debug(
                    "Feed handling : %d invoices from %s till %s"
                    % (number_of_invoices, start_position, last_invoice)
                )
                invoice_feed.start(
                    response.headers["X-LAST"], len(feed_response["Invoices"])
                )
                error = False
                for invoice in feed_response["Invoices"]:
                    self.logger.debug("Feed handling : %s" % invoice)
                    error = invoice_feed.invoice(Invoice(**invoice))
                    if error:
                        break
                if error:
                    self.logger.debug("Error while handing invoice, stopping")
                    break
                response = requests.get(
                    url=url,
                    headers=self.client.headers(),
                    timeout=15,
                )
                if "ApiErrorCode" in response.headers:
                    raise self.client.raise_error("Feed invoice", response)
                feed_response = response.json()
            self.logger.debug("Done handing invoice feed")
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Invoice feed", e)

