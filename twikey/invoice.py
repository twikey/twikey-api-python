import requests
import logging


class Invoice(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        self.logger = logging.getLogger(__name__)

    def create(self, data):
        url = self.client.instance_url("/invoice")
        data = data or {}
        self.client.refreshTokenIfRequired()
        headers = self.client.headers("application/json")
        response = requests.post(url=url, json=data, headers=headers)
        jsonResponse = response.json()
        if "ApiErrorCode" in response.headers:
            error = jsonResponse
            raise Exception("Error creating : %s" % error)
        self.logger.debug("Added invoice : %s" % jsonResponse["url"])
        return jsonResponse

    def feed(self, invoiceFeed):
        url = self.client.instance_url(
            "/invoice?include=customer&include=meta&include=lastpayment"
        )

        self.client.refreshTokenIfRequired()
        response = requests.get(url=url, headers=self.client.headers())
        response.raise_for_status()
        if "ApiErrorCode" in response.headers:
            raise Exception(
                "Error feed : %s - %s"
                % (response.headers["ApiErrorCode"], response.headers["ApiError"])
            )
        feedResponse = response.json()
        while len(feedResponse["Invoices"]) > 0:
            self.logger.debug("Feed handling : %d" % (len(feedResponse["Invoices"])))
            for invoice in feedResponse["Invoices"]:
                self.logger.debug("Feed handling : %s" % invoice)
                invoiceFeed.invoice(invoice)
            response = requests.get(url=url, headers=self.client.headers())
            if "ApiErrorCode" in response.headers:
                error = response.json()
                raise Exception("Error feed : %s" % error)
            feedResponse = response.json()

    def geturl(self, invoice_id):
        return "%s/%s/%s" % (
            self.client.api_base.replace("api", "app"),
            self.client.merchant_id,
            invoice_id,
        )


class InvoiceFeed:
    def invoice(self, invoice):
        pass
