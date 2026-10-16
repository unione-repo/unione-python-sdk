# Email

[Back to the list of sections](../README.md)

This group of methods is related with email sending.

`unione.api.email.EmailApi`, `client.email`

| Method | Endpoint | Description |
|---|---|---|
| [`send`](#send) | `POST /email/send.json` | Sends an email or a bunch of emails |
| [`subscribe`](#subscribe) | `POST /email/subscribe.json` | Sends an email with (re)subscribe link. |

## send

`POST /email/send.json` · [Documentation](https://docs.unione.io/en/web-api-ref#email-send)

Sends an email or a bunch of emails

While sending you can provide substitutions (merge tags), use a template, turn on read or click tracking, etc.

Restrictions:
* maximum request size is 10 MB
* maximum number of recipients is 500
* The symbol '/' is not allowed in attachment names

If the list of recipients contains invalid, non-existent, duplicate, or unsubscribed emails, those emails will be returned in the output parameter failed_emails, and the email will be sent to all other valid emails addresses. If all the emails addresses fall into failed_emails, sending will not be carried out and API error 204 will be returned.

### Request: `EmailSendRequest`

| Field | Type | Required | Description |
|---|---|---|---|
| `message` | `MessageObject` | yes | Object containing all message properties. |

### Response: `EmailSendResponse`

| Field | Type | Description |
|---|---|---|
| `status` | `str` | "success" string (`success`) |
| `job_id` | `str` | Job identifier, might be useful for investigating errors. |
| `emails` | `List[str]` | Array of recipients emails successfully accepted for sending. |
| `failed_emails` | `Dict[str, str]` | Object with emails rejected for sending as property names and their statuses as property values, e.g.: {"email1@gmail.com": "temporary_unavailable"}. Possible statuses:<br><br>- __unsubscribed__ - specified email is unsubscribed;<br>- __invalid__ - the email does not exist or has been entered incorrectly;<br>- __duplicate__ - the email already exists in the request, email duplicating is prevented;<br>- __temporary_unavailable__ - the email address is unavailable. This means that over the next three days sending to this address will return an error. Email may be temporarily unavailable due to several reasons, e.g.:<br><br>- a previous email has been rejected by the recipient's server for spam;<br>- the recipient's mailbox is full or is not used;<br>- recipient's domain does not accept mail;<br>- sending server was rejected due to blacklisting;<br><br>- __permanent_unavailable__ - the email address is permanently unavailable or unsubscribed globally.<br>- __complained__ -  the recipient reported spam in the previous emails;<br>- __blocked__ -  sending to the email is prohibited by administration of UniOne.<br>We may added new statuses in the future. |

### Example

```python
import unione
from unione.api.email import EmailSendRequest, MessageObject, MessageObjectRecipientsItem
from unione.common import TemplateEngine, BodyObject

client = unione.client("YOUR_API_KEY")

response = client.email.send(EmailSendRequest(
    message=MessageObject(
        recipients=[
            MessageObjectRecipientsItem(
                email="user@example.com",
                substitutions={
                    "CustomerId": "12452",
                    "to_name": "John Smith",
                },
                metadata={
                    "campaign_id": "c77f4f4e-3561-49f7-9f07-c35be01b4f43",
                    "customer_hash": "b253ac7",
                },
            ),
        ],
        template_id="00000000-0000-0000-0000-000000000000",
        global_language="en",
        template_engine=TemplateEngine.VELOCITY,
        body=BodyObject(
            html="<b>Hello, {{to_name}}</b>",
            plaintext="Hello, {{to_name}}",
            amp="<!doctype html><html amp4email><head> <meta charset=\"utf-8\"><script async src=\"https://cdn.ampproject.org/v0.js\"></script> <style amp4email-boilerplate>body{visibility:hidden}</style></head><body> Hello, AMP4EMAIL world.</body></html>",
        ),
        subject="UniOne test email ",
        from_email="email@example.com",
        from_name="John Smith",
        reply_to="email@example.com",
        reply_to_name="John Smith",
        idempotence_key="SG1VsbG68sIH2dvc5mx890kIQ",
    ),
))
print(response.job_id)
```

## subscribe

`POST /email/subscribe.json` · [Documentation](https://docs.unione.io/en/web-api-ref#email-subscribe)

Sends an email with (re)subscribe link.

This method allows subscription renewal by a former subscriber who has previously unsubscribed, or who is blocked because of complaints. This method sends an email with a new subscription link to a former subscriber. Once the recipient clicks the link, their subscription status is restored.
There is a default restriction that limits this method to being used once a day. If you need to resubscribe more often, please ask support about it.

### Request: `EmailSubscribeRequest`

| Field | Type | Required | Description |
|---|---|---|---|
| `from_email` | `str` | yes | Sender’s email on a confirmed domain. (Field alias "email_address_from" is supported, too). |
| `from_name` | `str` | yes | Sender’s name. (Field alias "name_from" is supported, too). |
| `to_email` | `str` | yes | Recipient’s email. (Field alias "email_address_to" is supported, too). |

### Response: `SuccessResponse`

| Field | Type | Description |
|---|---|---|
| `status` | `str` | "success" string (`success`) |

### Example

```python
import unione
from unione.api.email import EmailSubscribeRequest

client = unione.client("YOUR_API_KEY")

response = client.email.subscribe(EmailSubscribeRequest(
    from_email="email@example.com",
    from_name="Example",
    to_email="email@example.com",
))
```
