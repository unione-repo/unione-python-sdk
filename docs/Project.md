# Project

[Back to the list of sections](../README.md)

Projects allow you to group several independent domains, webhooks, templates, and unsubscription lists together. It's very useful if you have your own clients and manage their data from a single UniOne account. Each project receives its own API key, and all API calls with that API key only deal with the data of that project. This way, you can assign a separate project for each client and be sure that they won't conflict; e.g. unsubscribing from one project won't affect another.

Projects methods are disabled by default due to antispam measures. To enable them, [contact support](https://cp.unione.io/en/support).

Please note that sending domains are confirmed and used on per-project basis by default. But it's possible to allow projects to send emails from domains confirmed for main account - just [ask support](https://cp.unione.io/en/support) to enable it.

`unione.api.project.ProjectApi`, `client.project`

| Method | Endpoint | Description |
|---|---|---|
| [`create`](#create) | `POST /project/create.json` | Creates a new project. |
| [`update`](#update) | `POST /project/update.json` | Updates a project. |
| [`list`](#list) | `POST /project/list.json` | Lists projects. |
| [`delete`](#delete) | `POST /project/delete.json` | Deletes a project. |

## create

`POST /project/create.json` · [Documentation](https://docs.unione.io/en/web-api-ref#project-create)

Creates a new project.

### Request: `ProjectCreateRequest`

| Field | Type | Required | Description |
|---|---|---|---|
| `project` | `ProjectObject` | yes | Object with project properties. |

### Response: `ProjectCreateResponse`

| Field | Type | Description |
|---|---|---|
| `status` | `str` | "success" string (`success`) |
| `project_id` | `str` | Unqiue project identifier, ASCII string up to 36 characters long. |
| `project_api_key` | `str` | API key of the project. You can use it instead of the user API key parameter in all methods except project/* methods. |

### Example

```python
import unione
from unione.api.project import ProjectCreateRequest, ProjectObject

client = unione.client("YOUR_API_KEY")

response = client.project.create(ProjectCreateRequest(
    project=ProjectObject(
        name="Project 1A",
        country="ES",
        backend_domain_id=1234,
        unsubscribe_page_id=1,
    ),
))
print(response.project_id)
```

## update

`POST /project/update.json` · [Documentation](https://docs.unione.io/en/web-api-ref#project-update)

Updates a project.

### Request: `ProjectUpdateRequest`

| Field | Type | Required | Description |
|---|---|---|---|
| `project_id` | `str` |  | Unique project identifier. You should identify project to update either with project_id or with project_api_key field. But we recommend usage of project_id as a more secure option. |
| `project_api_key` | `str` |  | Optional project API key. You should identify project to update either with project_id or with project_api_key field. But we recommend usage of project_id as a more secure option. |
| `project` | `ProjectUpdateObject` | yes | Object with project properties. |

### Response: `ProjectUpdateResponse`

| Field | Type | Description |
|---|---|---|
| `status` | `str` | "success" string (`success`) |
| `project_api_key` | `str` | API key of the project. Returned only if the project to update was identified by project_api_key. Not returned in case of updating by project_id. |

### Example

```python
import unione
from unione.api.project import ProjectUpdateRequest, ProjectUpdateObject

client = unione.client("YOUR_API_KEY")

response = client.project.update(ProjectUpdateRequest(
    project_id="1234567890",
    project_api_key="your api_key",
    project=ProjectUpdateObject(
        name="Project 1A",
        country="ES",
        backend_domain_id=1234,
        unsubscribe_page_id=1,
    ),
))
print(response.project_api_key)
```

## list

`POST /project/list.json` · [Documentation](https://docs.unione.io/en/web-api-ref#project-list)

Lists projects.

### Request: `ProjectListRequest`

| Field | Type | Required | Description |
|---|---|---|---|
| `project_id` | `str` |  | Optional possibility to specify project_id to include only this project to list. |
| `project_api_key` | `str` |  | Optional possibility to specify project_api_key to include only this project to list. |

### Response: `ProjectListResponse`

| Field | Type | Description |
|---|---|---|
| `status` | `str` | "success" string (`success`) |
| `projects` | `List[ProjectListObject]` | Array of objects where each object represents one project. |

### Example

```python
import unione
from unione.api.project import ProjectListRequest

client = unione.client("YOUR_API_KEY")

response = client.project.list(ProjectListRequest(
    project_id="1234567890",
    project_api_key="your api_key",
))
print(response.projects)
```

## delete

`POST /project/delete.json` · [Documentation](https://docs.unione.io/en/web-api-ref#project-delete)

Deletes a project.

The project will be moved to the "trash bin" before being permanently deleted. You can restore the project by contacting support.

### Request: `ProjectDeleteRequest`

| Field | Type | Required | Description |
|---|---|---|---|
| `project_id` | `str` |  | Unique project identifier. You should identify project to delete either with project_id or with project_api_key field. We recommend usage of project_id as a more secure option. |
| `project_api_key` | `str` |  | Optional project API key. You should identify project to delete either with project_id or with project_api_key field. We recommend usage of project_id as a more secure option. |

### Response: `SuccessResponse`

| Field | Type | Description |
|---|---|---|
| `status` | `str` | "success" string (`success`) |

### Example

```python
import unione
from unione.api.project import ProjectDeleteRequest

client = unione.client("YOUR_API_KEY")

response = client.project.delete(ProjectDeleteRequest(
    project_id="1234567890",
    project_api_key="your api_key",
))
```
