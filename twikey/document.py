import requests


class Document(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    def create(self, data):
        url = self.client.instance_url("/invite")
        data = data or {}
        self.client.refreshTokenIfRequired()
        response = requests.post(url=url, data=data, headers=self.client.headers())
        if "ApiErrorCode" in response.headers:
            error = response.json()
            raise Exception("Error invite : %s" % error)
        return response.json()

    def feed(self, documentFeed):
        url = self.client.instance_url("/mandate")

        self.client.refreshTokenIfRequired()
        response = requests.get(url=url, headers=self.client.headers())
        response.raise_for_status()
        if "ApiErrorCode" in response.headers:
            error = response.json()
            raise Exception("Error feed : %s" % error)
        feedResponse = response.json()
        while len(feedResponse["Messages"]) > 0:
            for msg in feedResponse["Messages"]:
                if "AmdmntRsn" in msg:
                    documentFeed.updatedDocument(msg["Mndt"], msg["AmdmntRsn"])
                elif "CxlRsn" in msg:
                    documentFeed.cancelDocument(msg["OrgnlMndtId"], msg["CxlRsn"])
                else:
                    documentFeed.newDocument(msg["Mndt"])
            response = requests.get(url=url, headers=self.client.headers())
            if "ApiErrorCode" in response.headers:
                error = response.json()
                raise Exception(
                    "Error invite : %s - %s" % (error["code"], error["message"])
                )

            feedResponse = response.json()


class DocumentFeed:
    def newDocument(self, doc):
        pass

    def updatedDocument(self, doc, reason):
        pass

    def cancelDocument(self, docNumber, reason):
        pass
