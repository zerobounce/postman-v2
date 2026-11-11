# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project

The Postman collection for the ZeroBounce API v2: 74 requests across the validation, bulk, scoring, email finder, domain search, Inbox Placement Tester and Warmup APIs. Users import `ZeroBounce_ API_ v2.postman_collection.json` into Postman.

## Layout

- `ZeroBounce_ API_ v2.postman_collection.json`: the collection (Postman v2.1 format).
- `README.md`: importing, variables and regions.
- `.github/scripts/check_collection.py`: the CI check.

## Commands

```bash
python3 .github/scripts/check_collection.py
```

## Conventions

- **Never commit a key.** `api_key` and `warmup_api_key` stay empty in the file. CI fails if either has a value, or if a request carries a literal `api_key`.
- **Only the main API host is regional.** Requests to it use `{{base_url}}`; the bulk, Inbox Placement and Warmup hosts have no regional variants and stay literal URLs.
- **The Warmup folder uses `warmup_api_key`**, sent in an `API-Key` header. Every other request uses `api_key`.
