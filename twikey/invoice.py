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
        Retrieves the details of a specific invoice by ID or number,
        optionally including lastpayment, meta, or customer data.
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
        Performs an action on a specific invoice.

        Args:
            request (InvoiceActionRequest): The action request with invoice ID and type.

        Supported types:
            'email', 'sms', 'reminder', 'smsreminder',
            'letter', 'letterWithInvoice', 'invoice',
            'reoffer', 'peppol'
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
        Uploads a UBL invoice (XML) to Twikey.

        Args:
            request (UblUploadRequest): The UBL upload request containing the XML payload
                and optional headers like X-MANUAL and X-INVOICE-ID.

        Returns:
            UblUploadResponse: Parsed invoice response object.

        Raises:
            TwikeyError: If Twikey returns an error or network fails.
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

    def delete(self, inoviceId: str):
        url = self.client.instance_url("/invoice/" + inoviceId)
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

    def bulk_details(self, batch_id: str):
        """
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

    def feed(self, invoice_feed:InvoiceFeed, start_position=False, *includes):
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

    def geturl(self, invoice_id):
        if ".beta." in self.client.api_base:
            return "https://app.beta.twikey.com/%s/%s" % (
                self.client.merchant_id,
                invoice_id,
            )
        return "https://app.twikey.com/%s/%s" % (
            self.client.merchant_id,
            invoice_id,
        )
