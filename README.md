# Postman

Postman Collection of our ZeroBounce API V2.

Postman is an API Development Environment (ADE). To download Postman, please visit
https://www.getpostman.com/

Once you install Postman, import the file `ZeroBounce_ API_ v2.postman_collection.json`.

To get started you will need an account on https://www.zerobounce.net/ to access your API key.

## Set your API key once

The collection uses Postman variables, so you no longer edit every request. After importing,
open the collection, go to **Variables**, and fill in:

| Variable | Used by | Notes |
|---|---|---|
| `base_url` | The 10 main-host requests | Switch region here. Pre-filled with the default host. |
| `api_key` | Everything except Warmup | Your ZeroBounce account |
| `warmup_api_key` | The **Warmup** folder only | Warmup is team-scoped and issued separately |

Leave `warmup_api_key` empty if you do not use the Warmup API.

## Regions

Set `base_url` to the region you were assigned:

| Region | `base_url` |
|---|---|
| Default | `https://api.zerobounce.net/v2` |
| USA | `https://api-us.zerobounce.net/v2` |
| EU | `https://api-eu.zerobounce.net/v2` |

All three serve the same account — the same key and the same credit balance work on each.

**Only the main API host is regional.** The bulk, Inbox Placement and Warmup hosts have no
`-us` or `-eu` variants, so the other 64 requests always use their single host. Those are
left as literal URLs rather than variables, so nothing implies a region switch that does
not exist.

## What is in the collection

Requests are grouped by product area:

| Folder | Requests | Notes |
|---|---|---|
| Account | 2 | Credits, API usage |
| Single Email | 4 | Validate, AI scoring, activity, email finder |
| Batch Validation | 1 | Up to 100 addresses, on the **main** API host |
| Bulk Email Validator | 4 | Send file, status, get file, delete file |
| Bulk AI Scoring | 4 | |
| Bulk Email Finder | 4 | |
| Bulk Domain Search | 4 | |
| List Evaluator | 3 | |
| Filters | 3 | Add, list, delete |
| Amazon S3 | 6 | Files already in your bucket |
| SFTP | 5 | Files on your SFTP server |
| Inbox Placement Tester | 8 | |
| Warmup | 26 | |

## Three different ways to authenticate

The API is not uniform here, and the collection reflects what each endpoint actually accepts:

- **Most endpoints** take `api_key` as a query parameter or form field.
- **Inbox Placement Tester** uses an `Authorization: Bearer <api_key>` header. Sent as an
  `api_key` parameter the request is rejected, and the key would land in a query string
  that gets logged.
- **Warmup** uses an `API-Key` header on its own host (`warmup-api.zerobounce.net`) with its
  own team-scoped key.

## Hosts

- `api.zerobounce.net/v2` — single email, batch validation, filters
- `bulkapi.zerobounce.net/v2` — bulk file jobs, list evaluator
- `bulkapi.zerobounce.net` (no `/v2`) — S3 and SFTP jobs
- `bulkapi.zerobounce.net/api/ipt` — Inbox Placement Tester
- `warmup-api.zerobounce.net/api/v1/warmup` — Warmup

Full API documentation: https://www.zerobounce.net/docs/
