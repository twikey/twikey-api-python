import requests
import logging


class Document(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        self.logger = logging.getLogger(__name__)

    def create(self, data):
        url = self.client.instance_url("/invite")
        data = data or {}
        self.client.refreshTokenIfRequired()
        response = requests.post(url=url, data=data, headers=self.client.headers())
        json_response = response.json()
        if "ApiErrorCode" in response.headers:
            error = json_response
            raise Exception("Error invite : %s" % error)
        self.logger.debug("Added new mandate : %s" % json_response["mndtId"])
        return json_response

    def update(self, data):
        url = self.client.instance_url("/mandate/update")
        data = data or {}
        self.client.refreshTokenIfRequired()
        response = requests.post(url=url, data=data, headers=self.client.headers())
        self.logger.debug(
            "Updated mandate : %s status=%d" % (data.mndtId, response.status_code)
        )
        if "ApiErrorCode" in response.headers:
            error = response.json()
            raise Exception("Error invite : %s" % error)

    def cancel(self, mandate_number, reason):
        url = self.client.instance_url(
            "/mandate?mndtId=" + mandate_number + "&rsn=" + reason
        )
        self.client.refreshTokenIfRequired()
        response = requests.delete(url=url, headers=self.client.headers())
        self.logger.debug(
            "Updated mandate : %s status=%d" % (mandate_number, response.status_code)
        )
        if "ApiErrorCode" in response.headers:
            error = response.json()
            raise Exception("Error invite : %s" % error)

    def feed(self, document_feed):
        url = self.client.instance_url("/mandate")

        self.client.refreshTokenIfRequired()
        response = requests.get(url=url, headers=self.client.headers())
        response.raise_for_status()
        if "ApiErrorCode" in response.headers:
            error = response.json()
            raise Exception("Error feed : %s" % error)
        feed_response = response.json()
        while len(feed_response["Messages"]) > 0:
            self.logger.debug("Feed handling : %d" % (len(feed_response["Messages"])))
            for msg in feed_response["Messages"]:
                if "AmdmntRsn" in msg:
                    mndt_id_ = msg["OrgnlMndtId"]
                    self.logger.debug("Feed update : %s" % mndt_id_)
                    mndt_ = msg["Mndt"]
                    rsn_ = msg["AmdmntRsn"]
                    document_feed.updatedDocument(mndt_id_, mndt_, rsn_, msg["EvtTime"])
                elif "CxlRsn" in msg:
                    self.logger.debug("Feed cancel : %s" % (msg["OrgnlMndtId"]))
                    document_feed.cancelDocument(
                        msg["OrgnlMndtId"], msg["CxlRsn"], msg["EvtTime"]
                    )
                else:
                    self.logger.debug("Feed create : %s" % (msg["Mndt"]))
                    document_feed.newDocument(msg["Mndt"], msg["EvtTime"])
            response = requests.get(url=url, headers=self.client.headers())
            if "ApiErrorCode" in response.headers:
                error = response.json()
                raise Exception(
                    "Error invite : %s - %s" % (error["code"], error["message"])
                )
            feed_response = response.json()


class DocumentFeed:
    def newDocument(self, doc, evt_time):
        pass

    def updatedDocument(self, original_mandate_number, doc, reason, evt_time):
        pass

    def cancelDocument(self, doc_number, reason, evt_time):
        pass
