<p align="center">
  <img src="https://cdn.twikey.com/img/logo.png" height="64"/>
</p>
<h1 align="center">Twikey API client for Python</h1>

Want to allow your customers to pay in the most convenient way, then Twikey is right what you need.

Recurring or occasional payments via (Recurring) Credit Card, SEPA Direct Debit or any other payment method by bringing 
your own payment service provider or by leveraging your bank contract.

Twikey offers a simple and safe multichannel solution to negotiate and collect recurring (or even occasional) payments.
Twikey has integrations with a lot of accounting and CRM packages. It is the first and only provider to operate on a
European level for Direct Debit and can work directly with all major Belgian and Dutch Banks. However you can use the
payment options of your favorite PSP to allow other customers to pay as well.

## Requirements ##

To use the Twikey API client, the following things are required:

+ Get yourself a [Twikey account](https://www.twikey.com).
+ Python >= 3.0
+ Up-to-date OpenSSL (or other SSL/TLS toolkit)

## Pip Installation ##

The easiest way to install the Twikey API client is 
with [pip](https://pip.pypa.io).

    $ pip install twikey-api-python

## How to create anything ##

The api works the same way regardless if you want to create a mandate, a transaction, an invoice or even a paylink.
the following steps should be implemented:

1. Use the Twikey API client to create or import your item.

2. Once available, our platform will send an asynchronous request to the configured webhook
   to allow the details to be retrieved. As there may be multiple items ready for you a "feed" endpoint is provided
   which acts like a queue that can be read until empty till the next time.

3. The customer returns, and should be satisfied to see that the action he took is completed.

Find our full documentation online on [api.twikey.com](https://api.twikey.com).

## Getting started ##

Initializing the Twikey API client using the Requests library. 
and configure your API key which you can find in the [Twikey merchant interface](https://www.twikey.com).

```python
import twikey

twikeyClient = twikey.TwikeyClient(APIKEY, "https://api.beta.twikey.com")
``` 

## Documents

Invite a customer to sign a SEPA mandate using a specific behaviour template (ct) that allows you to configure 
the behaviour or flow that the customer will experience. This 'ct' can be found in the template section of the settings.

```python
invite = twikeyClient.document.create({
   "ct": ct,
   "email": "info@twikey.com",
   "firstname": "Info",
   "lastname": "Twikey"
})
```

_After creation, the link available in invite['url'] can be used to redirect the customer into the signing flow or even 
send him a link through any other mechanism. Ideally you store the mandatenumber for future usage (eg. sending transactions)._


### Feed

Once signed, a webhook is sent (see below) after which you can fetch the detail through the document feed, which you can actually
think of as reading out a queue. Since it'll return you the changes since the last time you called it.

```python
import twikey

class MyDocumentFeed(twikey.DocumentFeed):
    def newDocument(self, doc):
        print("new ", doc["MndtId"])

    def updatedDocument(self, orinalDocNumber, doc, reason):
        print("update ", doc["MndtId"], "b/c", reason["Rsn"])

    def cancelDocument(self, docNumber, reason):
        print("cancelled ", docNumber, "b/c", reason["Rsn"])

twikeyClient.document.feed(MyDocumentFeed())
```

## Transactions

Send new transactions and act upon feedback from the bank.

```python
tx = twikeyClient.transaction.create({
   "mndtId" : "CORERECURRENTNL16318",
   "message" : "Test Message",
   "ref" : "Merchant Reference",
   "amount" : 10.00, 
   "place" : "Here"
})
```

### Feed

```python
import twikey

class MyFeed(twikey.TransactionFeed):
    def transaction(self, transaction):
        print("TX ", transaction.ref, transaction.state)

twikeyClient.transaction.feed(MyFeed())
```

## Webhook ##

When wants to inform you about new updates about documents or payments a `webhookUrl` specified in your api settings be called.  

```python
import Flask 
import twikey 

app = Flask(__name__)

@app.route('/webhook', methods=['GET'])
def webhook(request):
   payload = unquote(request.query_string)
   received_sign = request.headers.get('X-Signature')
   if not received_sign:
      return False
   if twikey.Webhook.verify_signature(payload,received_sign,APIKEY):
      # trigger feed fetching
      return 'Successfully', 200
   return 'Forbidden', 403

if __name__ == '__main__':
   #setup dev server
   app.debug = True
   app.run(host = "0.0.0.0",port=8000)
```

## API documentation ##

If you wish to learn more about our API, please visit the [Twikey Api Page](https://api.twikey.com).
API Documentation is available in English.

## Want to help us make our API client even better? ##

Want to help us make our API client even better? We
take [pull requests](https://github.com/twikey/twikey-api-python/pulls). 

## Support ##

Contact: [www.twikey.com](https://www.twikey.com)
