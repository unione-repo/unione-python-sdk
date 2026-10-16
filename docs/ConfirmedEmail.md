# ConfirmedEmail

[Back to the list of sections](../README.md)

Manage email addresses confirmed for sandbox-domain sending. These methods are available only with a main account API key.

`unione.api.confirmed_email.ConfirmedEmailApi`, `client.confirmed_email`

| Method | Endpoint | Description |
|---|---|---|
| [`create`](#create) | `POST /confirmed-email/create.json` | Adds an email address and sends a confirmation link. |
| [`list`](#list) | `POST /confirmed-email/list.json` | Lists confirmed and unconfirmed email addresses for the account. |
| [`delete`](#delete) | `POST /confirmed-email/delete.json` | Deletes an email address from the account's confirmed email list. |

## create

`POST /confirmed-email/create.json` · [Documentation](https://docs.unione.io/en/web-api-ref#confirmed-email-create)

Adds an email address and sends a confirmation link.

### Request: `ConfirmedEmailRequest`

| Field | Type | Required | Description |
|---|---|---|---|
| `email` | `str` | yes | Email address to add or delete. |

### Response: `ConfirmedEmailCreateResponse`

| Field | Type | Description |
|---|---|---|
| `status` | `str` | "success" string (`success`) |
| `confirmed_email` | `ConfirmedEmail` |  |

### Example

```python
import unione
from unione.api.confirmed_email import ConfirmedEmailRequest

client = unione.client("YOUR_API_KEY")

response = client.confirmed_email.create(ConfirmedEmailRequest(
    email="dev@example.com",
))
print(response.confirmed_email)
```

## list

`POST /confirmed-email/list.json` · [Documentation](https://docs.unione.io/en/web-api-ref#confirmed-email-list)

Lists confirmed and unconfirmed email addresses for the account.

### Request

The method has no parameters.

### Response: `ConfirmedEmailListResponse`

| Field | Type | Description |
|---|---|---|
| `status` | `str` | "success" string (`success`) |
| `confirmed_emails` | `List[ConfirmedEmail]` |  |

### Example

```python
import unione

client = unione.client("YOUR_API_KEY")

response = client.confirmed_email.list()
print(response.confirmed_emails)
```

## delete

`POST /confirmed-email/delete.json` · [Documentation](https://docs.unione.io/en/web-api-ref#confirmed-email-delete)

Deletes an email address from the account's confirmed email list.

### Request: `ConfirmedEmailRequest`

| Field | Type | Required | Description |
|---|---|---|---|
| `email` | `str` | yes | Email address to add or delete. |

### Response: `ConfirmedEmailDeleteResponse`

| Field | Type | Description |
|---|---|---|
| `status` | `str` | "success" string (`success`) |
| `message` | `str` |  |

### Example

```python
import unione
from unione.api.confirmed_email import ConfirmedEmailRequest

client = unione.client("YOUR_API_KEY")

response = client.confirmed_email.delete(ConfirmedEmailRequest(
    email="dev@example.com",
))
print(response.message)
```
