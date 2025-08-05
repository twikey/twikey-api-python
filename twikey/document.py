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
            return [QueryMandateResponse(contract) for contract in contracts_data]
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("query", e)

    def action(self, request: MandateActionRequest):
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

    def update(self, request: UpdateMandateRequest):
        url = self.client.instance_url("/mandate/update")
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

    def update_customer(self, customer_id, data):
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