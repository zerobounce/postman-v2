# Security Policy

## Reporting a Vulnerability

If you think you've found a security issue, please report it privately instead of opening a public issue.

**Email:** integrations@zerobounce.net (use a subject like `[postman-v2] Security`).

We'll look into reports as we can. If the issue is in the ZeroBounce API or service rather than this collection, we may forward it to the right team.

## Supported Versions

We fix the current state of `master`. Re-import the latest collection to pick up fixes.

## Tips for Using This Collection

* Set `api_key` and `warmup_api_key` as collection variables after importing. Leave them empty in any copy of the collection you export, share or commit.
* Postman can sync collections and their variable values to its cloud. Keep keys in an environment's current value, not its initial value, if you share a workspace.
* The validation API puts the key in the query string of `GET` requests, so it appears in Postman's history and console. Clear them before sharing a screen or a log.

Thanks for helping keep things secure.
