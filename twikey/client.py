import binascii
import hmac
import struct
import time
import datetime

import requests

from .document import Document
from .transaction import Transaction
from .paylink import Paylink
from .invoice import Invoice
import logging


class TwikeyClient(object):
    lastLogin = None
    api_key = None
    api_token = None  # Once authenticated
    private_key = None
    vendorPrefix = "own"
    api_base = "https://api.twikey.com"

    document = None
    transaction = None
    paylink = None
    invoice = None

    def __init__(
        self,
        api_key,
        base_url="https://api.twikey.com",
        user_agent="twikey-python/v0.1.0",
    ) -> None:
        self.user_agent = user_agent
        self.api_key = api_key
        self.api_base = base_url
        self.document = Document(self)
        self.transaction = Transaction(self)
        self.paylink = Paylink(self)
        self.invoice = Invoice(self)
        self.logger = logging.getLogger(__name__)

    def instance_url(self, url=""):
        return "%s/%s%s" % (self.api_base, "creditor", url)

    def get_totp(self, vendorPrefix, secret):
        """Return the Time-Based One-Time Password for the current time, and the provided secret (base32 encoded)"""
        secret = bytearray(vendorPrefix) + binascii.unhexlify(secret)
        counter = struct.pack(">Q", int(time.time()) // 30)

        import hashlib

        hash = hmac.new(secret, counter, hashlib.sha256).digest()
        offset = ord(hash[19]) & 0xF

        return (
            struct.unpack(">I", hash[offset : offset + 4])[0] & 0x7FFFFFFF
        ) % 100000000

    def refreshTokenIfRequired(self):
        now = datetime.datetime.now()
        if self.lastLogin == None or (now - self.lastLogin).seconds > 23 * 3600:
            payload = {"apiToken": self.api_key}
            if self.private_key:
                payload["otp"] = self.get_totp(self.vendorPrefix, self.private_key)

            self.logger.debug("Authenticating with", self.api_base, payload)
            response = requests.post(
                self.instance_url(),
                data=payload,
                headers={"User-Agent": self.user_agent},
            )
            if "ApiErrorCode" in response.headers:
                # print response.headers
                raise Exception(
                    "Error authenticating : %s - %s"
                    % (response.headers["ApiErrorCode"], response.headers["ApiError"])
                )

            self.api_token = response.headers["Authorization"]
            self.lastLogin = datetime.datetime.now()

    def headers(self, contentType="application/x-www-form-urlencoded"):
        return {
            "Content-type": contentType,
            "Authorization": self.api_token,
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }

    def logout(self):
        response = requests.get(
            self.instance_url(), headers={"User-Agent": self.user_agent}
        )
        if "ApiErrorCode" in response.headers:
            # print response.headers
            raise Exception(
                "Error logging out : %s - %s"
                % (response.headers["ApiErrorCode"], response.headers["ApiError"])
            )

        self.api_token = None
        self.lastLogin = None
