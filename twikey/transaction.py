import requests

from .model.transaction_request import NewTransactionRequest, StatusRequest, QueryTransactionsRequest, ActionRequest, \
    UpdateRequest, RefundRequest, RemoveTransactionRequest
from .model.transaction_response import Transaction, TransactionStatusResponse, RefundResponse, TransactionFeed


class TransactionService(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    def create(self, request: NewTransactionRequest) -> Transaction:
        """
        See https://www.twikey.com/api/#new-transaction

        Create a new transaction via a POST request to the API.

        This method sends the provided request payload to the corresponding endpoint
        and parses the JSON response into a response model. Typically used to initiate
        actions like inviting a customer, creating a mandate, or generating a payment link.
        Raises an error if the API response contains an error code or the request fails.

        Args:
            request (NewTransactionRequest): An object representing the payload to send.

        Returns:
            Transaction: A structured response object representing the server’s reply.

        Raises:
            TwikeyAPIError: If the API returns an error or the request fails.
        """

        url = self.client.instance_url("/transaction")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url,
                data=data,
                headers=self.client.headers(),
                timeout=15,
            )
            response.raise_for_status()
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Create transaction", response)
            entries_ = response.json()["Entries"]
            if len(entries_) > 0:
                first_transaction = entries_[0]
                return Transaction(first_transaction)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Create transaction", e)

    def status_details(self, request: StatusRequest) -> TransactionStatusResponse:
        """
        See https://www.twikey.com/api/#transaction-status

        Retrieves transaction status by ID, ref, or mandate ID.

        This method queries the Twikey API for the latest details related to the mandate, invoice, etc. for the
        provided identifier. Typically used for querying status based on ID, reference, or mandate.

        Args:
            request (StatusRequest): An object representing information for identifying the transaction.

        Returns:
            TransactionStatusResponse: A structured response object representing the server’s reply.

        Raises:
            TwikeyError: If the API call fails or the identifier is invalid.
        """

        params = request.to_params()
        url = self.client.instance_url("/transaction/detail")
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers("application/json")
            response = requests.get(url=url, params=params, headers=headers, timeout=15)
            if response.status_code != 200:
                raise self.client.raise_error("Transaction detail", response)
            return TransactionStatusResponse(response.json())
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Transaction detail", e)

    def query(self, request: QueryTransactionsRequest) -> TransactionStatusResponse:
        """
        See https://www.twikey.com/api/#query-transactions

        retrieve all created transactions starting from a specific transaction ID.

        This endpoint allows you to search for transactions based on specific identifiers.
        The result contains a list of transactions that match the provided parameters.

        Args:
            request (QueryTransactionsRequest): an object that represents the payload of the request

        Returns:
            TransactionStatusResponse: A structured response object representing the server’s reply.

        Raises:
            TwikeyError: If the request fails or the API returns an error.
        """

        data = request.to_request()
        url = self.client.instance_url(f"/transaction/query?fromId={data.get('fromId')}")
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers()
            response = requests.get(url=url, headers=headers, timeout=15,)
            if response.status_code != 200:
                raise self.client.raise_error("Transaction detail", response)
            return TransactionStatusResponse(response.json())
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Transaction detail", e)

    def action(self, request: ActionRequest):
        """
        See https://www.twikey.com/api/#action-on-transaction

        Trigger a specific action on an existing transaction.

        This endpoint allows initiating predefined actions related to a transaction, such as reoffer
        or archive the transaction. The action type must be explicitly provided in the request.

        Args:
            request (ActionRequest): The action request with transaction ID and action.

        Returns:
            None

        Raises:
            TwikeyError: If the API returns an error or the request fails.
        """

        url = self.client.instance_url("/transaction/action")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url,
                data=data,
                headers=self.client.headers(),
                timeout=15,
            )
            response.raise_for_status()
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Action transaction", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Action transaction", e)

    def update(self, request: UpdateRequest):
        """
        See https://www.twikey.com/api/#update-transaction

        Send a PUT request to update existing transaction details.

        This endpoint allows modifying transaction information such as message or linked references.
        Only provide parameters for fields you wish to update.
        Some fields may have special behavior or limitations depending on the object state.

        Args:
            request (UpdateRequest): A model representing the payload to send.

        Returns:
            None

        Raises:
            TwikeyError: If the API returns an error or the request fails.
        """

        data = request.to_request()
        url = self.client.instance_url("/transaction")
        try:
            self.client.refresh_token_if_required()
            response = requests.put(url=url, data=data, headers=self.client.headers(), timeout=15)
            response.raise_for_status()
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Update transaction", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Update transaction", e)

    def refund(self, request: RefundRequest) -> RefundResponse:
        """
        See https://www.twikey.com/api/#refund-a-transaction

        Creates a refund for a given transaction via a POST request to the API.

        If the beneficiary account does not exist yet,
        it will be registered to the customer using the mandate IBAN or the one provided.

        Args:
            request (RefundRequest): Must include 'id', 'message', and 'amount'. May include
                         'ref', 'place', 'iban', or 'bic'. An object that represents the payload of the request.

        Returns:
            RefundResponse: Response payload containing refund entry details

        Raises:
            TwikeyError: If the request fails or the API returns an error.
        """

        data = request.to_request()
        url = self.client.instance_url("/transaction/refund")
        try:
            self.client.refresh_token_if_required()
            response = requests.post(url=url, data=data, headers=self.client.headers(), timeout=15)
            response.raise_for_status()
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Update transaction", response)
            entries_ = response.json()["Entries"]
            if len(entries_) > 0:
                first_transaction = entries_[0]
                return RefundResponse(first_transaction)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Update transaction", e)

    def remove(self, request: RemoveTransactionRequest):
        """
        See https://www.twikey.com/api/#remove-a-transaction

        Sends a DELETE request to remove a transaction that has not yet been sent to the bank on the Twikey API.

        This method allows the creditor to cancel/delete a resource by providing the unique ID.
        Typically used to delete/cancel object like an agreement, an invoice, or a payment link.
        Raises an error if the API response contains an error code or the request fails.

        Args:
            request (RemoveTransactionRequest): An object representing information for identifying the transaction.

        Returns:
            None

        Raises:
            TwikeyAPIError: If the request fails or the response contains an API error code.
        """

        data = request.to_request()
        url = self.client.instance_url(f"/transaction?id={data.get('id')}")
        try:
            self.client.refresh_token_if_required()
            response = requests.delete(url=url, headers=self.client.headers(), timeout=15)
            response.raise_for_status()
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Update transaction", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Update transaction", e)

    def feed(self, transaction_feed: TransactionFeed):
        """
        See https://www.twikey.com/api/#transaction-feed

        Fetches the latest transaction feed including new, updated, or cancelled transactions.

        This method retrieves events from Twikey since the last sync. These events may concern
        mandates, invoices, payment link, etc. It's typically
        used to synchronize your CRM or ERP system with the current state on the Twikey
        platform. Can be triggered periodically or via webhook.

        Args:
            transaction_feed (TransactionFeed): Custom handler class with methods for processing
                new, updated, or cancelled transaction events.

        Returns:
            None

        Raises:
            Exception: If the request to the feed endpoint fails or response is invalid.
        """

        url = self.client.instance_url("/transaction")
        try:
            self.client.refresh_token_if_required()
            response = requests.get(
                url=url,
                headers=self.client.headers(),
                timeout=15,
            )
            response.raise_for_status()
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Feed transaction", response)
            feed_response = response.json()
            while len(feed_response["Entries"]) > 0:
                for msg in feed_response["Entries"]:
                    transaction_feed.transaction(Transaction(msg))
                response = requests.get(
                    url=url,
                    headers=self.client.headers(),
                    timeout=15,
                )
                if "ApiErrorCode" in response.headers:
                    raise self.client.raise_error("Feed transaction", response)
                feed_response = response.json()
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Feed transaction", e)

    def batch_send(self, ct, colltndt=False):
        """
        See https://www.twikey.com/api/#execute-collection
        :param ct	Contract template for which to do the collection	Yes	number
        :param colltndt	Collection date (default=earliest batch) [*1]	No	string
        :return: struct containing identifier of the batch
        """
        url = self.client.instance_url("/collect")
        data = {"ct": ct}
        if colltndt:
            data["colltndt"] = colltndt
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url,
                data=data,
                headers=self.client.headers(),
                timeout=60,  # might be large batches
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Send batch", response)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Send batch", e)

    def batch_import(self, ct, pain008_xml):
        """
        See https://www.twikey.com/api/#import-collection
        :param pain008_xml the pain008 file
        """
        url = self.client.instance_url(f"/collect/import?ct={ct}")
        try:
            self.client.refresh_token_if_required()
            with open(pain008_xml, "rb") as file:
                response = requests.post(
                    url=url,
                    data=file,
                    headers=self.client.headers("text/xml"),
                    timeout=60,  # might be large batches
                )
                if "ApiErrorCode" in response.headers:
                    raise self.client.raise_error("Import batch", response)
                return response.json()
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Import batch", e)

    def reporting_import(self, reporting_content):
        """
        :param reporting_content content of the coda/camt/mt940 file
        """
        url = self.client.instance_url("/reporting")
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url,
                data=reporting_content,
                headers=self.client.headers(),
                timeout=60,  # might be large batches
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Import reporting", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Import reporting", e)
