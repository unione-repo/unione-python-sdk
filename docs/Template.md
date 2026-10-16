# Template

[Back to the list of sections](../README.md)

You have the option of storing a template on the UniOne side and then using it by id, which is highly recommended for sending repetitive messages or high volume traffic. UniOne supports two different [template engines](https://docs.unione.io/en/template-engines).

`unione.api.template.TemplateApi`, `client.template`

| Method | Endpoint | Description |
|---|---|---|
| [`set`](#set) | `POST /template/set.json` | Creates or updates an email template. |
| [`get`](#get) | `POST /template/get.json` | Gets template properties by it's id. |
| [`list`](#list) | `POST /template/list.json` | Returns the list of all or some templates of the account. |
| [`delete`](#delete) | `POST /template/delete.json` | Deletes a template by id. |

## set

`POST /template/set.json` · [Documentation](https://docs.unione.io/en/web-api-ref#template-set)

Creates or updates an email template.

Restrictions:
* The maximum request size is 10 MB.
* The number of templates is limited to 10000.

### Request: `TemplateSetRequest`

| Field | Type | Required | Description |
|---|---|---|---|
| `template` | `TemplateObject` | yes | Object with all the template properties. |

### Response: `TemplateSetResponse`

| Field | Type | Description |
|---|---|---|
| `status` | `str` | "success" string (`success`) |
| `template` | `TemplateObject` | Object with all the template properties. |

### Example

```python
import unione
from unione.api.template import TemplateSetRequest, TemplateObject, EditorType
from unione.common import TemplateEngine

client = unione.client("YOUR_API_KEY")

response = client.template.set(TemplateSetRequest(
    template=TemplateObject(
        name="name",
        editor_type=EditorType.HTML,
        template_engine=TemplateEngine.VELOCITY,
        subject="UniOne test email ",
        from_email="user@example.com",
        from_name="John Smith",
        reply_to="email@example.com",
        reply_to_name="John Smith",
    ),
))
print(response.template)
```

## get

`POST /template/get.json` · [Documentation](https://docs.unione.io/en/web-api-ref#template-get)

Gets template properties by it's id.

### Request: `TemplateGetRequest`

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | `str` | yes | Template id. |

### Response: `TemplateGetResponse`

| Field | Type | Description |
|---|---|---|
| `status` | `str` | "success" string (`success`) |
| `template` | `TemplateObject` | Object with all the template properties. |

### Example

```python
import unione
from unione.api.template import TemplateGetRequest

client = unione.client("YOUR_API_KEY")

response = client.template.get(TemplateGetRequest(
    id="00000000-0000-0000-0000-000000000000",
))
print(response.template)
```

## list

`POST /template/list.json` · [Documentation](https://docs.unione.io/en/web-api-ref#template-list)

Returns the list of all or some templates of the account.

You can iterate thru large list using "offset" and "limit" parameters. When less than "limit" templates are returned then the end of list is reached.

### Request: `TemplateListRequest`

| Field | Type | Required | Description |
|---|---|---|---|
| `limit` | `int` |  | Limits the number of templates returned, default is 50. |
| `offset` | `int` |  | Index of the first template in the list, starting with 0. |

### Response: `TemplateListResponse`

| Field | Type | Description |
|---|---|---|
| `status` | `str` | "success" string (`success`) |
| `templates` | `List[TemplateListObject]` | Array of template objects. |

### Example

```python
import unione
from unione.api.template import TemplateListRequest

client = unione.client("YOUR_API_KEY")

response = client.template.list(TemplateListRequest())
print(response.templates)
```

## delete

`POST /template/delete.json` · [Documentation](https://docs.unione.io/en/web-api-ref#template-delete)

Deletes a template by id.

### Request: `TemplateDeleteRequest`

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | `str` | yes | Template id. |

### Response: `SuccessResponse`

| Field | Type | Description |
|---|---|---|
| `status` | `str` | "success" string (`success`) |

### Example

```python
import unione
from unione.api.template import TemplateDeleteRequest

client = unione.client("YOUR_API_KEY")

response = client.template.delete(TemplateDeleteRequest(
    id="00000000-0000-0000-0000-000000000000",
))
```
