import logging

import requests
from datetime import datetime

from .model.document_request import InviteRequest, SignRequest, FetchMandateRequest, QueryMandateRequest, \
    MandateActionRequest, UpdateMandateRequest, PdfUploadRequest

from .model.document_response import InviteResponse, SignResponse, Document, QueryMandateResponse, PdfResponse, \
    CustomerAccessResponse, DocumentFeed


class DocumentService(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        self.logger = logging.getLogger(__name__)

    def create(self, request: InviteRequest) -> InviteResponse:
        """
        See https://www.twikey.com/api/#invite-a-customer

        Create a new mandate (certain period to be signed in) via a POST request to the API.

        This method sends the provided request payload to the corresponding endpoint
        and parses the JSON response into a response model. Typically used to initiate
        actions like inviting a customer, creating a mandate, or generating a payment link.
        Raises an error if the API response contains an error code or the request fails.

        Args:
            request (InviteRequest): An object representing the payload to send.

        Returns:
            InviteResponse: A structured response object representing the server’s reply.

        Raises:
            TwikeyAPIError: If the API returns an error or the request fails.
        """

        url = self.client.instance_url("/invite")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url, data=data, headers=self.client.headers(), timeout=15
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Invite", response)
            json_response = response.json()
            # self.logger.debug("Added new mandate : %s" % json_response["mndtId"])
            return InviteResponse(**json_response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Invite", e)

    def sign(self, request: SignRequest) -> SignResponse:  # pylint: disable=W8106
        """
        See https://www.twikey.com/api/#sign-a-mandate

        Create a new mandate (ready to be signed) via a POST request to the API.

        This method sends the provided request payload to the corresponding endpoint
        and parses the JSON response into a response model. Typically used to initiate
        actions like inviting a customer, creating a mandate, or generating a payment link.
        Raises an error if the API response contains an error code or the request fails.

        Args:
            request (SignRequest): An object representing the payload to send.

        Returns:
            SignResponse: A structured response object representing the server’s reply.

        Raises:
            TwikeyAPIError: If the API returns an error or the request fails.
        """


        url = self.client.instance_url("/sign")
        data = request.to_request()
        if not request.method:
            raise self.client.raise_error("Missing method")
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url, data=data, headers=self.client.headers(), timeout=15
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Sign", response)
            json_response = response.json()
            self.logger.debug("Added new mandate : %s" % json_response["MndtId"])
            return SignResponse(**json_response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Sign", e)

    def fetch(self, request: FetchMandateRequest) -> Document:
        """
        See https://www.twikey.com/api/#fetch-mandate-details

        Retrieves the details of a specific mandate by ID

        This method queries the Twikey API for the latest details related to the mandate, invoice, etc. for the
        provided identifier. Typically used for querying status based on ID, reference, or mandate.

        Args:
            request (FetchMandateRequest): An object representing information for identifying the mandate.

        Returns:
            Document: A structured response object representing the server’s reply.

        Raises:
            TwikeyError: If the API call fails or the identifier is invalid.
        """

        data = request.to_request()
        url = self.client.instance_url("/mandate/detail")
        try:
            self.client.refresh_token_if_required()
            response = requests.get(
                url=url, params=data, headers=self.client.headers(), timeout=15
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("detail", response)
            json_response = response.json()
            json_response["headers"] = response.headers
            self.logger.debug("Mandate details : %s" % json_response)
            return Document(mandate=json_response.get("Mndt"), headers=json_response.get("headers"))
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("detail", e)

    def query(self, request: QueryMandateRequest) -> list:
        """
        See https://www.twikey.com/api/#query-mandate

        Retrieve contract details by IBAN, customer number, email, or a combination of query parameters.

        This endpoint allows you to search for mandates based on specific identifiers.
        The result contains a list of contracts (mandates) that match the provided parameters.

        Args:
            request (QueryMandateRequest): Query parameters like 'iban', 'customerNumber', 'email', 'state' or 'page'.
                            At least one of 'iban', 'customerNumber' or 'email' is required.

        Returns:
            list[QueryMandateResponse]: A list of mandate details that match the query.

        Raises:
            TwikeyError: If the request fails or the API returns an error.
        """

        data = request.to_request()
        url = self.client.instance_url("/mandate/query")
        try:
            self.client.refresh_token_if_required()
            response = requests.get(
                url=url,
                params=data,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("query", response)
            json_response = response.json()
            contracts_data = json_response.get("Contracts", [])
            self.logger.debug("Mandate query result: %s" % json_response)
            return QueryMandateResponse(contracts_data)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("query", e)

    def action(self, request: MandateActionRequest):
        """
        See https://www.twikey.com/api/#mandate-actions

        Trigger a specific action on an existing mandate.

        This endpoint allows initiating predefined actions related to a mandate, such as sending
        an invitation or reminder, or toggling B2B validation behavior. The action type must
        be explicitly provided in the request.

        Args:
            request (MandateActionRequest): Dictionary containing the action type and any optional parameters.
                            Required fields include:
                                - mndtId (str): The unique identifier of the mandate.
                                - type (str): The action to perform (e.g., invite, reminder).

        Returns:
            None

        Raises:
            TwikeyError: If the API returns an error or the request fails.
        """

        data = request.to_request()
        url = self.client.instance_url(f"/mandate/{data.get('mndtId')}/action")
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url, data=data, headers=self.client.headers(), timeout=15
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("action", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("detail", e)

    def update(self, mandate_number: str, request: UpdateMandateRequest):
        """
        See https://www.twikey.com/api/#update-mandate-details

        Send a POST request to update existing mandate details.

        This endpoint allows modifying mandate information such as customer data,
        mandate configuration, or linked references. Only provide parameters for fields you
        wish to update. Some fields may have special behavior or limitations depending on the object state.

        Args:
            request (UpdateMandateRequest): An object representing the payload to send.

        Returns:
            None

        Raises:
            TwikeyError: If the API returns an error or the request fails.
        """

        url = self.client.instance_url(f"/mandate/update?mndtId={mandate_number}")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url, data=data, headers=self.client.headers(), timeout=15
            )
            self.logger.debug("Updated mandate : {} response={}".format(data, response))
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Update", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Update", e)

    def cancel(self, mandate_number: str, reason: str):
        """
        See https://www.twikey.com/api/#cancel-agreements

        Sends a DELETE request to cancel a mandate on the Twikey API.

        This method allows the creditor to cancel/delete a resource by providing the unique
        ID and a reason for cancellation. This ensures Twikey’s records are
        updated and, if applicable, forwards the cancellation to the debtor's bank.
        Cancellation can originate from the creditor, the creditor’s bank, or the debtor’s bank.

        Args:
            mandate_number (str): The unique identifier of the mandate to cancel (mndtId).
            reason (str): The reason for cancelling the mandate. Can be a custom message or an R-message code.
            notify (bool): When set to true, the customer will be notified by email. (optional)

        Returns:
            None

        Raises:
            TwikeyAPIError: If the request fails or the response contains an API error code.
        """

        url = self.client.instance_url(f"/mandate?mndtId={mandate_number}&rsn={reason}")
        try:
            self.client.refresh_token_if_required()
            response = requests.delete(
                url=url, headers=self.client.headers(), timeout=15
            )
            self.logger.debug(
                "Cancel mandate : %s status=%d" % (mandate_number, response.status_code)
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Cancel", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Cancel", e)

    def feed(self, document_feed: DocumentFeed, start_position=False):
        """
        See https://www.twikey.com/api/#mandate-feed

        Fetches the latest mandate feed including new, updated, or cancelled mandates.

        This method retrieves events from Twikey since the last sync. These events may concern
        mandates, invoices, payment link, etc. It's typically
        used to synchronize your CRM or ERP system with the current state on the Twikey
        platform. Can be triggered periodically or via webhook.

        Args:
            document_feed (DocumentFeed): Custom handler class with methods for processing
                new, updated, or cancelled mandate events.

        Returns:
            None

        Raises:
            Exception: If the request to the feed endpoint fails or response is invalid.
        """

        url = self.client.instance_url(
            "/mandate?include=id&include=mandate&include=person"
        )
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
                raise self.client.raise_error("Feed", response)
            feed_response = response.json()
            while len(feed_response["Messages"]) > 0:
                self.logger.debug(
                    "Feed handling : %d from %s till %s"
                    % (
                        len(feed_response["Messages"]),
                        start_position,
                        response.headers["X-LAST"],
                    )
                )
                document_feed.start(
                    response.headers["X-LAST"], len(feed_response["Messages"])
                )
                error = False
                for msg in feed_response["Messages"]:
                    if "AmdmntRsn" in msg:
                        mndt_id_ = msg["OrgnlMndtId"]
                        self.logger.debug("Feed update : %s" % mndt_id_)
                        mndt_ = msg["Mndt"]
                        amdmnt_rsn_ = msg["AmdmntRsn"]
                        rsn_ = amdmnt_rsn_.get("Rsn")
                        author_ = amdmnt_rsn_["Orgtr"]["CtctDtls"]["EmailAdr"]
                        at_ = msg["EvtTime"]
                        if at_.endswith("Z"):
                            at_ = at_.replace("Z", "+00:00")
                        error = document_feed.updated_document(mndt_id_, Document(mandate=mndt_), rsn_, author_, datetime.fromisoformat(at_))
                    elif "CxlRsn" in msg:
                        mndt_ = msg["OrgnlMndtId"]
                        cxl_rsn_ = msg["CxlRsn"]
                        rsn_ = cxl_rsn_.get("Rsn")
                        author_ = cxl_rsn_["Orgtr"]["CtctDtls"]["EmailAdr"]
                        at_ = msg["EvtTime"]
                        if at_.endswith("Z"):
                            at_ = at_.replace("Z", "+00:00")
                        self.logger.debug("Feed cancel : %s" % mndt_)
                        error = document_feed.cancelled_document(mndt_, rsn_, author_, datetime.fromisoformat(at_))
                    else:
                        mndt_ = msg["Mndt"]
                        at_ = msg["EvtTime"]
                        if at_.endswith("Z"):
                            at_ = at_.replace("Z", "+00:00")
                        self.logger.debug("Feed create : %s" % mndt_)
                        error = document_feed.new_document(Document(mandate=mndt_), datetime.fromisoformat(at_))
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
                    raise self.client.raise_error("Feed", response)
                feed_response = response.json()
            self.logger.debug("Done handing mandate feed")
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Mandate feed", e)

    def upload_pdf(self, request: PdfUploadRequest):
        """
        See https://www.twikey.com/api/#upload-pdf

        add a new mandate via a pdf during a POST request to the API.

        Args:
            request (PdfUploadRequest): object representing the payload for the request containing the file

        Returns:
            None

        Raises:
            Exception: If the request to the feed endpoint fails or response is invalid.
        """

        url = self.client.instance_url(
            f"/mandate/pdf?mndtId={request.mndt_id}&bankSignature={request.bank_signature}")
        try:
            self.client.refresh_token_if_required()
            with open(request.pdf_path, "rb") as file:
                response = requests.post(
                    url=url, data=file, headers=self.client.headers('application/pdf'), timeout=15
                )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("pdf", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("detail", e)

    def retrieve_pdf(self, mndt_id: str) -> PdfResponse:
        """
        See https://www.twikey.com/api/#retrieve-pdf

        retrieve the pdf of a mandate via during GET request to the API.

        Args:
            mndt_id (str): A unique identifier for a mandate

        Returns:
            PdfResponse: A structured response object representing the server’s reply.

        Raises:
            Exception: If the request to the feed endpoint fails or response is invalid.
        """

        url = self.client.instance_url(f"/mandate/pdf?mndtId={mndt_id}")
        try:
            self.client.refresh_token_if_required()
            response = requests.get(
                url=url, headers=self.client.headers(), timeout=15
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("pdf", response)
            filename = None
            if "Content-Disposition" in response.headers:
                disposition = response.headers["Content-Disposition"]
                parts = disposition.split("=")
                if len(parts) == 2:
                    filename = parts[1].strip().strip('"')
            return PdfResponse(content=response.content, filename=filename)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("detail", e)

    def update_customer(self, customer_id: str, data):
        """
        See https://www.twikey.com/api/#update-a-customer

        Send a POST request to update existing customer details.

        This endpoint allows modifying customer information such as customer data or linked references.
        Only provide parameters for fields you wish to update.
        Some fields may have special behavior or limitations depending on the object state.

        Args:
            customer_id (str): A unique identifier for a customer.

        Returns:
            None

        Raises:
            TwikeyError: If the API returns an error or the request fails.
        """

        url = self.client.instance_url("/customer/" + str(customer_id))
        try:
            self.client.refresh_token_if_required()
            response = requests.patch(
                url=url, params=data, headers=self.client.headers(), timeout=15
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Cancel", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Update customer", e)

    def customer_access(self, mndt_id: str) -> CustomerAccessResponse:
        """
        See https://www.twikey.com/api/#customer-access

        Create a new customer access link via a POST request to the API.

        Args:
            mndt_id (str): An object representing the payload to send.

        Returns:
            CustomerAccessResponse: A structured response object representing the server’s reply.

        Raises:
            TwikeyAPIError: If the API returns an error or the request fails.
        """

        url = self.client.instance_url("/customeraccess")
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url, data={"mndtId": mndt_id}, headers=self.client.headers(), timeout=15
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Cancel", response)
            return CustomerAccessResponse(**response.json())
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("customer access", e)