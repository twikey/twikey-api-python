import requests


class Invoice(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    def create(self, data):
        url = self.client.instance_url("/invoice")
        data = data or {}
        self.client.refreshTokenIfRequired()
        response = requests.post(
            url=url, json=data, headers=self.client.headers("application/json")
        )
        response.raise_for_status()
        if "ApiErrorCode" in response.headers:
            error = response.json()
            raise Exception("Error creating : %s" % error)
        return response.json()

    def feed(self, invoiceFeed):
        url = self.client.instance_url("/invoice")

        self.client.refreshTokenIfRequired()
        response = requests.get(url=url, headers=self.client.headers())
        response.raise_for_status()
        if "ApiErrorCode" in response.headers:
            # print response.headers
            raise Exception(
                "Error feed : %s - %s"
                % (response.headers["ApiErrorCode"], response.headers["ApiError"])
            )
        feedResponse = response.json()
        while len(feedResponse) > 0:
            for msg in feedResponse:
                invoiceFeed.invoice(msg)
            response = requests.get(url=url, headers=self.client.headers())
            if "ApiErrorCode" in response.headers:
                error = response.json()
                raise Exception("Error feed : %s" % error)
            feedResponse = response.json()


class InvoiceFeed:
    def invoice(self, invoice):
        pass
