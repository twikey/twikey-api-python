import requests

from .model.transaction_request import NewTransactionRequest, StatusRequest, QueryTransactionsRequest, ActionRequest, \
    UpdateRequest, RefundRequest, RemoveTransactionRequest
from .model.transaction_response import Transaction, TransactionStatusResponse, RefundResponse


class TransactionService(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    def create(self, request: NewTransactionRequest) -> Transaction:
        """
        See https://www.twikey.com/api/#new-transaction
        :param data: parameters of the rest call as a struct
        :return: struct containing return value of the rest call
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
        Retrieve transaction status by ID, ref, or mandate ID.
        Args:
            request (TransactionStatusRequest): The query parameters.
        Returns:
            TransactionStatusResponse: List of transaction status entries.
        Raises:
            TwikeyError: On error responses.
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
        Perform a GET request to retrieve all created transactions starting from a specific transaction ID.
        Args:
            from_id (int): Starting transaction ID (required).
            mndt_id (str, optional): Optional mandate reference to filter results.
        Returns:
            dict: Contains 'Entries' and '_links' as returned by the API.
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
        See https://www.twikey.com/api/#new-transaction
        :param data: parameters of the rest call as a struct
        :return: struct containing return value of the rest call
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
        Updates an existing transaction by sending a PUT request.
        Parameters:
            data (dict): Must contain 'id'; may include 'amount', 'ref', 'message',
                         'place', or 'reqcolldt'
        Returns:
            None
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

    def refund(self, request: RefundRequest):
        """
        See https://www.twikey.com/api/#refund-a-transaction
        Creates a refund for a given transaction. If the beneficiary account does not exist yet,
        it will be registered to the customer using the mandate IBAN or the one provided.
        Parameters:
            data (dict): Must include 'id', 'message', and 'amount'. May include
                         'ref', 'place', 'iban', or 'bic'
        Returns:
            dict: Response payload containing refund entry details
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
        Removes a transaction that has not yet been sent to the bank.
        At least one of 'id' or 'ref' must be provided.
        Parameters:
            data (dict): Dictionary with 'id' and/or 'ref' to identify the transaction
        Returns:
            None: A successful deletion returns HTTP 204 with no content
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

    def feed(self, transaction_feed):
        """
        See https://www.twikey.com/api/#transaction-feed
        :param transaction_feed: instance of TransactionFeed to handle transaction updates
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
